---
title: Details of run scripts
keywords: run script, log, optimization
summary: "We need to set OpenFOAM configurations, preProcessing.sh, and runScript.py for DAFoam optimization."
sidebar: mydoc_sidebar
permalink: mydoc_get_started_runscript.html
folder: mydoc
---

## OpenFOAM configurations

As mentioned in [Overview](index.html), DAFoam uses OpenFOAM for multiphysics analysis. So before running DAFoam optimizations, one needs to set up an OpenFOAM run case for NACA0012 airfoil. tutorials-master/NACA0012_Airfoil/incompressible has the following folder structure:

```bash
NACA0012_Airfoil/incompressible
|-- 0.orig            # initial fields and boundary conditions (OpenFOAM essentials)
|-- constant          # flow and turbulence property definition (OpenFOAM essentials)
|-- profiles          # NACA0012 profile coordinate for mesh generation
|-- system            # flow discretization, setup, time step, etc (OpenFOAM essentials)
|-- Allclean.sh       # script to clean up the simulation and optimization results
|-- preProcessing.sh  # generate mesh, copy the initial and boundary conditions to 0
|-- genAirFoilMesh.py # mesh generation script called by preProcessing.sh
|-- paraview.foam     # dummy file for paraview post-processing
|-- runScript.py      # main run script for DAFoam
```

Here we assume you are familiar with the OpenFOAM setup. Otherwise, refer to the [OpenFOAM tutorial guide](https://www.openfoam.com/documentation/tutorial-guide) for setting up the configuration files (i.e., the files in the 0, constant, and system folders). 

## preProcessing.sh

Once the OpenFOAM configuration files are properly set, we run the preProcessing.sh script to generate the mesh. This script first runs the genAirFoilMesh.py script to generate hyperbolic mesh using [pyHyp](https://github.com/mdolab/pyhyp), save the mesh to the plot3D format (volumeMesh.xyz). 

Then it uses the OpenFOAM's built-in utility plot3dToFoam to convert the plot3D mesh to the OpenFOAM mesh and save it to constant/polyMesh (`plot3dToFoam -noBlank volumeMesh.xyz`). 

Since the plot3D mesh does not have boundary information, the converted OpenFOAM mesh has only one boundary patch, so we need to use the autoPatch utility to split boundaries (`autoPatch 30 -overwrite`). Here 30 is the feature angle between two surface mesh faces. The utility will split patches if the feature angle is larger than 30 degree.

The above split patches will have names such as auto0, auto1, auto2, we need to rename them to wing, sym, inout, etc. This is done by running `createPatch -overwrite`. The definition of boundary name is in system/createPatchDict. 

Next we call `renumberMesh -overwrite` to renumber the mesh points to reduce the bandwidth of Jacobians and reduce the memory usage. Finally, we copy the boundary condition files 0.orig to 0.

```bash
#!/bin/bash

# Check if the OpenFOAM environments are loaded
if [ -z "$WM_PROJECT" ]; then
  echo "OpenFOAM environment not found, forgot to source the OpenFOAM bashrc?"
  exit
fi

# generate mesh
echo "Generating mesh.."
python genAirFoilMesh.py &> logMeshGeneration.txt
plot3dToFoam -noBlank volumeMesh.xyz >> logMeshGeneration.txt
autoPatch 30 -overwrite >> logMeshGeneration.txt
createPatch -overwrite >> logMeshGeneration.txt
renumberMesh -overwrite >> logMeshGeneration.txt
echo "Generating mesh.. Done!"

# copy initial and boundary condition files
cp -r 0.orig 0
```

## runScript.py

Once the OpenFOAM mesh is generated, we run `mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt` for optimization and save the detailed progress of optimization to logOpt.txt.

We first elaborate on the runScript.py script, which contains configurations for primal, adjoint, and optimization solutions.

The first section imports modules for DAFoam.

```python
# =============================================================================
# Imports
# =============================================================================
import os
import argparse
from mpi4py import MPI
from dafoam import PYDAFOAM, optFuncs
from pygeo import *
from pyspline import *
from idwarp import USMesh
from pyoptsparse import Optimization, OPT
import numpy as np
```

|

In the next section, we define the optimizer to use in "--opt". We use [pyOptSparse](https://github.com/mdolab/pyoptsparse) to set optimization problems. pyOptSparse supports multiple open-source and commercial optimizers. However, in runScript.py, we only provide optimizer setup for [slsqp](http://www.pyopt.org/reference/optimizers.slsqp.html) (default) and [snopt](https://ccom.ucsd.edu/~optimizers/solvers/snopt). Refer to [pyOptSparse documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/) for all supported optimizers.

The "--task" argument defines the task to run, which includes "opt": run optimization, "runPrimal": run the primal analysis, "runAdjoint": run the adjoint derivative computation, "solveCL": solve the angle of attack (alpha0) for a given CL_target. "verifySens": verify the adjoint accuracy, "testAPI": test the API of tutorials using Travis.

We then define some global parameters such at "U0": the far field velocity, "p0": the far field pressure, "nuTilda0", "k0", "epsilon0", "omega0": the far field turbulence variables, "CL_target": the target lift coefficient, "alpha0": the initial angle of attack, "A0": the reference area to normalize drag and lift coefficients.


```python
# =============================================================================
# Input Parameters
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument("--opt", help="optimizer to use", type=str, default="slsqp")
parser.add_argument("--task", help="type of run to do", type=str, default="opt")
args = parser.parse_args()
gcomm = MPI.COMM_WORLD

# Define the global parameters here
U0 = 10.0
p0 = 0.0
nuTilda0 = 4.5e-5
k0 = 0.015
epsilon0 = 0.14
omega0 = 100.0
CL_target = 0.5
alpha0 = 5.139186
A0 = 0.1
```

|

Next, the "daOptions" dictionary contains all the DAFoam parameters for primal and adjoint solvers. For a full list of input parameters in daOptions, refer to [here](https://dafoam.github.io/doxygen/html/classdafoam_1_1pyDAFoam_1_1DAOPTION.html).

"designSurfaces" is a list of patch names for the design surface to change during optimization. Here "wing" is a patch in constant/polyMesh/boundary and it needs to be of **wall** type. 

"DASimpleFoam" is an incompressible solver that uses the SIMPLE algorithm, and it is derived from the OpenFOAM's built-in solver simpleFoam with modification to compute adjoint derivatives. 

The "primalMinResTol" parameter is the residual convergence tolerance for the primal solver (DASimpleFoam). 

The "primalBC" dictionary defines the boundary conditions for primal solution. Note that if primalBC is defined, it will overwrite the values defined in the 0 folder. Here we need to provide the variable name, patch names, and value to set for each variable. If "primalBC" is left blank, we will use the BCs defined in the 0 folder. 

The "objFunc" dictionary defines the objective functions. Taking "CD" as an example, we need to give a name to the objective function, e.g., "CD" or any other preferred name, and the information for each part of the objective function. Most of the time, the objective has only one part (in this case "part1"), but one can also combine two parts of objectives, e.g., we can define a new objective that is the sum of force and moment. For each part, we need to define the type of objective (e.g., "force", "moment"; we need to use the reserved type names), how to select the discrete mesh faces to compute the objective (e.g., we select them from the name of a patch "patchToFace"), and the name of the patch (wing) for "patchToFace". Since it is a force objective, we need to project the force vector to a specific direction. Here we defines that "CD" is the force that is parallel to the flow direction ("parallelToFlow"). Alternative, we can also use "fixedDirection" and provide a "direction" key for force, i.e., "directionMode": "fixedDirection", "direction": [1.0, 0.0, 0.0]. Since we select "parallelToFlow", we need to prescribe the name of angle of attack design variable to determine the flow direction. Here "alpha" will be defined later in: DVGeo.addGeoDVGlobal("alpha", [alpha0], alpha, lower=-10.0, upper=10.0, scale=1.0).  NOTE: if no alpha is added in DVGeo.addGeoDVGlobal, we can NOT use "parallelToFlow". For this case, we have to use "directionMode": "fixedDirection" instead. The "scale" parameter is scaling factor for this objective "CD", i.e., CD = force / (0.5 * U0 * U0 * A0). Finally, if "addToAdjoint" is "True", the adjoint solver will compute the derivative for this objective. Otherwise, it will only calculate the objective value and print it to screen when solving the primal, no adjoint will be computed for this objective. The definition of "CL" is similar to "CD" except that we use "normalToFlow" for "directionMode".

The "adjEqnOption" dictionary contains the adjoint linear equation solution options. If the adjoint does not converge, increase "pcFillLevel" to 2. Or try "jacMatReOrdering" : "nd". By default, we require the adjoint equation to drop six orders of magnitudes.

"normalizeStates" contains the state normalization values. Here we use the far field values as reference. NOTE: since "p" is relative, we use the dynamic pressure "U0 * U0 / 2". Also, the face flux variable phi will be automatically normalized by its surface area so we can set "phi": 1.0. We also need to normalize the turbulence variables, such as nuTilda, k, omega, and epsilon.

The "adjPartDerivFDStep" dictionary contains the finite difference step sizes for computing partial derivatives in the adjoint solver. The delta for state is typically 1e-8 to 1e-6 and the delta for the FFD point displacement is typically LRef / 1000. 

The "adjPCLag" parameter allows us to compute the preconditioner (dRdWTPC) every a few adjoint equation solutions. Because the flow field does not significantly change during the optimization, we don't necessarily need to re-compute dRdWTPC for each optimization iteration. Setting adjPCLag to a large number increases the adjoint derivative speed because dRdWTPC consists of 20-30% of the total adjoint runtime. However, if the adjoint equation does not converge well, reduce adjPCLag such that we use the latest flow field to construct dRdWTPC.

Finally, we reserve an empty "designVar" dictionary and will add values for it later in "DVGeo.addGeoDVLocal".

```python
daOptions = {
    "designSurfaces": ["wing"],
    "solverName": "DASimpleFoam",
    "primalMinResTol": 1.0e-8,
    "primalBC": {
        "U0": {"variable": "U", "patches": ["inout"], "value": [U0, 0.0, 0.0]},
        "p0": {"variable": "p", "patches": ["inout"], "value": [p0]},
        "nuTilda0": {"variable": "nuTilda", "patches": ["inout"], "value": [nuTilda0]},
        "k0": {"variable": "k", "patches": ["inout"], "value": [k0]},
        "omega0": {"variable": "omega", "patches": ["inout"], "value": [omega0]},
        "epsilon0": {"variable": "epsilon", "patches": ["inout"], "value": [epsilon0]},
        "useWallFunction":True
    },
    "objFunc": {
        "CD": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["wing"],
                "directionMode": "parallelToFlow",
                "alphaName": "alpha",
                "scale": 1.0 / (0.5 * U0 * U0 * A0),
                "addToAdjoint": True,
            }
        },
        "CL": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["wing"],
                "directionMode": "normalToFlow",
                "alphaName": "alpha",
                "scale": 1.0 / (0.5 * U0 * U0 * A0),
                "addToAdjoint": True,
            }
        },
    },
    "adjEqnOption": {"gmresRelTol": 1.0e-6, "pcFillLevel": 1, "jacMatReOrdering": "rcm"},
    "normalizeStates": {
        "U": U0,
        "p": U0 * U0 / 2.0,
        "nuTilda": nuTilda0 * 10.0,
        "k": k0 * 10.0,
        "epsilon": epsilon0,
        "omega": omega0,
        "phi": 1.0,
    },
    "adjPartDerivFDStep": {"State": 1e-7, "FFD": 1e-3},
    "adjPCLag": 20,  # recompute preconditioner every 20 adjoint solutions
    "designVar": {},
}
```

|

Next, we need to define the mesh deformation and optimizer option. Users need to manually provide the point and normal of all symmetry planes for "symmetryPlanes" in meshOptions. For the optimizer options, we let the optimizer to run for maximal 50 steps, and set the tolerance of optimization to be 1e-7. These setup should work for most of the cases.

```python
# mesh warping parameters
meshOptions = {
    "gridFile": os.getcwd(),
    "fileType": "openfoam",
    "symmetryPlanes": [[[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]], [[0.0, 0.0, 0.1], [0.0, 0.0, 1.0]]],
}

# options for optimizers
if args.opt == "snopt":
    optOptions = {
        "Major feasibility tolerance": 1.0e-7,
        "Major optimality tolerance": 1.0e-7,
        "Function precision": 1.0e-7,
        "Verify level": -1,
        "Major iterations limit": 50,
        "Nonderivative linesearch": None,
        "Print file": "opt_SNOPT_print.txt",
        "Summary file": "opt_SNOPT_summary.txt",
    }
elif args.opt == "ipopt":
    optOptions = {
        "tol": 1.0e-7,
        "constr_viol_tol": 1.0e-7,
        "max_iter": 50,
        "output_file": "opt_IPOPT.txt",
        "mu_strategy": "adaptive",
        "limited_memory_max_history": 10,
        "nlp_scaling_method": "none",
        "alpha_for_y": "full",
        "recalc_y": "yes",
    }
elif args.opt == "slsqp":
    optOptions = {
        "ACC": 1.0e-7,
        "MAXIT": 50,
        "IFILE": "opt_SLSQP.txt",
    }
else:
    print("opt arg not valid!")
    exit(0)
```

|

In the next section, we set the design variable using the [pyGeo](https://github.com/mdolab/pygeo) module in the [MACH-Aero](https://github.com/mdolab/mach-aero) framework. We first create a DVGeo object (DVGeo = DVGeometry("./FFD/wingFFD.xyz")) to manipulate the design surface geometry using the free-form deformation (FFD) approach. NOTE: the FFD volume should completely contain the design surface (see the red dots from [this page](mydoc_get_started_run.html)). The FFD file wingFFD.xyz is generated by running "python genFFD.py" in the FFD folder. We then add a reference axis ("addRefAxis") for twist. Note that in this case we run 2D airfoil optimization, so no twist is needed, and "bodyAxis" is not used.

Once the FFD file is loaded and the reference axis is created, we select FFD points to move. The FFD file supports multi block meshes, but in this case we have only one block in the FFD, so we select "iVol = 0". We allow all the points to move so we set "pts[:, :, :]" for "indexList". Alternatively, we can select a subset of indices to move by setting a range for pts to move, e.g., indexList = pts[1:2, 3, 5:6].flatten(). 

Next, we call "DVGeo.addGeoDVLocal" to add a local shape variable "shapey" that moves in "y" direction with displacement bounds [-1.0:1.0]. The points we select to move are "PS = geo_utils.PointSelect("list", indexList)" (all points; see above) and provided into "DVGeo.addGeoDVLocal". After this, we set the design variable type for "shapey" in the daOptions dictionary. "FFD" is a type for shape design variable (e.g., "shape", "twist").

In addition to the shape variable, we add the angle of attack as the design variable. This is done by first defining "def alpha" function for angle of attack. This function takes "val" as input (i.e., angle of attack; "val" can also be an array) and changes the "geo" object (output). Here "geo" is a class object to change the displacement of FFD points. For the "alpha" function, we do not change the geometry or FFD so the "geo" object is not used. Instead, we compute the velocity components based on "U0" (global parameter defined previously) and update the "primalBC" key in daOptions. Then we call "DVGeo.addGeoDVGloal" to add angle of attack variable "alpha" with [0.0:10.0] degrees. The initial angle of attack is "[alpha0]", and the the function to change angle of attack is provided as "func=alpha". Again, we need to set the design variable type for "alpha", which is "AOA" (a reserved name). Here we also need to set at what patches the angle of attack is applied to (typically the names of far field patches) and the "flowAxis" and "normalAxis" for computing angle of attack: alpha = atan(U_normal/U_flow).

For more detailed explanation of design variable setup, refer to [MACH-Aero-Tutorials](https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/en/latest/opt_ffd.html).

```python
# =============================================================================
# Design variable setup
# =============================================================================
DVGeo = DVGeometry("./FFD/wingFFD.xyz")
DVGeo.addRefAxis("bodyAxis", xFraction=0.25, alignIndex="k")
# select points
iVol = 0
pts = DVGeo.getLocalIndex(iVol)
indexList = pts[:, :, :].flatten()
PS = geo_utils.PointSelect("list", indexList)
# shape
DVGeo.addGeoDVLocal("shapey", lower=-1.0, upper=1.0, axis="y", scale=1.0, pointSelect=PS)
daOptions["designVar"]["shapey"] = {"designVarType": "FFD"}
# angle of attack
def alpha(val, geo):
    aoa = val[0] * np.pi / 180.0
    inletU = [float(U0 * np.cos(aoa)), float(U0 * np.sin(aoa)), 0]
    DASolver.setOption("primalBC", {"U0": {"variable": "U", "patches": ["inout"], "value": inletU}})
    DASolver.updateDAOption()
DVGeo.addGeoDVGlobal("alpha", value=[alpha0], func=alpha, lower=0.0, upper=10.0, scale=1.0)
daOptions["designVar"]["alpha"] = {"designVarType": "AOA", "patches": ["inout"], "flowAxis": "x", "normalAxis": "y"}
```

|

In the next section, we initialize the DASolver object from DAFoam, and users usually don't need to change this section.

```python
# =============================================================================
# DAFoam initialization
# =============================================================================
DASolver = PYDAFOAM(options=daOptions, comm=gcomm)
DASolver.setDVGeo(DVGeo)
mesh = USMesh(options=meshOptions, comm=gcomm)
DASolver.addFamilyGroup(DASolver.getOption("designSurfaceFamily"), DASolver.getOption("designSurfaces"))
DASolver.printFamilyList()
DASolver.setMesh(mesh)
evalFuncs = []
DASolver.setEvalFuncs(evalFuncs)
```

|

After the DASolver is created, we can add geometric constraints (volume, thickness, and linear constraints) to ensures practical designs. 

Before setting the volume and thickness constraints, we need to first define the leading ("leList") and trailing ("teList") edges. For example, the leList includes two points that defines a straight line that is parallel to the leading edge. The straight line in leList should be close to the leading edge and completely within the wing surface mesh. 

Then we call "DVCon.addVolumeConstraint" to add a volume constraint with bounds [1.0:3.0]. Here we use relative upper and lower bound values with respect to the initial volume by setting "scaled=True". To compute the volume, pyGeo first constructs a 2D mesh from the "leList" and "teList". Here "nSpan = 2" and "nChord = 10" mean we use two points in the spanwise (z) and 10 points in the chordwise (x) to construct the 2D mesh. Then pyGeo projects this 2D mesh upward and downward to the wing surface mesh and form 3D trapezoid volumes to approximate the wing volume. The more the leList and teList are close to the actual leading and trailing edges of the airfoil mesh, the better the volume approximation will be. Also, increasing the nSpan and nChord gives a better volume approximation. We recommend nSpan and nChord be similar to the number of FFD points in the spanwise and chordwise directions.

Then we call "DVCon.addThicknessCOnstraints2D" to add thickness constraints with bounds [0.8:3.0]. Again we use relative value with respect to the initial thickness by setting "scaled=True". Similar to the volume constraint, pyGeo first construct a 2 by 10 mesh from the leList and teList and and projects the 2D mesh points upward and downward to the wing surface to compute the thickness at these 20 locations; we have 20 thickness constraints in total.

Next, we create linear constraints to link the shape changes between k=0 and k=1 so that the shape changes are same in the spanwise direction, this is needed only for the airfoil case where we have two symmetry planes. Here "nFFDs_x = pts.shape[0]" is the number of FFD points in the x direction. Here we impose: "lower <= factorA * dy_{k=0} + factorB * dy_{k=1} <= upper" with "dy" being the displacement of FFD point in the y direction, which is defined in the "DVGeo.addGeoDVLocal" function. Substituting the parameters into the above equation, we have: "0 <= dy_{k=0} - dy_{k=1} <= 0". In other words: "dy_{k=0} = dy_{k=1}".

Similarly, we create a linear constraint to fix the leading and trailing edge points. This is done by requiring the upper and lower FFD point on the leading and trailing edges to move in opposite directions. This constraint is needed because we do not want the shape variable to change the pitch and therefore the angle of attack. Instead, we want to change the far field velocity direction for the angle of attack.

For more detailed explanation of constraint setup, refer to [MACH-Aero-Tutorials](https://mdolab-mach-aero-tutorial.readthedocs-hosted.com/en/latest/opt_aero.html).

```python
# =============================================================================
# Constraint setup
# =============================================================================
DVCon = DVConstraints()
DVCon.setDVGeo(DVGeo)
DVCon.setSurface(DASolver.getTriangulatedMeshSurface(groupName=DASolver.getOption("designSurfaceFamily")))

leList = [[1e-4, 0.0, 1e-4], [1e-4, 0.0, 0.1 - 1e-4]]
teList = [[0.998 - 1e-4, 0.0, 1e-4], [0.998 - 1e-4, 0.0, 0.1 - 1e-4]]

# volume constraint
DVCon.addVolumeConstraint(leList, teList, nSpan=2, nChord=10, lower=1.0, upper=3, scaled=True)

# thickness constraint
DVCon.addThicknessConstraints2D(leList, teList, nSpan=2, nChord=10, lower=0.8, upper=3.0, scaled=True)

# Create linear constraints to link the shape change between k=0 and k=1
nFFDs_x = pts.shape[0] 
indSetA = []
indSetB = []
for i in range(nFFDs_x):
    for j in [0, 1]:
        indSetA.append(pts[i, j, 1])
        indSetB.append(pts[i, j, 0])
DVCon.addLinearConstraintsShape(indSetA, indSetB, factorA=1.0, factorB=-1.0, lower=0.0, upper=0.0)

# Create a linear constraint to fix the leading and trailing point.
indSetA = []
indSetB = []
for i in [0, nFFDs_x - 1]:
    for k in [0]:  # do not constrain k=1 because it is linked in the above symmetry constraint
        indSetA.append(pts[i, 0, k])
        indSetB.append(pts[i, 1, k])
DVCon.addLinearConstraintsShape(indSetA, indSetB, factorA=1.0, factorB=1.0, lower=0.0, upper=0.0)
```

|

In the next section, we assign the class objects created in the "runScript.py" script to "optFuncs.py". "optFuncs.py" is located in "dafoam/dafoam/optFuncs.py" and contains common functions to compute objective values and their derivatives.

```python
# =============================================================================
# Initialize optFuncs for optimization
# =============================================================================
optFuncs.DASolver = DASolver
optFuncs.DVGeo = DVGeo
optFuncs.DVCon = DVCon
optFuncs.evalFuncs = evalFuncs
optFuncs.gcomm = gcomm
```

|

In the final section, we set up the tasks. For "opt", we create an optimization problem ("optProb = Optimization") through the [pyOptSparse](https://github.com/mdolab/pyoptsparse) module and provide a function to compute objective ("objFun=..."). Here optFuncs.calcObjFuncValues is defined in "optFuncs.py". Then we add the objective function (drag) and physical constraint (lift). The names in "optProb.addObj" and "optProb.addCon" need to be consistent with the names defined in "objFunc" in daOption. Before running the optimization, we call "DASolver.runColoring()" to calculate the graph coloring for the dRdW matrix. Then we call "opt = OPT" to create the optimization and call "sol = opt" to solve the optimization. Here we provide a function to compute derivatives (sens=..). Again, optFuncs.calcObjFuncSens is defined in "optFuncs.py". 

Other tasks include "runPrimal": run the primal analysis, "runAdjoint": run the adjoint derivative computation, "solveCL": solve the angle of attack (alpha0) for a given CL_target. "verifySens": verify the adjoint accuracy, "testAPI": test the API of tutorials using Travis.
    

```python
# =============================================================================
# Task
# =============================================================================
if args.task == "opt":

    optProb = Optimization("opt", objFun=optFuncs.calcObjFuncValues, comm=gcomm)
    DVGeo.addVariablesPyOpt(optProb)
    DVCon.addConstraintsPyOpt(optProb)

    optProb.addObj("CD", scale=1)
    optProb.addCon("CL", lower=CL_target, upper=CL_target, scale=1)

    if gcomm.rank == 0:
        print(optProb)

    DASolver.runColoring()

    opt = OPT(args.opt, options=optOptions)
    histFile = "./%s_hist.hst" % args.opt
    sol = opt(optProb, sens=optFuncs.calcObjFuncSens, storeHistory=histFile)
    if gcomm.rank == 0:
        print(sol)

elif args.task == "runPrimal":

    optFuncs.runPrimal()

elif args.task == "runAdjoint":

    optFuncs.runAdjoint()

elif args.task == "solveCL":

    optFuncs.solveCL(CL_target, "alpha", "CL")

elif args.task == "verifySens":

    optFuncs.verifySens()

elif args.task == "testAPI":

    DASolver.setOption("primalMinResTol", 1e-2)
    DASolver.updateDAOption()
    optFuncs.runPrimal()

else:
    print("task arg not found!")
    exit(0)
```

|

## Optimization progress logOpt.txt

"logOpt.txt" is useful to monitor the optimization progress and identify potential issues. We will first see a summary of the optimization problem that includes the information for objective, all design variables and constraints. This is useful to verify the setup in "runScript.py".

```python
Optimization Problem -- opt
================================================================================
Objective Function: calcObjFuncValues

Objectives
   Index  Name            Value          Optimum
       0  CD     0.000000E+00     0.000000E+00

Variables (c - continuous, i - integer, d - discrete)
   Index  Name        Type      Lower Bound            Value      Upper Bound     Status
       0  alpha_0        c    -1.000000E+01     5.139186E+00     1.000000E+01           
       1  shapey_0       c    -1.000000E+00     0.000000E+00     1.000000E+00           
       2  shapey_1       c    -1.000000E+00     0.000000E+00     1.000000E+00           
     ...
     ...      
      19  shapey_18      c    -1.000000E+00     0.000000E+00     1.000000E+00           
      20  shapey_19      c    -1.000000E+00     0.000000E+00     1.000000E+00           

Constraints (i - inequality, e - equality)
   Index  Name                              Type    Lower      Value      Upper  Status   Lagrange 
       0  DVCon1_volume_constraint_0           i   1.0E+00    0.0E+00    3.0E+00     L    9.0E+100
       1  DVCon1_thickness_constraints_0       i   8.0E-01    0.0E+00    3.0E+00     L    9.0E+100
       2  DVCon1_thickness_constraints_0       i   8.0E-01    0.0E+00    3.0E+00     L    9.0E+100
      ...
      ...
      21  DVCon1_linear_constraint_0_shapey    e   0.0E+00    0.0E+00    0.0E+00          9.0E+100
      22  DVCon1_linear_constraint_0_shapey    e   0.0E+00    0.0E+00    0.0E+00          9.0E+100
      ...
      ...
      31  DVCon1_linear_constraint_1_shapey    e   0.0E+00    0.0E+00    0.0E+00          9.0E+100
      32  DVCon1_linear_constraint_1_shapey    e   0.0E+00    0.0E+00    0.0E+00          9.0E+100
      33  CL                                   e   5.0E-01    0.0E+00    5.0E-01     E    9.0E+100
```

|

Next, we will see the progress of the coloring solver

```python
+--------------------------------------------------------------------------+
|                       Running Coloring Solver                            |
+--------------------------------------------------------------------------+
...
...
Calculating dRdW Coloring... 0 s
Calculating dRdW Coloring..
Parallel Distance 2 Graph Coloring....
MaxCols: 129
AllNonZeros: 2539971
nUniqueCols: 10291
ColorSweep: 0   1 s
number of uncolored: 31694 4
ColorSweep: 100   1 s
number of uncolored: 19158 4
ColorSweep: 200   2 s
number of uncolored: 7950 4
...
...
```

|

Once the coloring is computed, we first solve the primal to obtain the objective function value.

```python
+--------------------------------------------------------------------------+
|                  Evaluating Objective Functions 000                      |
+--------------------------------------------------------------------------+
Design Variables: 
OrderedDict([('alpha', array([5.139186])), ('shapey', array([0., 0., 0., 0., 0., 0., 0., 0., 0., 
0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]))])
...
...
Time = 1
U Initial residual: (0.9999999999986563 1 0.9999999794693428)
U   Final residual: (0.08240762811390384 0.08007994807629101 0.08735247207649212)
p Initial residual: 1
p   Final residual: 0.09187576310824178
Time step continuity errors : sum local = 0.002527994818431577
                                 global = 0.0009814325462186569
                             cumulative = 0.0009814325462186569
nuTilda Initial residual: 0.9999999999995365
          Final residual: 0.07796197615755995
CD-part1-force: 0.5024804194374696
CL-part1-force: -0.04014023236014436
ExecutionTime = 5.46 s  ClockTime = 6 s
...
...
Time = 437
Minimal residual 9.722186140334214e-09 satisfied the prescribed tolerance 1e-08
...
...
Objective Functions: 
{'DVCon1_volume_constraint_0': 1.0000000000000018, 'DVCon1_thickness_constraints_0': array([
1.0000000000000102, 0.9999999999999997, 1.0000000000000004, 1.0000000000000002, 1.                , 
1.0000000000000002, 0.9999999999999994, 1.0000000000000002, 0.9999999999999998, 1.0000000000000033, 
1.0000000000000056, 0.9999999999999996, 0.9999999999999999, 1.0000000000000002, 1.0000000000000002,
1.0000000000000002, 0.9999999999999998, 1.0000000000000002,0.9999999999999998, 1.0000000000000007]), 
'CD': 0.020820258191996517, 'CL': 0.4999999575481259, 'fail': False}
Flow Runtime: 2.62659
```

|

After the primal solution is done, we call the adjoint solver to compute derivatives.

```python
+--------------------------------------------------------------------------+
|              Evaluating Objective Function Sensitivities 000             |
+--------------------------------------------------------------------------+
...
dRdWT: 0 of 380, ExecutionTime: 9 s
dRdWT: 100 of 380, ExecutionTime: 10 s
...
Solving Linear Equation... 17 s
Main iteration 0 KSP Residual norm 3.216462436656e-02 17 s
Main iteration 100 KSP Residual norm 5.825540354005e-05 18 s
Main iteration 167 KSP Residual norm 2.962925212261e-08 19 s 
...
Computing total derivatives....
Calculating the dXvdFFD matrix with epsFFD: 0.001
Computing total derivatives for shapey
Partial deriative matrix created. 21 s
dRdFFD: 0 of 20, ExecutionTime: 21 s
dRdFFD: 19 of 20, ExecutionTime: 22 s
...
```

|

The above process will repeat until the optimization converges. 

In the [next section](mydoc_get_started_common_modifications.html), we will elaborate on some common modification for this case.

{% include links.html %}

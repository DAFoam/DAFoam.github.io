---
title: UAV propeller - aerodynamic optimization of turbomachinery
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: user-guide-uav-prop.html
folder: mydoc
---

## Learning Objectives:

This chapter includes a detailed explaination for the relevant files such as the runScript for the aerodynamic NACA0012 UAV Propeller case.

After reading this chapter, you should be able to: 

- Describe the folders, files and scripts for a DAFoam optimization case
- Describe the structure of the runScript for a UAV Propeller optimization
- ...
- ...


## Overview of the NACA0012 UAV Propeller optimization 

The following is an aerodynamic shape optimization case for a UAV propeller in hover conditions:

<pre>
Case: UAV Propeller aerodynamic optimization 
Geometry: NACA0012 UAV Propeller
Objective function: Shaft Power Coefficient 
Design variables: 6 twist variables, 72 shape variables, 6 chord variables, rotation speed 
Constraints: Thrust coefficient, propeller thickness, propeller spanwise curvature, leading edge, mass 
Rotation rate: 5000 RPM
Reynolds number: 0.180 million
Mesh cells: ~1.5 Million
Solver: DARhoSimpleFoam
</pre>


Below is the file and directory structure for the aerodynamic NACA0012 UAV Propeller case in the DAFoam tutorial. 

To run the optimization, first run preProcessing.sh to generate the mesh, and then run runScript.py. If you wish to re-run the optimizaion, make sure to run Allclean.sh first.

We will explain in detail the files and directories that are unique to DAFoam.

```bash
NACA0012_Airfoil/incompressible
|-- 0.orig            # initial fields and boundary conditions (OpenFOAM essentials)
|-- constant          # flow and turbulence property definition (OpenFOAM essentials)
|-- system            # flow discretization, setup, time step, etc (OpenFOAM essentials)
|-- Allclean.sh       # script to clean up the simulation and optimization results
|-- preProcessing.sh  # generate mesh, copy the initial and boundary conditions to 0
|-- paraview.foam     # dummy file for paraview post-processing
|-- runScriptAero.py  # main run script for DAFoam -- aerodynamic optimization only case
|-- runScriptAeroStruct.py # main run script for DAFoam -- aerostructural optimization case
|-- runScriptMultipoint.py # main run script for DAFoam -- multipoint optimization case
|-- tacsSetup.py      # TACS setup -- structural case only 
```

## 0.orig

The 0.orig directory contains the initial condition for a DAFoam case. The preProcessing.sh script duplicates it as the 0 directory, and then it functions the same way as in OpenFoam.

## preProcessing.sh

Once the OpenFOAM configuration files are properly set, we run the preProcessing.sh script to download the polyMesh. This is downloaded as a `.tar` folder. This folder will be moved to the `constant` folder.  

Next, the structural mesh is downloaded as a `.bdf` file (this will not be used in the example case for this user guide). 

Next, we simply generate the mesh from the downloads. Finally, we copy the boundary condition files 0.orig to 0.

```bash
#!/bin/bash

# Check if the OpenFOAM enviroments are loaded
if [ -z "$WM_PROJECT" ]; then
  echo "OpenFOAM environment not found, forgot to source the OpenFOAM bashrc?"
  exit
fi

if [ -f "constant/polyMesh" ]; then
  echo "Mesh already exists."
else
  echo "Downloading mesh polyMesh_UAV_Propeller.tar"
  wget https://github.com/dafoam/files/releases/download/v1.0.0/polyMesh_UAV_Propeller.tar
fi
tar -xvf polyMesh_UAV_Propeller.tar
mv polyMesh constant/

if [ -f "Structure.bdf" ]; then
  echo "Mesh already exists."
else
  echo "Downloading mesh StructMesh.bdf.tar.gz"
  wget https://github.com/dafoam/files/releases/download/v1.0.0/StructMesh.bdf.tar.gz
fi


echo "Generating mesh.. Done!"

# copy initial and boundary condition files
cp -r 0.orig 0
```

To change the propeller configuration and mesh, simply modify the `.preProcessing.sh` file to download the correct mesh for any propeller.


## runScriptAero.py

Once the OpenFOAM mesh is generated, we run `mpirun -np 144 python runScriptAero.py 2>&1 | tee logOpt.txt` for optimization and save the detailed progress of optimization to logOpt.txt.

We first elaborate on the runScriptAero.py script, which contains configurations for primal, adjoint, and optimization solutions.

The first section imports modules for DAFoam.

```python
# =============================================================================
# Imports
# =============================================================================
import os
import argparse
import numpy as np
from mpi4py import MPI
import openmdao.api as om
from mphys.multipoint import Multipoint
from dafoam.mphys import DAFoamBuilder, OptFuncs
from mphys.scenario_aerodynamic import ScenarioAerodynamic
from pygeo.mphys import OM_DVGEOCOMP
from pygeo import geo_utils

import tacsSetup
```

|

In the next section, we define the optimizer to use in "-optimizer". We use [pyOptSparse](https://github.com/mdolab/pyoptsparse) to set optimization problems. pyOptSparse supports multiple open-source and commercial optimizers. However, in runScript.py, we only provide optimizer setup for [IPOPT](https://coin-or.github.io/Ipopt) (default), [SLSQP](http://www.pyopt.org/reference/optimizers.slsqp.html), and [SNOPT](https://ccom.ucsd.edu/~optimizers/solvers/snopt). Refer to [pyOptSparse documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/) for all supported optimizers.

The "-task" argument defines the task to run, which includes "run_driver": run optimization, "run_model": run the primal analysis, "compute_totals": run the adjoint derivative computation, "check_totals": verify the adjoint accuracy against the finite-difference method.

We then define some global parameters such at "omega0": this is the propeller RPM in rad/s, "thrust_target": this is the target thrust for the propeller, and "m0": this is the hover mass and is not important for the aerodynamic-only optimization. 


```python
parser = argparse.ArgumentParser()
# which optimizer to use. Options are: IPOPT (default), SLSQP, and SNOPT
parser.add_argument("-optimizer", help="optimizer to use", type=str, default="SNOPT")
# which task to run. Options are: opt (default), runPrimal, runAdjoint, checkTotals
parser.add_argument("-task", help="type of run to do", type=str, default="opt")
# which case to opt. Options are: 1 - twist
parser.add_argument("-case", help="which case to optimize", type=int, default=1)
args = parser.parse_args()

# =============================================================================
# Input Parameters
# =============================================================================
omega0 = 523.6
thrust_target = 6.5
m0 = 0.02824
```

|

Next, the "daOptions" dictionary contains all the DAFoam parameters for primal and adjoint solvers. For a full list of input parameters in daOptions, refer to [here](https://dafoam.github.io/doxygen/html/classdafoam_1_1pyDAFoam_1_1DAOPTION.html).

"designSurfaces" is a list of patch names for the design surface to change during optimization. 

"DARhoSimpleFoam" is a compressible solver that uses the SIMPLE algorithm, and it is derived from OpenFOAM's built-in solver rhoSimpleFoam with modifications to compute adjoint derivatives. 

The "primalMinResTol" parameter is the residual convergence tolerance for the primal solver (DASimpleFoam). Coupled with that, the "primalMinResTolDiff" is used to tweak how much difference between primalMinResTol and the actual primal convergence is consider to be fail=True for the primal solution.

Since this is a propeller in hover, we set "hasIterativeBC" to be true to enforce iterative boundary conditions. We also set "useConstrainHbyA" to true to directly compute the HbyA term without any constraints. In this case, without that HbyA term, it may diverge without the constrainHbyA, e.g., the MRF cases with the SST model. Here we have an option to add the constrainHbyA back to the primal and adjoint solvers.

The "primalBC" dictionary defines the boundary conditions for the primal solution. Note that if primalBC is defined, it will overwrite the values defined in the 0 folder. Here we need to provide the variable name, patch names, and value to set for each variable. If "primalBC" is left blank, we will use the BCs defined in the 0 folder. 

Next, we define the "primalVarBounds", which defines the upper and lower bounds for the primal solution. In this case, we define a minimum omega. 

The "objFunc" dictionary defines our objective and constraint functions. Some of these parameters within the objFunc are the same as in the NACA0012 Airfoil case. Specifically in the propeller case, we want to define the "power", with important parts here are setting the type to "power", we set the "patches" type to "blade" since this is a propeller, we set the "axis" and "center", and we make sure to include this in the adjoint calculation by setting "addToAdjoint" to "True". The thrust here is set as "fixedDirection" to fix the direction of thrust while the propeller is in hover. We again add this to the adjoint calculation. For both "skewness" and "nonOrtho", we define these as mesh quality checks as the optimization is running. 

We set "adjStateOrdering" explicity here to "cell" because the default is "state". This simply sets the ordering of the state variable, with two options "state" and "cell". 

Now, we set the parameters for the adjoint calculation using "adjEqnOption" dictionary. 

Next, we set the "adjPCLag", whic is the interval of recomputing the pre-conditioner matrix dRdWTPC for solveAdjoint. By default, dRdWTPC will be re-computed each time the solveAdjoint function is called. However, you can increase the lag to skip it and reuse the dRdWTPC computed previously.

Next, we set our normalized states in the "normalizedStates" dictionary. Here, we simply set the states for generally standard temperature and pressure values for the propeller in hover. 

In the "checkMeshTreshold" dictionary, we just add this for a check to make sure that the nonorthogonality and skewness are within our constraints. 

Finally, we set our design variables and declare the "decomposeParDict", which is a file that will be automatically written such that we can run an optimization with any number of CPU cores without the need to manually change "decomposeParDict".

```python
daOptions = {
    "designSurfaces": ["blade"],
    "solverName": "DARhoSimpleFoam",
    "primalMinResTol": 1.0e-8,
    "primalMinResTolDiff": 1.0e4,
    # set it to True for hover case
    "hasIterativeBC": True,
    "useConstrainHbyA": True,
    "primalBC": {
        "MRF": omega0,
        "useWallFunction": False,
    },
    "primalVarBounds": {
        "omegaMin": -1e16,
    },
    "objFunc": {
        "power": {
            "part1": {
                "type": "power",
                "source": "patchToFace",
                "patches": ["blade"],
                "axis": [1.0, 0.0, 0.0],
                "center": [0.0, 0.0, 0.0],
                "scale": -2.0,
                "addToAdjoint": True,
            }
        },
        "thrust": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["blade"],
                "directionMode": "fixedDirection",
                "direction": [1.0, 0.0, 0.0],
                "scale": -2.0,
                "addToAdjoint": True,
            }
        },
        "skewness": {
            "part1": {
                "type": "meshQualityKS",
                "source": "boxToCell",
                "min": [-10.0, -10.0, -10.0],
                "max": [10.0, 10.0, 10.0],
                "coeffKS": 20.0,
                "metric": "faceSkewness",
                "scale": 1.0,
                "addToAdjoint": True,
            },
        },
        "nonOrtho": {
            "part1": {
                "type": "meshQualityKS",
                "source": "boxToCell",
                "min": [-10.0, -10.0, -10.0],
                "max": [10.0, 10.0, 10.0],
                "coeffKS": 1.0,
                "metric": "nonOrthoAngle",
                "scale": 1.0,
                "addToAdjoint": True,
            },
        },
    },
    "adjStateOrdering": "cell",
    "adjEqnOption": {
        "gmresRelTol": 1.0e-3,
        "pcFillLevel": 1,
        "jacMatReOrdering": "natural",
        "gmresMaxIters": 1000,
        "gmresRestart": 1000,
        "useNonZeroInitGuess": True,
    },
    "adjPCLag": 1,
    "normalizeStates": {
        "U": 50.0,
        "p": 101325.0,
        "T": 300.0,
        "nuTilda": 1e-3,
        "phi": 1.0,
    },
    "checkMeshThreshold": {
        "maxNonOrth": 89.0,
        "maxSkewness": 5.0,
    },
    "designVar": DVDict,
    "decomposeParDict": {"preservePatches": ["cyc1", "cyc2"]},
}
```

Next, we need to define the mesh options, shown below.

```python
meshOptions = {
    "gridFile": os.getcwd(),
    "fileType": "OpenFOAM",
    "useRotations": False,
    # point and normal for the symmetry plane
    "symmetryPlanes": [],
}
```

Now, we set up the top class, defined as 

```python
class Top(Multipoint):
```

Inside this OpenMDAO class, we first setup the problem. Similar to the NACA0012 airfoil case, we first set up the DAFoam solver. In this case, we call it the "aero_builder" rather than "dafoam_builder". Next, we add our subsystems, with "dvs" being a set of independent variable components, which we tend to use as inputs, "mesh_aero" being the aerodynamnic mesh that we use for the optimization, and "geometry" being the set of FFD points for the geometry. Next, we use mPhys to set up the aerodynamic scenario, which we call "hover" for this case. Lastly, we connect the x_aero0 from the mesh and geometry components and subsequently x_aero0 also from the geometry component to the hover scenario group. This is the surface mesh coordinate. 

```python
def setup(self):
  # create the builder to initialize the DASolvers
  aero_builder = DAFoamBuilder(daOptions, meshOptions, scenario="aerodynamic")
  aero_builder.initialize(self.comm)

  # add the design variable component to keep the top level design variables
  self.add_subsystem("dvs", om.IndepVarComp(), promotes=["*"])

  # add the aerodynamic mesh component
  self.add_subsystem("mesh_aero", aero_builder.get_mesh_coordinate_subsystem())

  # add the geometry component (FFD)
  self.add_subsystem("geometry", OM_DVGEOCOMP(file="FFD/FFD.xyz", type="ffd"))

  self.mphys_add_scenario("hover", ScenarioAerodynamic(aero_builder=aero_builder))

  # need to manually connect the x_aero0 between the mesh and geometry components
  # here x_aero0 means the surface coordinates of structurally undeformed mesh
  self.connect("mesh_aero.x_aero0", "geometry.x_aero_in")
  # need to manually connect the x_aero0 between the geometry component and the hover
  # scenario group
  self.connect("geometry.x_aero0", "hover.x_aero")
```

Next, we set up the `configure(self)` function. First, we add the objective function to the hover scenario: `self.hover.aero_post.mphys_add_funcs()`. 

Similar to the NACA0012 airfoil case, we add the surface coordinates and set the triangular points for geometric constraints. 

```python
# get the surface coordinates from the mesh component
points = self.mesh_aero.mphys_get_surface_mesh()

# add pointset to the geometry component
self.geometry.nom_add_discipline_coords("aero", points)

# set the triangular points to the geometry component for geometric constraints
tri_points = self.mesh_aero.mphys_get_triangulated_surface()
self.geometry.nom_setConstraintSurface(tri_points)
```



## Allclean.sh

Allclean.sh is used for wiping all data generated by previous optimization runs and restore the default setup. If you wish to rerun the optimziation, make sure to use Allclean.sh first. Otherwise, DAFoam will not run and it will lead to errors.



{% include note.html content="This webpage is under construction." %}


{% include links.html %}

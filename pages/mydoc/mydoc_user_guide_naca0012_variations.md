---
title: NACA0012 variations - compressibility, multi-point, multi-cases
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_naca0012_variations.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## Subsonic and transonic optimization

The following is the overview of an aerodynamic shape optimization case for the NACA0012 airfoil in subsonic conditions. 

<pre>
Case: Airfoil aerodynamic optimization 
Geometry: NACA0012
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.5
Design variables: 20 free-form deformation (FFD) points moving in the y direction, one angle of attack
Constraints: Symmetry, volume, thickness, and lift constraints (total number: 34)
Mach number: 0.294 (100 m/s)
Reynolds number: 6.667 million
Mesh cells: ~4,500
Solver: DARhoSimpleFoam
</pre>

The "runScript.py" is similar to the one used in the NACA0012 [incompressible case](mydoc_user_guide_naca0012.html) with the following exceptions:

- In the global parameters, we provide additional variable such as "T0" (far field temperature) and "rho0" (a reference density to normalize CD and CL). In addition, we provide the absolute value of pressure "p", instead of the relative value use in the low speed case.

```python
# =============================================================================
# Input Parameters
# =============================================================================
U0 = 100.0
p0 = 101325.0
T0 = 300.0
nuTilda0 = 4.5e-5
CL_target = 0.5
aoa0 = 4.0
A0 = 0.1
# rho is used for normalizing CD and CL
rho0 = p0 / T0 / 287
```


- In "primalBC", we need to set boundary condition for temperature "T0".

- We use "DARhoSimpleFoam", which is an OpenFOAM built-in compressible flow solver suitable for subsonic conditions. Accordingly, we set "flowCondition" to "Compressible".

```python
# Input parameters for DAFoam
daOptions = {
    "designSurfaces": ["wing"],
    "solverName": "DARhoSimpleFoam",
    "primalMinResTol": 1.0e-8,
    "primalBC": {
        "U0": {"variable": "U", "patches": ["inout"], "value": [U0, 0.0, 0.0]},
        "p0": {"variable": "p", "patches": ["inout"], "value": [p0]},
        "T0": {"variable": "T", "patches": ["inout"], "value": [T0]},
        "nuTilda0": {"variable": "nuTilda", "patches": ["inout"], "value": [nuTilda0]},
        "useWallFunction": True,
    },
    "function": {
        "CD": {
            "type": "force",
            "source": "patchToFace",
            "patches": ["wing"],
            "directionMode": "parallelToFlow",
            "patchVelocityInputName": "patchV",
            "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
        },
        "CL": {
            "type": "force",
            "source": "patchToFace",
            "patches": ["wing"],
            "directionMode": "normalToFlow",
            "patchVelocityInputName": "patchV",
            "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
        },
    },
    "adjEqnOption": {"gmresRelTol": 1.0e-6, "pcFillLevel": 1, "jacMatReOrdering": "rcm"},
    "normalizeStates": {
        "U": U0,
        "p": p0,
        "T": T0,
        "nuTilda": nuTilda0 * 10.0,
        "phi": 1.0,
    },
    "inputInfo": {
        "aero_vol_coords": {"type": "volCoord", "components": ["solver", "function"]},
        "patchV": {
            "type": "patchVelocity",
            "patches": ["inout"],
            "flowAxis": "x",
            "normalAxis": "y",
            "components": ["solver", "function"],
        },
    },
}
```


## transonic optimization

The following is the overview of an aerodynamic shape optimization case for the NACA0012 airfoil in transonic conditions.

<pre>
Case: Airfoil aerodynamic optimization 
Geometry: NACA0012
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.5
Design variables: 20 free-form deformation (FFD) points moving in the y direction, one angle of attack
Constraints: Symmetry, volume, thickness, and lift constraints (total number: 34)
Mach number: 0.7 (238 m/s)
Reynolds number: 15.9 million
Mesh cells: ~4,500
Solver: DARhoSimpleCFoam
</pre>


The "runScript.py" is similar to the one used in the NACA0012 subsonic case mentioned above with the following exceptions:

- We use "DARhoSimpleCFoam", which is an OpenFOAM built-in compressible flow solver with the "SIMPLEC" algorithm that is suitable for transonic conditions.

- The far field velocity is 238 m/s with Mach number of 0.7.

- We use special treatment for the preconditioner matrix to improve the convergence of adjoint linear equation by setting "transonicPCOption": 1. This option is only needed for transonic conditions.

```python
# Input parameters for DAFoam
daOptions = {
    "designSurfaces": ["wing"],
    "solverName": "DARhoSimpleCFoam",
    "primalMinResTol": 1.0e-8,
    "primalBC": {
        "U0": {"variable": "U", "patches": ["inout"], "value": [U0, 0.0, 0.0]},
        "p0": {"variable": "p", "patches": ["inout"], "value": [p0]},
        "T0": {"variable": "T", "patches": ["inout"], "value": [T0]},
        "nuTilda0": {"variable": "nuTilda", "patches": ["inout"], "value": [nuTilda0]},
        "useWallFunction": True,
    },
    "function": {
        "CD": {
            "type": "force",
            "source": "patchToFace",
            "patches": ["wing"],
            "directionMode": "parallelToFlow",
            "patchVelocityInputName": "patchV",
            "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
        },
        "CL": {
            "type": "force",
            "source": "patchToFace",
            "patches": ["wing"],
            "directionMode": "normalToFlow",
            "patchVelocityInputName": "patchV",
            "scale": 1.0 / (0.5 * U0 * U0 * A0 * rho0),
        },
    },
    "adjEqnOption": {"gmresRelTol": 1.0e-6, "pcFillLevel": 1, "jacMatReOrdering": "rcm"},
    # transonic preconditioner to speed up the adjoint convergence
    "transonicPCOption": 1,
    "normalizeStates": {
        "U": U0,
        "p": p0,
        "T": T0,
        "nuTilda": nuTilda0 * 10.0,
        "phi": 1.0,
    },
    "inputInfo": {
        "aero_vol_coords": {"type": "volCoord", "components": ["solver", "function"]},
        "patchV": {
            "type": "patchVelocity",
            "patches": ["inout"],
            "flowAxis": "x",
            "normalAxis": "y",
            "components": ["solver", "function"],
        },
    },
}
```


Place holder text, don't change!

## Multi-point optimization

Place holder text, don't change!

## Multi-case optimization

The following is a multi-case aerodynamic shape optimization problem for the NACA0012 airfoil. This tutorial will show you how to use one runScript.py to run multiple cases within one folder. Go to the directory: /tutorials-master/NACA0012_Airfoil/multicase, we will see two subdirectories, SA and SST, which are the two cases we are going to run. To do that, we need create the builder to initialize the DASolvers for both cases In the `setup(self)` function.

'''python
    def setup(self):

        # create the builder to initialize the DASolvers for both cases (they share the same mesh option)
        dafoam_builder_sa = DAFoamBuilder(daOptionsSA, meshOptions, scenario="aerodynamic", run_directory="SA")
        dafoam_builder_sa.initialize(self.comm)

        dafoam_builder_sst = DAFoamBuilder(daOptionsSST, meshOptions, scenario="aerodynamic", run_directory="SST")
        dafoam_builder_sst.initialize(self.comm)
'''

Place holder text, don't change!


{% include links.html %}

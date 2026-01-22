---
title: NACA0012 Incompressible Surrogate Based Optimization
keywords: tutorial, surrogate
summary: Shape optimization of the NACA0012 airfoil to reduce drag with a fixed lift force
sidebar: mydoc_sidebar
permalink: tutorials-SBO-naca0012.html
folder: mydoc
---

The following tutorial is an optimization of the NACA0012 airfoil to reduce drag while maintaining a predefined lift value. This shape optimization is handled via a surrogate based optimization method utilizing the [SMT](https://smt.readthedocs.io/en/latest/index.html) python package.

<pre>
Case: Airfoil aerodynamic optimization 
Geometry: NACA0012
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.5
Design variables: 8 free-form deformation (FFD) points moving in the y direction, one angle of attack
Constraints: Symmetry and lift constraint (total number: 2)
Mach number: 0.02941 (10 m/s)
Reynolds number: 0.6667 million
Mesh cells: ~4,000
Solver: DASimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/CHT_ubend_ffd.png" style="width:500px !important;" />

Fig. 1. Mesh and FFD points for the NACA0012 airfoil

The surrogate based optimization capability in DAFoam is designed in such a way that any DAFoam opitmization case can be converted to a surrogate based optimization case by adding one additional python file to configure the surrogate optimization. For this variation of the NACA0012, this file is `runScript_SBO.py` which can be found in the [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) under the NACA0012_SBO case folder.

The first part of `runScript_SBO.py` is to import the necessary packages and the case setup (the OpenMDAO model):

```python
import numpy as np                                 # use numpy for arrays
from runScript import prob as NACA0012             # import OpenMDAO model of airfoil from runScript
from dafoam.pyDAFoam import surrogateOptimization  # import surrogate optimization class
```

`Numpy` arrays are required by [SMT](https://smt.readthedocs.io/en/latest/index.html) for the design variable arrays. The secong import, `from runScript import prob as NACA0012` imports the OpenMDAO model from `runScript.py` and renamed to `NACA0012`. This model will be passed to the surrogate optimization class to perform the actual optimization. The last import, `from dafoam.pyDAFoam import surrogateOptimization`, imports the surrogate optimization class which will execute the optimization.

Following this, we need to define the design variables of the problem:

```python
# define design variables (name & size)
dvNames = ["shape", "patchV"]
dvSizes = [8, 2]

# prescribe bounds on design variables
xlimits = np.array([[-0.05, 0.05]] * 10)

# adjust bounds for AOA, fix velocity to 10m/s, and limit trailing edge FFD displacement
xlimits[-1] = [0, 3]                          
xlimits[-2] = [10, 10 + 1e-9]                  
xlimits[-3] = [-0.01, 0.01]                    
xlimits[-4] = [-0.01, 0.01]
```

`dvNames` lists only the names of the design variables which must match the naming convention in `runScript.py`. `dvSizes` gives the number of actual design variables (e.g. The `shape` design variable uses 8 FFD points, hence the first element of `dvSizes` is 8. `patchV` is an array which contains the far field velocity and angle of attack, hence the size is given as 2). In total, this gives 10 points for which we must prescribe design variable bounds. 

To prescribe bounds, we first define `xlimits = np.array([[-0.05, 0.05]] * 10)`, where the design variables are organized by the first 8 entries corresponding to the FFD point displacements and the final two entries are for the far field velocity (second to last entry) and angle of attack (final entry). 

This initial setup uses a lower bound of `-0.05` to an upper bound of `0.05` for all 10 design variables. These bounds will work for most FFD points, aside the FFD points around the trailing edge of the airfoil. For the trailing edge, this displacement is too great and hence more restrictive bounds are applied to `xlimits[-3]` and `xlimits[-4]`. The far field velocity is a fixed value. However, [SMT](https://smt.readthedocs.io/en/latest/index.html) does not support design variables with equal upper and lower bounds. The easiest solution is to give an upper and lower bound which differ by only a small amount. This is done for the far field velocity via `xlimits[-2] = [10, 10 + 1e-9]`. Lastly, the angle of attack needs a different set of bounds which is set as `xlimits[-1] = [0, 3]`.

With the design variables and the design variable bounds being properly defined, we next define the objective function and constraint function for the lift coefficient, $C_{l} = 0.5$, and apply a weight to the constraint equation:

```python
objFunc = 'scenario1.aero_post.CD'
cons = 'scenario1.aero_post.CL'
conWeights = [10]
consEqs = ["x - 0.5"]
```

The names used for the objective function (`objFunc`) and constraint function(s) (`cons`) must match the naming convention used in `runScript.py`. `consWeights` is an array containing the weight(s) for the constraint function(s). A higher weight will strongly enforce the constraint, a lower weight will relax the constraint. The user should prescribe the weights according to how strict the constraint should be. The surrogate based optimization can handle multiple constraint functions but for this NACA0012 case, only one constraint function is needed. This is dissimilar to the gradient based optimizations for the NACA0012 airfoil; the surrogate based optimization for this case happens to naturally satisfy the thickness and volume constraints seen in the gradient based version of this case and hence those constraints are excluded in the current implementation. 

The `consEqs` is where the actual constraint function is defined. It is given as a string and must always be a function of `x`. Additionally, this should be defined as an equality constraint. Since we want to enforce that $C_{l} = 0.5$, we can rewrite this as $C_{l} - 0.5 = 0$ then replace $C_{l}$ with $x$ to get the constraint equation of $x - 0.5 = 0$.

The last step before running the optimization is to define the `surrogateOptions` dictionary and pass the dictionary to the `surrogateOptimization` class:

```python
surrogateOptions = {
    "optType"    : "constrained",  # constrained or unconstrained optimization
    "criterion"  : "EI",           # criterion for next evaluation point
    "iters"      : 20,             # num iterations to optimize function
    "numDOE"     : 10,             # number of sampling points
    "seed"       : 42,             # seed value to reproduce results
    "dvNames"    : dvNames,        # names of design variables
    "dvSizes"    : dvSizes,        # number of points for each design variable
    "dvBounds"   : xlimits,        # design variable bounds
    "objFunc"    : objFunc,        # objective function
    "cons"       : cons,           # quantity to constrain
    "conWeights" : conWeights,     # constraint weight
    "consEqs"    : consEqs,        # constraint equation(s)
}

surrogateOptimization(surrogateOptions , NACA0012)  # pass surrogateOptions and OpenMDAO model to surrogateOptimization class
```

The `surrogateOptions` dictionary defines various parameters for the optimization problem. Since this is a constrained optimization, `optType` is set to `constrained`. We use the Expected Improvement scheme (`EI`) as our evaluation `criterion`. The number of iterations (`iters`) is set to `20`. These are the iterations used to optimize the objective function. For this surrogate optimization we must also decide how many Design of Experiment (`numDOE`) points to use. A higher number will increase accuracy but will also increase run time. Too few points and the optimization will struggle to find the correct optimal point. It should be noted that the `numDOE` points are generated using a random number generator (RNG). To be able to reproduce results, a `seed` value is given. The final entries relate to the design variable definitions, objective function, and constraint definitions which were covered earlier in this section. Here we simply pass these values into the `surrogateOptions` dictionary.   


To run this case, first download the [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/NACA0012 and run the preProcessing.sh script to generate the mesh. Once that completes, run the optimization using the following command:

<pre>
mpirun -np 4 python runScript_SBO.py 2>&1 | tee logOpt.txt
</pre>

This case ran for 20 iterations, enhancing the total heat flux by 2.29% and decreasing pressure loss by 52.71%.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/CHT_ubend.gif" width="640" />

Fig. 2. Evolution of wall heat flux and velocity during the optimization

{% include links.html %}
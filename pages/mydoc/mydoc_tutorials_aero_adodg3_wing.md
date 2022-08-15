---
title: ADODG3 Wing
keywords: tutorial, adodg3
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_adodg3_wing.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the ADODG3 wing configuration.

<pre>
Case: Wing aerodynamic optimization 
Geometry: ADODG3 Wing
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.375
Design variables: xx FFD points, twist, and angle of attack for the shape-only case (total: 126).
Constraints: volume, thickness, LE/TE, and the lift coefficient (total number: 764)
Mach number: 0.3
Reynolds number: 0.22 million
Mesh cells: ~435,000
Solver: DARhoSimpleCFoam
</pre>

Fig. 1. Mesh and FFD points for the ADODG3 wing.

For the ADODG3 Wing configuration, we create three cases: a shape-only case using “runScript.py”, a planform case using “runScript_planform.py”, and a combined shape and planform case using “runScript_both.py”.

The shape-only case has the variables aoa, twist, and shape.<br>
The planform case has the variables aoa, taper, and span. <br>
The combined shape and planform case has all of the previous variables: aoa, twist, shape, taper, and span. <br>
The angle of attack was used consistently as a variable for all three cases in order to facilitate CFD convergence. 
<br>

The shape-only case has volume, thickness, LE/TE, and lift constraints.<br>
The planform case has only volume and lift constraints. The LE/TE and thickness constraints are redundant in the planform case.<br>
The combined shape and planform case has volume, thickness, LE/TE, and lift constraints. 

The runScripts are similar to the one used in the NACA0012 [incompressible case](mydoc_tutorials_naca0012_incompressible.html) with a few differences:

- Similarly to the [Onera M6 case,](mydoc_tutorials_aero_m6.html), we set FFD points to “nTwist” and do not change the root twist. 

  ```python
  def twist(val, geo):
      for i in range(1, nTwists):
          geo.rot_z["bodyAxis"].coef[i] = val[i - 1]
  ```
  
  We add the twist variable using the following function.

  ```python
  DVGeo.addGeoDVGlobal("twist", np.zeros(nTwists - 1), twist, lower=-10.0, upper=10.0, scale=1.0)
  daOptions["designVar"]["twist"] = {"designVarType": "FFD"}
  ```

- We add the function checkMeshThreshold in daOptions.
  ```python
   "checkMeshThreshold": {
        "maxAspectRatio": 3000.0,
        "maxNonOrth": 75.0,
        "maxSkewness": 6.0,
        "maxIncorrectlyOrientedFaces": 3, 
        }
   ```

- In daOptions, we add the function “primalMinResTolDiff” to adjust the convergence tolerance for the primal solver. 

  ```python
  "primalMinResTol": 1.0e-8,
  "primalMinResTolDiff": 1.0e4,
  ```
  
The value of primalMinResTolDiff is multiplied with the value of primalMinResTol to loosen the tolerances. 

<br>
To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/ADODG3_Wing and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The shape-only case ran for 49 steps and took about 11 hours with 320 cores on 4 Icelake nodes of [Stampede 2](https://portal.xsede.org/tacc-stampede2). According to "opt_SNOPT_summary.txt", the drag reduction was **8.79%**.
The planform case ran for 7 steps and took about 1 hour with 320 cores on 4 Icelake nodes of Stampede2. According to "opt_SNOPT_summary.txt", the drag reduction was **11.5%**.
The combined case ran for 100 steps and took about 12 hours with 320 cores on 4 Icelake nodes of Stampede 2. According to "opt_SNOPT_summary.txt", the drag reduction was **17.2%**.

The evolution of pressure and shape during the optimization is as follows.

![Movie_shapecase](https://user-images.githubusercontent.com/106775921/184717033-aba631c2-b29a-4c23-919c-474c5c8db5b2.gif)
Fig. 2. Pressure and shape evolution during the optimization process for the shape-only case

{% include links.html %}



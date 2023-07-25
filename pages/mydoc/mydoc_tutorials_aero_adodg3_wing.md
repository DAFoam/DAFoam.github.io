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
Design variables: 120 FFD points, twist, and angle of attack for the shape-only case (total: 126).
Constraints: volume, thickness, LE/TE, and the lift coefficient (total number: 764)
Mach number: 0.3
Reynolds number: 0.22 million
Mesh cells: ~435,000
Solver: DARhoSimpleCFoam
</pre>
![image](https://user-images.githubusercontent.com/106775921/184982881-66223c83-2e5b-46c3-b9da-33b5f99795d2.png)<br>
Fig. 1. Mesh and FFD points for the ADODG3 wing.

For the ADODG3 Wing configuration, we create three cases: a shape-only case using “runScript.py”, a planform case using “runScript_planform.py”, and a combined shape and planform case using “runScript_shape_planform.py”.

The shape-only case has the variables aoa, twist, and shape.<br>
The planform case has the variables aoa, taper, and span. <br>
The shape and planform case has all of the previous variables: aoa, twist, shape, taper, and span. <br>
The angle of attack is used consistently for all three cases to facilitate CFD convergence. We select "paralleltoFlow" in "objFunc" to specify the airflow direction, which requires the use of the aoa variable. 
<br>

The shape-only case has volume, thickness, LE/TE, and lift constraints.<br>
The planform case has only volume and lift constraints. The LE/TE and thickness constraints are redundant in the planform case.<br>
The shape and planform case has volume, thickness, LE/TE, and lift constraints. 

The "runScript.py" is similar to the one used in the NACA0012 [incompressible case](mydoc_tutorials_aero_naca0012_incompressible.html) with a few differences:

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

- We add the function "checkMeshThreshold" in daOptions to relax the mesh quality criteria.
  ```python
   "checkMeshThreshold": {
        "maxAspectRatio": 3000.0,
        "maxNonOrth": 75.0,
        "maxSkewness": 6.0,
        "maxIncorrectlyOrientedFaces": 3, 
        }
   ```

- In daOptions, we add the function “primalMinResTolDiff” to adjust the convergence tolerance for the primal solver. The value of "primalMinResTolDiff" is multiplied by the value of "primalMinResTol" to loosen the tolerances. 

  ```python
  "primalMinResTol": 1.0e-8,
  "primalMinResTolDiff": 1.0e4,
  ```
  
<br>
The "runScript_planform.py" is the same as the "runScript.py" but with only the aoa, taper, and span design variables. <br>
The "runScript_shape_planform.py" is similar to the "runScript.py" with the following differences:

- We add the function "adjStateOrdering" to ease the convergence of the adjoint equation.
  ```python
  "adjStateOrdering": "cell",
  ```

- We change the scaling factor "scaler" for all of the variables except for the angle of attack. This is done to control the relative step sizes of the design variables. We give the variables taper and span significance by scaling them up by a factor of 100 while reducing the impact of the shape variable by scaling it down by a factor of 10. 

  ```python
   self.add_design_var("twist", lower=-10.0, upper=10.0, scaler=0.1)
   self.add_design_var("span", lower=-30.0, upper=30.0, scaler=0.01)
   self.add_design_var("taper", lower=[0.0, -30.0], upper=30.0, scaler=0.01)
   self.add_design_var("shape", lower=-1.0, upper=1.0, scaler=10.0)
   self.add_design_var("aoa", lower=0.0, upper=10.0, scaler=1.0)
  ```
  
- As previously stated, the "runscript_shape_planform.py" adds the variables taper and span along with the variables contained in "runScript.py", twist, aoa, and shape. 

<br>
To run this case, first, download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/ADODG3_Wing and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

It is recommended to run this tutorial on an HPC. However, the following command can be used to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The shape-only case ran for 49 steps and took about 11 hours with 320 cores on 4 Icelake nodes of [Stampede 2](https://portal.xsede.org/tacc-stampede2). According to "opt_SNOPT_summary.txt", the drag reduction was **8.79%**. <br>
![Movie_shapecase](https://user-images.githubusercontent.com/106775921/184717033-aba631c2-b29a-4c23-919c-474c5c8db5b2.gif)
Fig. 2. Pressure and shape evolution during the optimization process for the shape-only case<br><br>

The planform case ran for 5 steps and took about 1 hour with 320 cores on 4 Icelake nodes of Stampede2. According to "opt_SNOPT_summary.txt", the drag reduction was **8.47%**. <br>
![movie_gif](https://user-images.githubusercontent.com/106775921/184983955-667beac1-ce20-4a17-8052-db14f946e8dc.gif)
Fig. 3. Pressure and shape evolution during the optimization process for the subsonic planform case<br><br>

The shape and planform case ran for 100 steps (exceeding the SNOPT iteration limit) and took about 12 hours with 320 cores on 4 Icelake nodes of Stampede 2. According to "opt_SNOPT_summary.txt", the drag reduction was **17.2%**. It is not recommended to run the case for more than 100 major iterations because of the minimal change in drag after iteration 100. 
![ezgif com-gif-maker](https://user-images.githubusercontent.com/106775921/185023313-5ddebf4c-0efb-431a-8216-a8e9adfe7a74.gif)
Fig. 4. Pressure and shape evolution during the optimization process for the subsonic shape and planform case

To generate the pressure and shape figure of the wing, first reconstruct the processor folders from the optimization into simpler timestamp folders using the following command. 
<pre>
reconstructPar
</pre>
Next, delete the processor folders.
<pre>
rm -r processor*
</pre>
Then, open Paraview and open the "paraview.foam" file. Make sure that the case type selected is "reconstructed", select "patch/wing" in Mesh Regions, and check the box that says "Camera Parallel Projection. Click "Apply" to view a colored pressure gradient on the ADODG3 Wing. For more details related to post-processing, refer to the [post-processing](mydoc_get_started_post_processing.html) page in Get Started.


The following is a transonic optimization of the same wing as above

<pre>
Lift coefficient (CL): 0.375
Mach number: 0.7
</pre>

The shape-only case ran for 103 steps and ran for 72 hours with 72 cores on the Nova HPC.  According to “opt_SNOPT_summary.txt”, the drag reduction was **17.4%**. <br>
![ezgif com-video-to-gif](https://github.com/DAFoam/DAFoam.github.io/assets/137945749/333d639a-6ec1-4e0b-aa55-488dff8595b2)

Fig. 5. Pressure and shape evolution during the optimization process for the transonic shape-only case<br><br>

The shape and planform case ran for 91 steps and ran for 48 hours with 72 cores on the Nova HPC. According to “opt_SNOPT_summary.txt”, the drag reduction was **25.4%**. <br>
![ezgif com-video-to-gif](https://github.com/DAFoam/DAFoam.github.io/assets/137945749/bf68b277-a5cc-43e9-a584-1b90d502b35e)

Fig. 6. Pressure and shape evolution during the optimization process for the transonic shape and planform case<br><br>

Over the iterations, it is possible to see shock waves as large differentiations in pressure can be seen on the ParaView post-processing images. In the transonic case, the drag reduction is much higher compared to the subsonic cases. This is due to the overall higher drag values that come from the higher Mach numbers, which leaves more room for optimization and drag reduction. 

{% include links.html %}

---
title: FAQ
keywords: new case, faq
summary:
sidebar: mydoc_sidebar
permalink: mydoc_get_started_faq.html
folder: mydoc
---

The following are some frequently asked questions (FAQ) for the NACA0012 airfoil and other tutorials. If you have more questions, please post them to [DAFoam Github Discussions](https://github.com/mdolab/dafoam/discussions).

## Where can I find all supported parameters and their default values for the daOption dictionary in runScript.py?

The documentation for all the supported parameters in daOption is available at [here](https://dafoam.github.io/doxygen/html/classdafoam_1_1pyDAFoam_1_1DAOPTION.html). Note that, we typically set essential parameters for daOption, and use the default values for other parameters. Their defaults values can be found in dafoam/pyDAFoam.py. In addition, all the values for daOption will be printed to the screen when the optimization runs.

## How to use a finer mesh?

To increase the mesh density, one needs to modify the parameters in "genAirFoilMesh.py". For example, changing "dX1PS = 0.005" to "dX1PS = 0.002" will increase the mesh density at the leading edge, changing "dXMaxPS = 0.02" to "dXMaxPS = 0.01" will increase the mesh density for the lower surface of the airfoil, changing "NpTE = 5" to "NpTE = 11" will use 11 mesh points for the blunt trailing edge. To change the mesh density in the marching direction, modify "NpExtrude" (number of layers to extrude), "yWall" (wall distance of the first layer mesh), "marchDist" (marching distance). Refer to [pyHyp](https://github.com/mdolab/pyhyp) for more details of the genAirFoilMesh.py script. 

## How to use more FFD points?

To increase the number of FFD points, one needs to increase "nx" (number of FFD points in the x direction) in "FFD/genFFD.py". Then run "python genFFD.py" in the FFD folder to generate a new "wingFFD.xyz" file. Note that the plot3D file we generate is a 3D mesh, and any internal points can be moved. Therefore, it is not necessary to use more than two points in the vertical (y) direction. Similarly, because it is a 2D case, there is no need to use more than two points in the z direction either. Also note that the "genFFD.py" script supports only uniform FFD points. We recommend using ICEM-CFD to generate more complex FFD points. 

## How to visualize the FFD points?

You can open a FFD file (*.xyz; plot3D format) in Paraview and choose "PLOT3D Reader" in the pop-up window. Then, on the left panel, uncheck "Binary File", check "Multi Grid", and then hit "Apply". NOTE: Paraview sometime crashes when loading Plot3D files with a small number of points (it is a bug in Paraview). To avoid this, you can convert a Plot3D file to the Tecplot format. First load the DAFoam environment, and run `dafoam_plot3d2tecplot.py yourFFDFileName.xyz newFFDFileName.dat`. Once done, a new file newFFDFileName.dat will be generated in the Tecplot format. You can then use Paraview to load this new file.

## How to use more CPU cores?

To run the optimization using 8 cores, first clean up previous results `./Allclean`, then run:

<pre>
./preProcessing.sh && mpirun -np 8 python runScript.py 2>&1 | tee optLog.txt
</pre>

## How to optimize a different airfoil?

To run optimization for a different airfoil, one needs to create two new files in the "profiles" folder and put the new airfoil x-y coordinates in these files. The airfoil data should be separated into upper and lower surfaces, they should start from the leading edge and ends at trailing edge. We use blunt trailing edge, so one needs to truncate the lower and upper surface data at about 99.8% of the chord. In other words, the profile data shouldn't end at x=1.0, delete a few points from the end. 

Once the new airfoil data are ready, modify the file names to load for "airfoilProfilePS" and "airfoilProfileSS" in "genAirFoilMesh.py". 

In addition, one may need to change the parameters for "corners" in FFD/genFFD.py to make sure the FFD points fully contains the new airfoil. Once done, in the "FFD" folder, run "python genFFD.py" to generate a new FFD file "wingFFD.xyz".

## How to change the flow conditions?

To run optimization at different flow conditions, one needs to modify the boundary condition values "U0", "p0", and "nuTilda0" from the "runScript.py". 

To run at a different lift coefficient, modify "CL_target", then run `mpirun -np 4 python runScript.py --task=solveCL`. Once the solveCL is done, note down the "alpha0" value that is printed to the screen, and replace the value in "runScript.py". 

This tutorial uses an incompressible flow solver DASimpleFoam, so the Mach number should be less than 0.1. For subsonic flow conditions (e.g., ~0.1 < M < ~0.6), refer to the settings in tutorials-master/NACA0012_Airfoil/subsonic. For the transonic flow conditions, refer to tutorials-master/NACA0012_Airfoil/transonic. Note that both runScript.py and the OpenFOAM configuration files (e.g., fvSchemes, fvSolution) are modified for these flow conditions.

## How to use different turbulence models?

To use the kOmegaSST or kEpsilon model, change the `RASModel` parameter to `kOmegaSST` or `kEpsilon` in constant/turbulenceProperties.

## How many CPU cores to use and how much memory does it need?

We recommend using one CPU core and reserve 2 GB memory per 10,000 cells. That being said, for a one million cell case, we recommend using 100 CPU cores and reserve 200 GB memory.

## How to extract the optimized geometry?

If you run the optimization in serial, load the OpenFOAM environment and run this:

<pre>
surfaceMeshTriangulate -patches '(wing)' -latestTime optShape.stl
</pre>

If you run the optimization in parallel using 4 cores, run this:

<pre>
mpirun -np 4 surfaceMeshTriangulate -patches '(wing)' -latestTime -parallel optShape.stl
</pre>

The above command will extract the patch "wing" to a stl file called "optShape.stl". If you have multiple patches to extract, modify the "-patches" flag, e.g., -patches '(wing body)'. Also, the "-lastTime" flag extracts stl files for the last optimization step. If you don't add the "-lastTime" flag, it will extract stl files for all optimization steps.

## Can I get the optimized geometry in a CAD format?

Yes, you can get the optimized geometry in the IGES format through pyGeo. Follow the "deformGeo" section from [here](https://dafoam.github.io/mydoc_tutorials_aero_prowim_wing.html). Refer to the [pyGeo documentation](https://mdolab-pygeo.readthedocs-hosted.com/en/latest/update_pygeo.html) for more general instructions on how to deform the design surface geometry.

## How to get sensitivity maps?

The latest version of DAFoam can output sensitivity maps during optimization. You need to set the names of the design variables to "writeSensMap" in runScript.py (check [this example](https://github.com/mdolab/dafoam/blob/c1c3ea12a49ceec7177238f7dc70a25ce260bba9/tests/runTests_DASimpleFoam.py#L46)). A more general description is [here](https://github.com/mdolab/dafoam/blob/c1c3ea12a49ceec7177238f7dc70a25ce260bba9/dafoam/pyDAFoam.py#L552). Now, we only support outputting sensitivity for FFD and Field designVarType.

## How to reduce the size of parallel optimization results?

When running in parallel, OpenFOAM will generate folders for each decomposed domain, e.g., processor0, processor1. This feature takes a lot of space and is slow to transfer and post-process. To fix this issue, wait until the parallel optimization is done, then go to the optimization folder, load the OpenFOAM environment, and run this command `reconstructPar` to combine all the decomposed flow fields that are stored in processor0, processor1, etc. You will see a bunch of new folders called 0.00000001, 0.00000002, etc. These are the combined flow solutions for each optimization step. So once the reconstructPar command is done, one can delete all the processor0, processor1, etc. folders. When visualizing the flow fields in Paraview, there is no need to choose "Decomposed Case" for "Case Type" because the cases have been reconstructed. This will increase the speed for visualization.  

## Does DAFoam support optimization for pure 2D problems?

No, DAFoam does **NOT** support pure 2D optimization. In OpenFOAM, there is an option to do pure 2D simulation, which is setting a patch type to **empty** in constant/polyMesh/boundary. This feature is **NOT** supported in DAFoam. So, one need to change the **empty** patch type to **symmetry** instead, and use one cell in the symmetry direction to mimic a 2D simulation. Refer to the case setup in the [NACA0012 case](https://github.com/DAFoam/tutorials/tree/master/NACA0012_Airfoil/incompressible).

## Can I use my own mesh?

Yes, DAFoam can run optimization with meshes generated by other software. Just put the mesh in constant/polyMesh. Then, you need to make sure the OpenFOAM configuration files are modified properly for the new mesh, e.g., change the patch name/type for the boundary conditions, change the fvSchemes and fvSolution. We suggest you run the built-in OpenFOAM solvers, e.g., simpleFoam, and make sure they run, before running a DAFoam optimization. Also, since you have generated your own meshes, there is NO need to run `./preProcessing.sh`.

## How to fix the "Primal solution failed for the baseline design!" error?

This error basically says the first primal solution does not converge to the prescribed tolerance (`primalMinResTol`, default 1e-8), so the optimization aborts. There are two ways to fix it. 1. Increase the primal tolerance `primalMinResTol`, or 2. Increase how much difference (`primalMinResTolDiff`, default 1e2) between the prescribed and actual tolerances is considered as a failed primal solution. By default, if the actual tolerance does not drop to at least two order of magnitude higher than the prescribed one, the primal solution is considered to be a failed one.

## Why the adjoint equation is not converging?

If your adjoint equation is not converging well. Try to use the following setup for daOptions in runScript.py

<pre>
"adjStateOrdering": "cell",
"adjEqnOption": {"gmresRelTol": 1.0e-6, "pcFillLevel": 1, "jacMatReOrdering": "natural", "gmresMaxIters": 2000, "gmresRestart": 2000},
</pre>

If the above options do not help, change `"pcFillLevel": 1` to `"pcFillLevel": 2`. NOTE: this will significantly increase the memory usage! If still not working, change `div(phi,U) bounded Gauss linearUpwindV grad(U);` to `div(phi,U) bounded Gauss upwind;` in system/fvSchemes and also check if the boundary conditions are properly assigned.

## Why do I keep getting failed mesh quality checks?

If you keep getting failed mesh checks throughout the optimization, first check if your baseline mesh quality passes. If yes, you may want to relax the mesh quality criteria, i.e., set `checkMeshThreshold` in daOption. Its default values are: 

<pre>
"checkMeshThreshold": {
    "maxAspectRatio": 1000.0,
    "maxNonOrth": 70.0,
    "maxSkewness": 4.0,
    "maxIncorrectlyOrientedFaces": 0,
},
</pre>

You need to increase these default values, e.g., set `"maxSkewness": 6.0,`. If you want to ignore just a few incorrectly oriented faces, set maxIncorrectlyOrientedFaces to be greater than 0. 

Another way to fix the issue is setting mesh quality constraints in optimization. Check the runScript_meshQualityConstraint.py script from the [UBend](https://github.com/DAFoam/tutorials/blob/master/UBend_Channel/runScript_meshQualityConstraint.py) tutorial.

## How to know the detailed description for a function's input parameters defined in runScript.py?

In runScript.py, we call multiple functions from other modules, e.g., pyGeo, IDWarp, pyOptSparse. To learn the detailed description for a function's input parameters, we take the function: `DVGeo.addGeoDVLocal` as an example. One can go to the `dafoam/packages/miniconda3/lib/python3.6/site-packages` directory and run this command `grep -r addGeoDVLocal *`. Then, one can find this function is defined in `pygeo/DVGeometry.py` with detailed description of its input parameters.

## What are the commands to start the DAFoam Docker image?

For your convenient, here are the commands for [Linux](mydoc_get_started_start_docker_linux.html), [MacOS](mydoc_get_started_start_docker_mac.html), and [Windows](mydoc_get_started_start_docker_windows.html).

## Why I keep getting a "Permission Denied" error when using the DAFoam Docker image?

If your OS system has more than one user, and you are not the first user and do not have admin access, you may get "Permission Denied" errors when using the DAFoam Docker image. The workaround is to run optimization in the Docker container. To this end, first, go to the optimization folder (e.g., NACA0012_Airfoil/incompressible), and then start the DAFoam docker container (use the commands for [Linux](mydoc_get_started_start_docker_linux.html), [MacOS](mydoc_get_started_start_docker_mac.html), and [Windows](mydoc_get_started_start_docker_windows.html)). Once in the docker container, switch to the root account by running `sudo su` and use `dafoamuser` as the password. Next, create a tmpRun folder in /home/dafoamuser and go there by running `mkdir /home/dafoamuser/tmpRun && cd /home/dafoamuser/tmpRun`. Now, copy all the optimization files from the mounted location to tmpRun and set the proper permission by running `cp -r /home/dafoamuser/mount/* /home/dafoamuser/tmpRun/ && chmod -R 777 /home/dafoamuser/tmpRun`. Next, exit the root account `exit`. Finally, we can go to tmpRun and run the optimization there `cd /home/dafoamuser/tmpRun && echo y | ./Allclean.sh && ./preProcessing.sh && mpirun -np 4 python runScript.py`. Once the job is done, switch to the root account `sudo su` and copy the tmpRun folder to the mounted location `cp -r /home/dafoamuser/tmpRun /home/dafoamuser/mount/`. NOTE: not doing this step will lose all the optimization results because the tmpRun folder will be deleted when exiting the docker container. After this, you can `exit` the docker container, and you should be able to see the tmpRun folder in your optimization folder (NACA0012_Airfoil/incompressible).

## How to run a multipoint optimization?

Refer to the tutorial tutorials-master/NACA0012_Airfoil/multipoint.

## How to run an optimization for 3D wings?

Refer to the tutorial tutorials-master/Onera_M6_Wing.

|


**NOTE:** Once the above modifications are done, go to the tutorial folder and clean up the previous optimization results.

<pre>
./Allclean
</pre>

Finally, generate the mesh and run the new optimization using 4 CPU cores:

<pre>
./preProcessing.sh && mpirun -np 4 python runScript.py 2>&1 | tee optLog.txt
</pre>

{% include links.html %}

## How to create a new objective function?

The objective functions for DAFoam are stored in the *src/adjoint/DAObjFunc* directory of [this repository](https://github.com/mdolab/dafoam). To create a new objective function, it is recommended to base it off of a similar existing function. You will need to first create yourObjFunc.H and yourObjFunc.C with your constructors, input/output definitions and implementation. 

Then, you will need to add the paths to the files you created in *src/adjoint/Make/files_Compressible* and *files_Incompressible*. At this point you can attempt to compile the project to test your code, follow [these instructions](https://dafoam.github.io/mydoc_installation_source.html) to build from source.

Finally, you will need to add the objective function to one of the runTests_*.py located in the *tests* directory. Again, use the other objective functions as an example. 

When making a pull request, the code coverage test will not pass unless the output from testing your objective function (the value itself and sensitivity values) is copied into the corresponding tests/refs/DAFoam_Test_*.txt file.
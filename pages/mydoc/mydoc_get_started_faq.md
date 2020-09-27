---
title: FAQ
keywords: new case, faq
summary:
sidebar: mydoc_sidebar
permalink: mydoc_get_started_faq.html
folder: mydoc
---

The following are the frequently asked questions (FAQ) for the NACA0012 airfoil tutorial. 

## How to use a finer mesh?

To increase the mesh density, one needs to modify the parameters in "genAirFoilMesh.py". For example, changing "dX1PS = 0.005" to "dX1PS = 0.002" will increase the mesh density at the leading edge, changing "dXMaxPS = 0.02" to "dXMaxPS = 0.01" will increase the mesh density for the lower surface of the airfoil, changing "NpTE = 5" to "NpTE = 11" will use 11 mesh points for the blunt trailing edge. To change the mesh density in the marching direction, modify "NpExtrude" (number of layers to extrude), "yWall" (wall distance of the first layer mesh), "marchDist" (marching distance). Refer to [pyHyp](https://github.com/mdolab/pyhyp) for more details of the genAirFoilMesh.py script. 

## How to use more FFD points?

To increase the number of FFD points, one needs to increase "nx" (number of FFD points in the x direction) in "FFD/genFFD.py". Then run "python genFFD.py" in the FFD folder to generate a new "wingFFD.xyz" file. Note that the plot3D file we generate is a 3D mesh, and any internal points can be moved. Therefore, it is not necessary to use more than two points in the vertical (y) direction. Similarly, because it is a 2D case, there is no need to use more than two points in the z direction either. Also note that the "genFFD.py" script supports only uniform FFD points. We recommend using ICEM-CFD to generate more complex FFD points. 

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

## How to use a different turbulence model?

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

## How to run a multipoint optimization?

Refer to the tutorial tutorials-master/NACA0012_Airfoil/multipoint.

## How to run an optimization for 3D wings?

Refer to the tutorial tutorials-master/Onera_M6_Wing.

|


**NOTE:** Once the above modifications are done, go to the tutorial folder and load the DAFoam image:

<pre>
docker run -it --rm -u dafoamuser --mount "type=bind,src=$(pwd),target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash
</pre>

Then clean up the previous optimization results.

<pre>
./Allclean
</pre>

Finally, generate the mesh and run the new optimization using 4 CPU cores:

<pre>
./preProcessing.sh && mpirun -np 4 python runScript.py 2>&1 | tee optLog.txt
</pre>

{% include links.html %}

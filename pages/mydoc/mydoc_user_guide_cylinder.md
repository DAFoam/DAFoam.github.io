---
title: Cylinder - unsteady aerodynamic shape optimization
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: user-guide-cylinder.html
folder: mydoc
---

This chapter was written by [Zilong Li](https://github.com//zilonglicfd) and reviewed by [Ping He](https://github.com/friedenhe).

## Learning Objectives:

After reading this chapter, you should be able to:

- Setup unsteady aerodynamic shape optimizations

## Overview of the Cylinder - unsteady aerodynamic shape optimization

The following is an unsteady aerodynamic shape optimization case for a cylinder
<pre>
Case: Unsteady flow over a cylinder
Geometry: Cylinder
Objective function: Time-averaged CD
Design variables: 16 FFD points moving in the x direction
Constraints: Cylinder volume does not decrease; FFD symmetry wrt z=0 and y=0
Inlet velocity: 10 m/s
Mesh cells: 2450
Solver: DAPimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Cylinder_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the Cylinder case

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/Cylinder_Unsteady and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Follow similar steps as in the NACA0012 airfoil case, We use the pyHyp package to generate the mesh. After the mesh generation is done, we are ready to run the simulation. Because in this case we run the unsteady aerodyanmic shape optimization, we need to first run the steady simulation to prepare the initial flow fields for the unsteady optimization. We use the simpleFoam solver to run the steady simulation and reconstruct the flow fields. As a side note, in this case we run the potentialFoam solver to generate the initial flow fields for the simpleFoam.

```bash
# run simpleFoam
cp -r system/controlDict_simple system/controlDict
cp -r system/fvSchemes_simple system/fvSchemes
cp -r system/fvSolution_simple system/fvSolution
potentialFoam
mpirun -np 4 python runPrimalSimple.py

# reconstruct the simpleFoam fields
reconstructPar
rm -rf processor*
rm -rf 0
mv 500 0
rm -rf 0/uniform 0/polyMesh
```

After the simpleFoam is done, we run the pimpleFoam primal to get equilibrium initial fields.

```bash
# run the pimpleFoam primal to get equilibrium initial fields
cp -r system/controlDict_pimple_long system/controlDict
cp -r system/fvSchemes_pimple system/fvSchemes
cp -r system/fvSolution_pimple system/fvSolution
mpirun -np 4 python runScript.py -task=run_model
reconstructPar -latestTime
rm -rf processor*
rm -rf 0
mv 10 0
rm -rf 0/uniform 0/polyMesh
cp -r system/controlDict_pimple system/controlDict
```

We recommend running this case with 4 CPU cores:

<pre>
mpirun -np 4 python runScript_v2.py 2>&1 | tee logOpt.txt
</pre>

We ran this case using the SNOPT optimizer. The case ran for 14 major iterations and took about 10 hours. According to “opt_snopt_summary.txt”, the initial CD is 6.5587285E-01 and the optimized CD is 5.3605074E-01 with a percentage decrease of **18%**.
Comparison of the unsteady velocity animation and CD time series between the baseline and optimized designs are shown as follows.

|

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Cylinder_TimeSeriesCD.png" width="640" />

Fig. 2. Time-series of CD for the baseline and optimized design

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Cylinder_U.gif" width="640" />

Fig. 3. Animation of velocity contours for the baseline (left) and optimized (right) designs.
 

{% include links.html %}

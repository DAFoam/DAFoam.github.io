---
title: pitzDaily 
keywords: tutorial, pitzDaily
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_topo_pitzdaily.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a density-based topology optimization case for the pitzDaily case in OpenFOAM. 

<pre>
Case: pitzDaily topology optimization 
Geometry: pitzDaily channel
Objective function: Total pressure loss
Design variables: 12,225 alpha porosity values in the flow field
Constraints: None
Mach number: 0.12 (40 m/s)
Reynolds number: 0.13 million
Mesh cells: ~12,225
Solver: DASimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/pitzDaily_topo_opt.gif" width="640" />

Fig. 1. Velocity and alpha porosity evolution during the optimization.

|

The "runScript.py" for a topology optimization is similar to the one used for shape optimization. In other words, we still need to specify a dummy design surface (although we will not move it)

<pre>
"designSurfaces": ["upperWall"],
</pre>

And we need to create a dummy FFD box to cover the dummy design surface and load it to DVGeo,

<pre>
DVGeo = DVGeometry("./FFD/dummyFFD.xyz")
</pre>

We also need to specify set up a dummy reference axis to make sure we can use global design variable (alpha porosity field)

<pre>
DVGeo.addRefAxis("dummyAxis", xFraction=0.25, alignIndex="k")
</pre>

Other notes:

- This case only works with the **SNOPT** optimizer at this moment.

- We need to specify the total number of cells "nCells".

- We need to choose the Jacobian free option in daOptions: "adjJacobianOption": "JacobianFree". This means that we need to compile the AD version of OpenFOAM and DAFoam (see [here](https://dafoam.github.io/mydoc_installation_source.html#compile-dafoam-with-automatic-differentiation-optional)). If you use the Docker image, they have been compiled so no additional action is needed.

- We need to properly scale the design variable because the alpha porosity field could be very large, e.g., 1e4. So we use "scale=1e-4" in DVGeo.addGeoDVVGlobal("alphaPorosity", ...).

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/pitzDaily and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The case ran for 36 steps and took about 2 hours using Intel 3.0 GHz CPU with 4 cores. According to "logOpt.txt" and "opt_SNOPT_summary.txt", the initial pressure loss is 0.28228 and the optimized drag is 0.16579 with a pressure-loss reduction of **41.3%**. 

{% include links.html %}

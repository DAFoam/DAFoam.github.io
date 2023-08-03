---
title: NREL6 wind turbine
keywords: tutorial, nrel6
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_nrel6.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the NREL6 wind turbine blades.
<pre>
Case: Wind turbine aerodynamic optimization
Geometry: NREL6
Objective function: Torque
Design variables: 100 FFD points moving in the x and y directions
Constraints: None
Inlet velocity: 7 m/s
Rotation speed: 7.5 rad/s
Mesh cells: 800 K
Solver: DATurboFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/NREL6_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the NREL6 case

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/NREL6_Wind_Turbine and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

We recommend running this case on an HPC system with 80 CPU cores:

<pre>
mpirun -np 80 python runScript.py 2>&1 | tee logOpt.txt
</pre>

{% include links.html %}

The case ran for 82 major iterations and took about 33 hours using HPC with 72 cores. According to “opt_snopt_summary.txt”, the initial torque is 6.7699821E+02 and the optimized torque is 1.2347349E+03 with a percentage increase of **82%**.
The evolution of pressure and shape during the optimization is as follows.

![ezgif com-gif-maker (1)](https://github.com/DAFoam/DAFoam.github.io/assets/140402482/5fbec539-8e65-4328-8e1d-a48f7c17f766)


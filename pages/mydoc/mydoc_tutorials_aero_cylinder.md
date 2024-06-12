---
title: Cylinder (unsteady flow)
keywords: tutorial, cylinder
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_cylinder.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an unsteady aerodynamic shape optimization case for a cylinder
<pre>
Case: Unsteady flow over a cylinder
Geometry: Cylinder
Objective function: CD
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
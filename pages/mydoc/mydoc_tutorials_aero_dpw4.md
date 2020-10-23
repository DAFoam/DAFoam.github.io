---
title: DPW4 aircraft
keywords: tutorial, dpw4
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_dpw4.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the DPW4 aircraft (wing-body-tail configuration) at transonic conditions.

<pre>
Case: Aircraft aerodynamic optimization
Geometry: CRM wing, body, and tail
Objective function: Drag coefficient
Design variables: 216 FFD points moving in the z direction, 9 wing twists, one tail rotation, one angle of attack
Constraints: Volume, thickness, LE/TE, and lift constraints (total number: 771)
Mach number: 0.85
Reynolds number: 5 million
Mesh cells: 860 K
Solver: DARhoSimpleCFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/DPW4_FFD.svg" width="500" />

Fig. 1. Mesh and FFD points for the DPW4 wing-body-tail configuration

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/DPW4_Aircraft and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

We recommend running this case on an HPC system with 100 CPU cores:

<pre>
mpirun -np 100 python runScript.py 2>&1 | tee logOpt.txt
</pre>


{% include links.html %}

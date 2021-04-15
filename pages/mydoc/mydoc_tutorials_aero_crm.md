---
title: Common research model (CRM) wing
keywords: tutorial, crm
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_crm.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the common research model (CRM) wing at transonic condition.

<pre>
Case: Wing aerodynamic optimization 
Geometry: CRM wing
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.5
Design variables: 192 FFD points moving in the z direction, seven twists, and one angle of attack.
Constraints: volume, thickness, LE/TE, and lift constraints (total number: 768)
Mach number: 0.85
Reynolds number: 5 million
Mesh cells: ~579K
Solver: DARhoSimpleCFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/CRM_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the CRM wing.

|

The "runScript.py" is similar to that used in the [Onera M6 wing](mydoc_tutorials_aero_m6.html).

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/CRM_Wing and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization (we recommend using 64 cores):

<pre>
mpirun -np 64 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The case ran for 160 optimization iterations, the original CD was 0.02090 and the optimized CD was 0.01932 (7.6% drag reduction).

The evolution of pressure and shape during the optimization is as follows.

|

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/CRM_Movie.gif" width="640" />

Fig. 2. Pressure and shape evolution during the optimization process

{% include links.html %}

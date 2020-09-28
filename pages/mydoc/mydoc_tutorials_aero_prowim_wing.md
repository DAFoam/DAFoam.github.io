---
title: Prowim wing
keywords: tutorial, prowim
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_prowim_wing.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the Prowim wing-propeller configuration. Refer to [this paper](https://arc.aiaa.org/doi/10.2514/6.2020-1764) for more simulations and optimization results.

<pre>
Case: Wing-propeller aerodynamic optimization
Geometry: Prowim wing
Objective function: Drag
Design variables: 120 FFD points moving in the y direction
Constraints: Volume, thickness, and lift
Propeller model: Actuator disk
Mach number: 0.3
Mesh cells: 190 K
Adjoint solver: DARhoSimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Prowim_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the Prowim wing-propeller case

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/Prowim_Wing_Propeller and run this command to start the DAFoam docker container.

<pre>
docker run -it --rm -u dafoamuser --mount "type=bind,src=$(pwd),target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash
</pre>

**Now you are on the DAFoam Docker container**, run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

We recommend running this case on an HPC system with 20 CPU cores:

<pre>
mpirun -np 20 python runScript.py 2>&1 | tee logOpt.txt
</pre>

{% include links.html %}

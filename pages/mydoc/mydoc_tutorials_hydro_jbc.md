---
title: JBC bulk carrier hull
keywords: tutorial, jbc
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_hydro_jbc.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a hydrodynamic optimization for the JBC bulk carrier hull.

<pre>
Case: Ship hydrodynamic optimization with self-propulsion
Geometry: Japan Bulk Carrier (JBC) hull
Objective function: Weighted drag and wake distortion
Design variables: 32 FFD points moving in the y direction
Constraints: Volume, thickness, symmetry, and curvature constraints (total number: 83)
Mach number: less than 0.01
Reynolds number: 7.5 million
Mesh cells: 40K
Solver: DASimpleFoam
</pre>

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/JBC_Hull and run this command to start the DAFoam docker container.

<pre>
docker run -it --rm -u dafoamuser --mount "type=bind,src=$(pwd),target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash
</pre>

**Now you are on the DAFoam Docker container**, run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 8 CPU cores:

<pre>
mpirun -np 8 python runScript.py 2>&1 | tee logOpt.txt
</pre>

{% include links.html %}

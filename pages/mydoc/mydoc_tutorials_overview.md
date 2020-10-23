---
title: Overview
keywords: tutorial, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_overview.html
folder: mydoc
---

DAFoam supports high-fidelity design optimization for a wide range of disciplines, e.g., aerodynamics, heat transfer, solid mechanics, and hydrodynamics. 

The optimization configurations for the DAFoam tutorials are available from [here](http://github.com/dafoam/tutorials). If you use the DAFoam Docker image, first start a Docker container, refer to [this page](mydoc_get_started_run.html). Then, for most of the tutorials, run this command for pre-processing:

<pre>
./preProcessing.sh
</pre>

Then, use this command to run the tutorial:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

Check the instructions in each tutorial for details.

{% include links.html %}

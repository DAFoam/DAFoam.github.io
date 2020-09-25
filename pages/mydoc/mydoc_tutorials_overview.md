---
title: Overview
keywords: tutorial, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_overview.html
folder: mydoc
---

DAFoam supports high-fidelity design optimization for a wide range of disciplines, e.g., aerodynamics, heat transfer, structure, and hydrodynamics. 

The case setup for the DAFoam tutorials are hosted on [Github](http://github.com/dafoam/tutorials). For most of the tutorials, run this command for pre-processing:

<pre>
./preProcessing.sh
</pre>

Then, use this command to run the tutorial:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

Check the instructions in each tutorial for details.

{% include links.html %}

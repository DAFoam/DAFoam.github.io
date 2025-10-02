---
title: Conjugate heat transfer topology optimization of a channel  
keywords: tutorial, channel
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_topo_channel_cht.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a conjugate heat transfer topology optimization setup for a channel. 

<pre>
Case: Conjugate heat transfer topology optimization 
Geometry: A square channel
Objective function: Weighted total pressure loss and outlet temperature 
Design variables: 6400 porosity values in the flow field
Constraints: None
Reynolds number: 1000 (laminar flow)
Mesh cells: 6400
Solver: DATopoChtFoam
</pre>

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/Channel_TopoCHT and run the "preProcessing.sh" script to generate the mesh and set a boundary layer profile at the inlet:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The case ran for 21 steps and took about one hour using Intel 3.0 GHz CPU with 4 cores. According to "logOpt.txt" and "opt_SNOPT_summary.txt", the initial and final objective functions are -2.417 and -5.121 with a reduction of **111.9%**. 

The following are the animations of the optimization. Notes: The **SNOPT** optimizer works better than **IPOPT** for this case.


<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/TopoCHT_U.gif" style="width:300px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/TopoCHT_alpha.gif" style="width:300px !important;" />

Fig. 1. Velocity and alpha porosity evolution during the optimization.

{% include links.html %}

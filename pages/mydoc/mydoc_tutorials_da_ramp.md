---
title: Data assimilation to find inlet velocity field 
keywords: tutorial, ramp
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_da_ramp.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a data-assimilation optimization case where we try to find the inlet velocity field based on pressure data on the bottom wall.

<pre>
Case: Data assimilation optimization 
Geometry: Ramp
Objective function: Regularized pressure prediction errors on the bottom wall
Design variables: Velocity profile at the inlet
Constraints: None
Reynolds number: ~1 million
Mesh cells: 5000
Solver: DASimpleFoam
</pre>

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/Ramp_DA/steady and run the "preProcessing.sh" script to generate the training data.

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The case ran for 18 steps and took about 15 mins using Intel 3.0 GHz CPU with 4 cores. According to "logOpt.txt" and "opt_SNOPT_summary.txt", the initial and optimized objective functions are 5.2079934E+01 and 1.3298352E+00 with one order of reduction. 

The animations of the optimization are as follows. We can see that the overall velocity and pressure fields agree with the reference, but there are some velocity oscillations at the inlet. We may need to tweak the regularization term "UVar" to improve the results.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Ramp_DA_U.gif" style="width:500px !important;" />

Fig. 1. Velocity contour evolution during the optimization.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Ramp_DA_U_in.gif" style="width:500px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Ramp_DA_p_bot.gif" style="width:500px !important;" />

Fig. 2. Inlet velocity and bottom wall pressure distributions during the optimization.

{% include links.html %}

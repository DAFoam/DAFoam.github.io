---
title: Data assimilation to velocity magnitude and angle of attack
keywords: tutorial, ramp
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_da_naca0012.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a data-assimilation optimization case where we try to find the velocity magnitude and angle of attack based on pressure data on the NACA0012 airfoil.

<pre>
Case: Data assimilation optimization 
Geometry: NACA0012
Objective function: Pressure prediction errors on the airfoil
Design variables: Velocity magnitude and angle of attack at the far field
Constraints: None
Reynolds number: 0.6667 million
Mesh cells: 4000
Solver: DASimpleFoam
</pre>

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/NACA0012_DA and run the "preProcessing.sh" script to generate the training data.

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The case ran for 11 steps and took about 5 mins using Intel 3.0 GHz CPU with 4 cores. According to "logOpt.txt" and "opt_IPOPT.txt", the initial and optimized objective functions are 7.3338354e+00 and 4.9991657e-13 with 13 order of reduction. 

The animations of the optimization are as follows. We can see that the overall pressure profile agree well with the reference

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/NACA0012_DA_p.gif" style="width:500px !important;" />

Fig. 1.Pressure contour evolution during the optimization.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/NACA0012_DA_p_profile.gif" style="width:500px !important;" />

Fig. 2. Wall pressure distributions during the optimization.

{% include links.html %}

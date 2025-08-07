---
title: UAV Propeller 
keywords: tutorial, uav propeller
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aerostruct_uav_prop.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerostructural shape optimization case for the UAV propeller in hover. The baseline design is an untwisted, untapered NACA 0012 propeller blade. The flow is solved using the DARhoSimpleFoam CFD solver and the structure is solved using an open-source FEM solver [TACS](https://github.com/smdogroup/tacs). The load and displacement transfer is computed using [FUNtoFEM](https://github.com/smdogroup/funtofem). The aerostructural coupling is implemented in the [OpenMDAO/Mphys](https://github.com/OpenMDAO/mphys) framework.

<pre>
Case: Propeller aerostructural optimization 
Geometry: NACA 0012 UAV Propeller 
Objective function: Shaft Power Coefficient
Design variables: 6 twist variables, 72 shape variables, 6 chord variables, rotation speed
Constraints: Thrust coefficient, propeller thickness, propeller spanwise curvature, leading edge, and mass
RPM: 5000
Reynolds number: 180 thousand
Mesh cells: ~1.5 million
Solver: DARhoSimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AeroStruct_Propeller_Mesh" style="width:500px !important;" />

Figure 1. Simulation domain, propeller meshes, and FFD points. The blue and red squares are the FFD points. Only the blue FFD points move during the optimization.

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/UAV_Prop and run the “preProcessing.sh” script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the code below to run the optimization usign 144 CPU cores:
  
<pre>
mpirun -np 144 python runScript_AeroStruct.py 2>&1 | tee logOpt.txt
</pre>

The case in this tutorial ran for 42 iterations, and the optimality dropped by one order of magnitude. In total, we saw an 18.3% reduction in power, while the thrust, mass, and stress constraints were met. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/UAV_Prop_Baseline_Optimized_Design" style="width:500px !important;" />

Figure 2. Comparison of the baseline and optimized designs for case where twist, shape, and chord are design variables. 

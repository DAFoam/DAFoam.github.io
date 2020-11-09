---
title: Plate hole
keywords: tutorial, platehole
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_struct_platehole.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a structural optimization case for a plate with a hole in the middle.

<pre>
Case: Structural optimization for the plate hole configuration
Geometry: Plate hole
Objective function: Weight
Design variables: 24 FFD points moving in the x and y directions
Constraints: Symmetry constraint (total number: 18), max stress constraint
Mesh cells: 4 K
Solver: DASolidDisplacementFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Plate_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the plate hole case

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/PlateHole_Structure and  run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 1 CPU cores:

<pre>
python runScript.py 2>&1 | tee logOpt.txt
</pre>

{% include links.html %}

After conducting the optimization, use ParaView to ensure the simulation has been completed successfully. There should be 10 geometry iterations which minimize mass while preserving the original maximum stress.

![Stress Results at Original Case](https://user-images.githubusercontent.com/59976472/98586637-9aa2e800-228e-11eb-8304-08567d892c6e.png)

Fig. 2. Stress results and distribution before optimization

|

![Stress Results after Optimization](https://user-images.githubusercontent.com/59976472/98587972-8fe95280-2290-11eb-8fad-ba6200757ff0.png)

Fig. 3. Stress results and distribution after optimization

|

As you can see, the optimization eliminates material to reduce component weight while preserving the maximum stress. The mass is reduced from 11950 to 10701, or a reduction of mass by 10.5 percent. This can be seen in the logOpt.txt output file.

We have gone further to compare the simulation results from OpenFoam to the results from a numerical solution for a plate hole case and the same simulation executed in an established software ANSYS. The results are shown below in the figures below.

![Stress Equation Plate Hole](https://user-images.githubusercontent.com/59976472/98589909-a2b15680-2293-11eb-8cc9-bbacf0c1f426.png)

Fig. 4. Stress equation for a plate hole

|

This equation assumes the plate has infinite width, which causes some discrepancy near the edge of the plate. The maximum case for this equation occurs at +90 deg and -90 deg.

![ANSYS Stress Results at Original Case](https://user-images.githubusercontent.com/59976472/98591511-f58c0d80-2295-11eb-9a2d-3d0cd8253413.png)

Fig. 5. ANSYS stress results and distribution before optimization with mesh

|

It was not possible to use the exact constraints as ANSYS would display an error that it was under constrained, so the setup is shown in figure 6.

![ANSYS Setup](https://user-images.githubusercontent.com/59976472/98592486-697ae580-2297-11eb-83ff-6c9b788de3e0.png)

Fig. 6. ANSYS setup

|

Next, by exporting the stress along the +90 deg and -90 deg boundary, the three methods for stress evaluation can be compared.

![ParaView Slice](https://user-images.githubusercontent.com/59976472/98592650-a515af80-2297-11eb-9daf-26a74d3bfa3a.png)

Fig. 7. ParaView maximum stress boundary

|



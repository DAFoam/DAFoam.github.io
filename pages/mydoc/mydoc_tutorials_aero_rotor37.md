---
title: Rotor 37 compressor
keywords: tutorial, rotor37
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_rotor37.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the Rotor37 axial compressor rotor.

<pre>
Case: Axial compressor aerodynamic optimization at transonic conditions
Geometry: Rotor37
Objective function: Torque
Design variables: 50 FFD points moving in the y and z directions
Constraints: Constant mass flow rate and total pressure ratio
Rotation speed: 1800 rad/s
Mesh cells: 40 K
Adjoint solver: DATurboFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Rotor37_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the Rotor37 case

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/Rotor37_Compressor and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

Post Procesing:

Use the following command to load the OpenFOAM environment:

<pre>
of1812
</pre>

Next, run the following command:

<pre>
reconstructPar
</pre>

This will generate new folders and allow the deletion of all of the processor folders. This makes the entire directory a bit smaller and allow for easier processing.

Open the paraview.foam file in the ParaView application. Check the boxes next to blade and hub and uncheck the box next to mesh. After hitting apply, the blade will appear on the viewer. This will show the pressure gradient by default. There is a play button at the top of the window that will show all iterations through each timestep of the optimization. The original blade should look like figure 2 and figure 3 as the top and bottom, respectively.

![toporig](https://user-images.githubusercontent.com/31484354/113370066-8ab49f00-9328-11eb-9478-ae013ae7da3d.png)
Fig. 2. Pressure gradient on the top of the original blade

![bottomorig](https://user-images.githubusercontent.com/31484354/113370100-a5871380-9328-11eb-8552-bf57fe0e0b23.png)
Fig. 3. Pressure gradient on the bottom of the orignal blade

After optimizaiton, the pressure gradients should look as follows:

![topopt](https://user-images.githubusercontent.com/31484354/113370157-c8b1c300-9328-11eb-95b3-eac575498a77.png)
Fig. 4. Pressure gradient on the top of the optimized blade

![bottomopt](https://user-images.githubusercontent.com/31484354/113370193-d6674880-9328-11eb-852a-d7422aba9bfe.png)
Fig. 5. Pressure gradient on the bottom of the optimized blade

After this, the blade can be sliced using a cylindrical slice. The slices allow the profile of the blade to be viewed. Figures 6 and 7 show a comparison of the original blade vs the optimized blade at the root and at the tip.

![rootshapes](https://user-images.githubusercontent.com/31484354/113370809-71aced80-932a-11eb-8fb6-5cb994733838.png)
Fig. 6. The original airfoil and the optimized airfoil at the root

![tipshapes](https://user-images.githubusercontent.com/31484354/113370885-9903ba80-932a-11eb-9229-b813b4670eb6.png)
Fig. 7. The original airofil and the optimized airfoil at the tip

On each slice, use the "Plot on sorted lines" filter to achieve a graph of the pressure distribution accross the airfoil. Figures 8 and 9 show overlayed plots of the orignal shape and the optimized shape at the root and at the tip.

![rootpresdist](https://user-images.githubusercontent.com/31484354/113370487-9ce30d00-9329-11eb-9c25-70a90158b201.png)
Fig. 8. Overlayed plot of pressure distribution at the root

![tippresdist](https://user-images.githubusercontent.com/31484354/113370572-d3208c80-9329-11eb-902d-53af8f0bcd22.png)
Fig. 9. Overlayed plot of pressure distribution at the tip

To see the Mach gradiant, check the box next to mesh and uncheck the blade and hub. The slice will update to show the mesh. This will need to be coppied 4 or 5 more times, with each slice being translated up by 10&deg;. A calculator needs to be put onto each slice to calculate the Mach number. The Mach number can then be selected to view instead of the pressure. Figures 10 and 11 show the Mach gradients for both the original and optimized cases at the root and at the tip.

![rootgradient](https://user-images.githubusercontent.com/31484354/113371581-53e08800-932c-11eb-86ea-e8f8e4ddde40.png)
Fig. 10. Mach gradient at root, left is original and right is optimized

![tipgradient](https://user-images.githubusercontent.com/31484354/113371709-a0c45e80-932c-11eb-9df0-1d383c6b57b2.png)
Fig. 11. Mach gradient at tip, left is orignal and right is optimized

{% include links.html %}

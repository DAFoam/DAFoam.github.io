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
Objective function: Drag
Design variables: 32 FFD points moving in the y direction
Constraints: Volume, thickness, symmetry, and curvature constraints (total number: 83)
Mach number: less than 0.01
Reynolds number: 7.5 million
Mesh cells: 265 K
Solver: DASimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/JBC_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the JBC hull

|

To avoid wave shapes, this case impose a curvature constraint to the hull shape. The aggregated curvature (approximated max-curvature) in the optimized design is constrained to be less than 1.2 times of the curvature in the baseline design. See the following code to add the curvature constraint. Here the "hullCurv.xyz" file is a 2D surface mesh that define which area the curvature constraint is applied to. This surface mesh should be as close as possible to the hull shape. Then, pyGeo will load in this surface mesh in the FFD box and deform it along with the hull. This way, the curvature of this 2D surface mesh is the curvature of the hull.

<pre>
# Curvature constraints
DVCon.addCurvatureConstraint(
    "./FFD/hullCurv.xyz", curvatureType="KSmean", lower=0.0, upper=1.21, addToPyOpt=True, scaled=True
)
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/JBC_curvature.png" width="500" />

Fig. 2. Example of adding curvature constraint. The red mesh is the 2D surface mesh defined hullCurv.xyz.

This case requires the IPOPT optimizer and the AD version of DAFoam. To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/JBC_Hull and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

We recommend running this case on an HPC system with 30 CPU cores:

<pre>
mpirun -np 30 python runScript.py 2>&1 | tee logOpt.txt
</pre>

This case ran for 40 steps. The drag reduces by 2.1%. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/JBC_movie.gif" width="640" />

Fig. 3. Evolution of hull shape and pressure distribution during the optimization.

{% include links.html %}

---
title: NACA0012 airfoil (incompressible)
keywords: tutorial, NACA0012
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_naca0012_incompressible.html
folder: mydoc
---

{% include note.html content="This is the tutorial used in [Get started](mydoc_get_started_download_docker.html)." %}

The following is an aerodynamic shape optimization case for the NACA0012 airfoil at low speed.

<pre>
Case: Airfoil aerodynamic optimization 
Geometry: NACA0012
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.5
Design variables: 20 free-form deformation (FFD) points moving in the y direction, one angle of attack
Constraints: Symmetry, volume, thickness, and lift constraints (total number: 34)
Mach number: 0.02941 (10 m/s)
Reynolds number: 0.6667 million
Mesh cells: ~4,000
Solver: DASimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/NACA0012_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the NACA0012 airfoil

|

The evoluation of pressure and shape during the optimization is as follows. Refer to [this page](mydoc_get_started_post_processing.html) for post-processing the optimization results.

|

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Paraview_Movie.gif" width="640" />

Fig. 2. Pressure and shape evolution during the optimization process


{% include links.html %}

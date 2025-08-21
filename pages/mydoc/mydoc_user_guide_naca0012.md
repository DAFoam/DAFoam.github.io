---
title: NACA0012 airfoil - 2D aerodynamic shape optimization
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_naca0012.html
folder: mydoc
---

## Overview 

The following is an aerodynamic shape optimization case for the NACA0012 airfoil at low speed:

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

## FFD points

## Mesh generation through pyHyp

## preProcess

## runScript


{% include links.html %}

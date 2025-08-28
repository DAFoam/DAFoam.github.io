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

Below is the file and directory structure for the incompressible NACA0012 airfoil case in the DAFoam tutorial. We will explain in detail the files and directories that are unique to DAFoam.

```bash
NACA0012_Airfoil/incompressible
|-- 0.orig            # initial fields and boundary conditions (OpenFOAM essentials)
|-- FFD               # generate the FFD points
|-- constant          # flow and turbulence property definition (OpenFOAM essentials)
|-- profiles          # NACA0012 profile coordinate for mesh generation
|-- system            # flow discretization, setup, time step, etc (OpenFOAM essentials)
|-- Allclean.sh       # script to clean up the simulation and optimization results
|-- preProcessing.sh  # generate mesh, copy the initial and boundary conditions to 0
|-- genAirFoilMesh.py # mesh generation script called by preProcessing.sh
|-- paraview.foam     # dummy file for paraview post-processing
|-- runScript.py      # main run script for DAFoam
```

## 0.orig

The 0.orig directory contains the initial condition for a DAFoam case. The preProcessing.sh script duplicates it as the 0 directory, and then it functions the same way as in OpenFoam.

## FFD points

We use the free-form deformation (FFD) points to parameterize the design surface geometry and deform it during the optimization process. The FFD volume should completely contain the design surface (see the red dots in Fig.1).

Under the FFD directory, the FFD file wingFFD.xyz contains the coordinates of the FFD points, and is generated from running genFFD.py. 

To change the FFD points, we need to change some parameters in genFFD.py and rerun it. Below we explain genFFD.py in detail.

<!-- 
def writeFFDFile, no need to change
def returnBlockPoints, no need to change
nBlocks = 1
Change nx, ny, nz,
Corners are the FFD block coordinates
-->

## Mesh generation through pyHyp

## preProcess

## runScript


{% include links.html %}

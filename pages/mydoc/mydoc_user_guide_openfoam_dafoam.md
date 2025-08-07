---
title: OpenFOAM and DAFoam Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openfoam_dafoam.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## 1. Overview of DAFoam and OpenFOAM

### 1.1 What is DAFoam?
DAFoam (Discrete Adjoint with OpenFOAM) is a high-fidelity multidisciplinary design optimization and analysis framework. DAFoam can be used to compute derivatives for a large amount of design variables, perform gradient based optimizations, and run OpenFOAM primal solvers to generate CFD samples.

### 1.2 What is OpenFOAM?
OpenFOAM (Open-source Field Operation And Manipulation) is a free finite-volume open-source CFD solver. OpenFOAM is primarily written in C++ and comes with libraries to help facilitate numerical operations on field values. OpenFOAM also has a wide range of utilities for pre- and post- processing such as mesh generation/quality checks and paraview (for post-process visualization). There are three main branches of OpenFOAM: ESI OpenCFD, The OpenFOAM Foundation, and Extended Project. DAFoam only supports the ESI OpenCFD version.


## 2. Details of Configuration Files
Since DAFoam uses OpenFOAM as the CFD solver, the file structure of a DAFoam simulation is very similar to that of an OpenFOAM simulation. To help with clarity, below is the file structure for the [NACA 0012 incompressible tutorial case]([http://github.com/dafoam/tutorials/](https://github.com/DAFoam/tutorials/tree/main/NACA0012_Airfoil/incompressible)) 

<pre>
- 0.orig               // initial fields and boundary conditions
- FFD                  // folder that containts FFD file
- constant             // flow and turbulence property information
- profiles             // naca0012 profile coordinates for mesh generation
- system               // flow discretization, setup, time step etc.
- Allclean.sh          // script to clean up simulation results
- genAirFoilMesh.py    // mesh generation script called by preProcessing
- paraview.foam        // dummy file used by paraview to load results
- preProcessing.sh     // script to generate the mesh
- runScript.py         // main run script for optimization
</pre>

### 2.1 0.orig
The 0.orig file contains the initial field values as well as the field boundary conditions of the simulation:

<pre>
0.orig         
|-- epsilon    // turbulent kinetic energy dissipation rate
|-- k          // turbulent kinetic energy
|-- nut        // turbulent viscosity
|-- nuTilda    // modified turbulent viscosity
|-- omega      // specific dissipation rate
|-- p          // pressure
|-- U          // velocity
</pre>

The exact setup of the 0.orig file (which values to include and what the initial values should be) depends on the case being setup. To serve as an example we can open the 0.orig/U file. The first line is the `dimensions [0 1 -1 0 0 0 0];` line. This line specifies the units used for each field value. For the NACA 0012 case the initial velocity condition is 10 m/s, hence `internalField uniform (10 0 0);` is set. The following block (`boundaryField`) is where the actual boundary conditions are defined. 

<pre>
dimensions      [0 1 -1 0 0 0 0];
  
internalField uniform (10 0 0);

boundaryField
{
    "(wing.*)"
    {
        type            fixedValue;
        value           uniform (0 0 0);
    }
  
    symmetry1
    {
        type            symmetry;
    }
  
    symmetry2
    {
        type            symmetry;
    }
  
    inout
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }
}
</pre>


























































## Post-processing Results
### Installing Paraview
### Loading case into paraview
### Visualizing case in paraview



















{% include links.html %}

---
title: OpenFOAM Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openfoam.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

# OpenFOAM Simulation Setup User Guide

## Introduction

### Background
OpenFOAM (Open-source Field Operation And Manipulation) is a free finite-volume open-source CFD solver. OpenFOAM is primarily written in C++ and comes with libraries to help facilitate numerical operations on field values. OpenFOAM also has a wide range of utilities for pre- and post-processing, such as mesh generation/quality checks and Paraview (for post-process visualization). There are three main branches of OpenFOAM: ESI OpenCFD, The OpenFOAM Foundation, and Extended Project. DAFoam only supports the ESI OpenCFD version, the OpenFOAM version discussed within this document.

### Follow Along
This document contains basic information related to setting up an OpenFOAM simulation using the steady-state NACA0012 simulation. We will discuss every file within this case in an effort to clarify the various aspects of OpenFOAM.

To help with clarity, below is the file structure for the NACA0012 case. As a general overview: `0` contains boundary conditions and initial field values, `constant` handles flow properties (such as turbulence model and fluid modeling parameters), and `system` controls the numerical discretization, equation solution parameters, etc. This document serves as detailed documentation to these directories.

<pre>
- 0.orig               // initial fields and boundary conditions
- constant             // flow and turbulence property information
- system               // flow discretization, setup, time step etc.
- clean                // script to clean and reset case to default
- paraview.foam        // dummy file used by Paraview to load results
- run                  // script to execute simulation
</pre>

These steps will be elaborated on in the coming sections with particlar emphasis on the `0.orig`, `constant`, and `system` directories. It is intended that the user reads this documentation carefully to gain a basic understanding of OpenFOAM. It is also recommended to follow along in the tutorial cases to recreate the simulation and post-process using Paraview (Dont have paraview? Download paraview for free [here!](https://www.paraview.org/download/)). 

## 1. Boundary and Initial Conditions
The `0.orig` directory contains both the boundary conditions and the initial field values for the simulation. For clarity purposes it should be noted here that this simulation contains a `wing` boundary (wall), an `inout` boundary (far field domain), and two symmetry planes, one for either side of the airfoil. For this NACA0012 case, we can expand the `0.orig` directory to see which field values have specified boundary conditions:

<pre>      
|-- 0.orig        // directory containing BCs
  |-- epsilon     // turbulent kinetic energy dissipation rate
  |-- k           // turbulent kinetic energy
  |-- nut         // turbulent viscosity
  |-- nuTilda     // modified turbulent viscosity
  |-- omega       // specific dissipation rate
  |-- p           // pressure
  |-- U           // velocity
</pre>

### Velocity (U)
For the NACA0012, the fluid flow is 10 m/s in the positive x-direction as seen below:

<pre>
dimensions      [0 1 -1 0 0 0 0];          // units to use for velocity (m/s)
internalField uniform (10 0 0);            // velocity value within the simulation domain 

boundaryField
{
    wing                                   // patch name to apply BC to
    {
        type            fixedValue;        // type of BC, could use noSlip
        value           uniform (0 0 0);   // value at boundary
    }

    symmetry1
    {
        type            symmetry;          // symmetry type, nothing else to specify
    }

    symmetry2
    {
        type            symmetry;
    }

    inout
    {
        type            inletOutlet;       // handles reverse flow at outlets
        inletValue      $internalField;
        value           $internalField;
    }
}
</pre>

The wing boundary takes on a `fixedValue uniform (0 0 0);` condition. This enforces a no slip boundary condition at the wall. This is also equivalent to using `type noSlip;` on the wing (either will work). The `symmetry` boundary condition will ensure an identical flow field over the two symmetry planes present. The `inletOutlet` boundary condition automatically applies `fixedValue` when the flow enters the simulation domain with the values given by the `inletValue` key, and `zeroGradient` when the flow exits the domain. Here, the user can use `$internalField` to specify the far field domain conditions: prescribe the same as the internalField value defined above (i.e., `uniform (10 0 0)`). The `value` key for the `inout` patch prescribes an initial value for this patch, and this value will be automatically updated (depending on whether the flow enters or leaves the domain) when the simulation starts. When adding the boundary conditions to a the simulation there are a few points to keep in mind: which field values need boundary conditions specified in `0.orig`, which type of boundary condition to use for eatch patch as well as the accompanying value, the `dimensions` key (specifying which units to use), and finally the `internalField` value.

{% include links.html %}

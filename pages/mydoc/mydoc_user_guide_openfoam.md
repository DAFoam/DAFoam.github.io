---
title: OpenFOAM Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openfoam.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

This chapter was written by [Christian Psenica](https://github.com/ChrisPsenica) and reviewed by [Ping He](https://github.com/friedenhe).

# OpenFOAM User Guide - NACA0012 Simulation Setup

## Introduction

### Background
OpenFOAM (Open-source Field Operation And Manipulation) is a free finite-volume open-source CFD solver. OpenFOAM is primarily written in C++ and comes with libraries to help facilitate numerical operations on field values. OpenFOAM also has a wide range of utilities for pre- and post-processing, such as mesh generation/quality checks and support for Paraview (for post-process visualization). There are three main branches of OpenFOAM: ESI OpenCFD, The OpenFOAM Foundation, and Extended Project. DAFoam only supports the ESI OpenCFD version, the OpenFOAM version discussed within this document.

### Follow Along
This document contains basic information related to setting up an OpenFOAM simulation using the steady-state NACA0012 simulation. We will discuss every file within this case in an effort to clarify the various aspects of OpenFOAM.

To help with clarity, below is the file structure for the NACA0012 case. As a general overview: `0` contains boundary conditions and initial field values, `constant` handles flow properties (such as turbulence model and fluid modeling parameters), and `system` controls the numerical discretization, equation solution parameters, etc. This document serves as detailed documentation to these directories.

<pre>
- 0.orig               // initial fields and boundary conditions
- constant             // transport/ turbulence property information and mesh files
- system               // flow discretization, simulation run parameters, solver settings etc.
- clean                // script to clean and reset case to default
- paraview.foam        // dummy file used by Paraview to load results
- run                  // script to execute simulation
</pre>

These steps will be elaborated on in the coming sections with particular emphasis on the `0.orig`, `constant`, and `system` directories. It is intended that the user reads this documentation carefully to gain a basic understanding of OpenFOAM. It is also recommended to follow along in the tutorial cases to recreate the simulation and post-process using Paraview (Dont have paraview? Download paraview for free, [here!](https://www.paraview.org/download/)). 

## 1. Boundary and Initial Conditions - 0.orig
The `0.orig` directory contains both the boundary conditions and the initial field values for the simulation. For clarity purposes, it should be noted here that this simulation contains a `wing` boundary (wall), an `inout` boundary (far field domain), and two symmetry planes, one for either side of the airfoil. For this NACA0012 case, we can expand the `0.orig` directory to see which field values have specified boundary conditions:

<pre>      
|-- 0.orig        // directory containing BCs
  |-- epsilon     // turbulent kinetic energy dissipation rate
  |-- k           // turbulent kinetic energy
  |-- nut         // turbulent kinematic viscosity
  |-- nuTilda     // modified turbulent viscosity
  |-- omega       // specific dissipation rate
  |-- p           // pressure
  |-- U           // velocity
</pre>

As a note: we name this folder `0.orig`. This is not a necessity; OpenFOAM needs this file to be named `0` at the start of the simulation. Hence in the `run` script we have the line `cp -r 0.orig 0`. This is simply for preservation and is common practice. To avoid confusion, as a motivated reader may notice that various sources use either `0` or `0.orig` naming conventions, we leave the name of this folder as `0.orig` and note the distinction here.

### 1.1 The dimensions and internalField
As a preface to the following boundary conditions discussed, we will clarify a couple entries found in all boundary condition files: `dimensions` and  `internalField`.

When entering values for both boundary conditions and `internalField`, it is important to be mindful of the units used as they are not all constant. Though OpenFOAM's default is SI units, the derived units are based on which solver is used. For example, if using the `simpleFoam` solver (the steady-state solver we will use for the NACA0012 case), pressure is expected to be the kinematic pressure which is measured in $m^2/s^2$. However, if using pimpleFoam (unsteady solver), then pressure is measured as thermodynamic pressure, measured in Pascals $N/m^2 = kg/(m*s^2)$. The exact units used are specified by the `dimensions` key in `0.orig/`. Using the same `0.orig/U` from the NACA0012 case, we can see the dimensions used for velocity are `dimensions [0 1 -1 0 0 0 0];`. This is, as one would suspect, $m/s$. But looking at solely the `dimensions` key, this may not be so obvious. However it is in fact very simple: 

<pre>
dimensionsUsed  [Mass Meter Second Kelvin Mole Ampere Candela]   

dimensions      [0 1 -1 0 0 0 0]; 
</pre>

The `dimensions` key is a list containing 7 numbers. Each (non-zero) number in `dimensions` denotes which unit is being used, corresponding to the entries in `dimensionsUsed` (this key is for an example, it is not an actual key used in OpenFOAM). A zero indicates that the unit is not being used. The value of the actual (non-zero) numbers gives the exponent on the unit. So an entry of `[0 1 0 0 0 0 0]` gives meter ($m$). However, `[0 2 0 0 0 0 0]` indicates $m*m = m^2$ and so on. A negative sign before the number indicates a negative exponent. Knowing this, it becomes far clearer to see which units are expected. As an example, the kinematic pressure, $`m^2/s^2`$, would be `dimensions [0 2 -2 0 0 0 0]`.

Lastly, the `internalField` key is used as an initial condition to the problem and should be assigned with care. Field values such as pressure, temperature, velocity etc. can be easily assigned by the user and depend on what the user wants to simulate. The calculations for turbulent fields (such as `nuTilda`, `k`, `epsilon` etc.) are beyond the scope of this beginner user guide and we encourage the motivated reader to see the advanced user guide for a breakdown on these calculations.

### 1.2 Velocity (U)
For the NACA0012, the fluid flow is 10 m/s in the positive x-direction as seen below:

<pre>
dimensions      [0 1 -1 0 0 0 0];          // units to use for velocity (m/s)
internalField   uniform (10 0 0);          // velocity value within the simulation domain 

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

The wing boundary takes on a `fixedValue uniform (0 0 0);` condition. This enforces a no-slip boundary condition at the wall. This is also equivalent to using `type noSlip;` on the wing (either will work). The `symmetry` boundary condition will ensure an identical flow field over the two symmetry planes present (this is consistent for all field values specified in this section). The `inletOutlet` boundary condition automatically applies `fixedValue` when the flow enters the simulation domain with the values given by the `inletValue` key, and `zeroGradient` when the flow exits the domain. Here, the user can use `$internalField` to specify the far field domain conditions: prescribe the same as the internalField value defined above (i.e., `uniform (10 0 0)`). The `value` key for the `inout` patch prescribes an initial value for this patch, and this value will be automatically updated (depending on whether the flow enters or leaves the domain) when the simulation starts.

### 1.3 Pressure (p)
Since this is a steady-state simulation, the pressure is given as the kinematic pressure ($`m^2/s^2`$). For this solver we use a reference pressure of 0 (`internalField  uniform 0;`).

<pre>
dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    wing
    {
        type            zeroGradient;
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
        type            fixedValue;
        value           $internalField;
    }
}
</pre>

Wall boundaries (such as the wing) receive a `zeroGradient` boundary condition type. As mentioned previously, the symmetry planes always receive the `symmetry` type boundary condition (in the following sections, 1.4-1.8 we will omit discussion of this in an effort to reduce redundancy). The far field domain, `inout`, takes on a fixed value consistent with the `internalField` entry. In a typical setup, inlets (far field domain here) are `fixedValue` while all other physical domains will be `zeroGradient`.

### 1.4 Turbulent Kinetic Energy Dissipation Rate (epsilon)
The following sections (1.4-1.8) are all turbulence field values. It is not uncommon, though not all the time necessary, to use wall functions for these values. For now we will just state the use of wall functions and point the reader to the advanced user guide for in depth details on wall functions and their applications within OpenFOAM. The discussion for these turbulent fields will also be brief as the types of boundary conditions specified largely remain unchanged aside from the `wing` boundary.

<pre>
dimensions      [0 2 -3 0 0 0 0];

internalField   uniform 0.14;

boundaryField
{
    wing
    {
        type            epsilonWallFunction;
        value           $internalField;
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

Here we apply a wall function to the `wing` boundary. As the name implies, wall functions are only applicable to wall boundaries and should not/ cannot be used for other types of boundaries. Additionally, we treat `inout` the same as for velocity (U): apply `fixedValue` when the flow enters the simulation domain, and `zeroGradient` when the flow exits the domain.

### 1.5 Turbulent Kinetic Energy (k)
As noted previously, the boundary conditions applied for these turbulent field values are mostly the same. The one change here is the type of wall function used, now being `kqRWallFunction`. There is no universal wall function applicable to all boundaries. In OpenFOAM we use different wall functions for different field values. Typically the name of the particular wall function being used indicates which field values it may be applied to. As we have the turbulent kinetic energy (k), we use the `kqRWallFunction`. As the name implies, this wall function may be used for the `q` and `R` field values as well (though these values will not be discussed in the basic user guide, but defined in the advanced user guide).

<pre>
dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0.015;

boundaryField
{
    wing
    {
        type            kqRWallFunction;
        value           $internalField;
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

### 1.6 Turbulent Kinematic Viscosity (nut)
For the turbulent viscosity, note the change of the wall function to `nutUSpaldingWallFunction`. Similar as before, this is a wall function specifically designed for the `nut` turbulent field. 

<pre>
dimensions      [0 2 -1 0 0 0 0];

internalField   uniform 4.5E-5;

boundaryField
{
    wing
    {
        type            nutUSpaldingWallFunction;
        value           $internalField;
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
        type            calculated;
        value           $internalField;
    }
}
</pre>

For this field however, we switch the `inout` boundary condition type to `calculated`. This naturally raises two questions: what is a `calculated` boundary condition type, and why use this type versus `inletOutlet` such as the other turbulent fields? 

Put simply, `nut` is a turbulent field which is not solved for directly, its value depends on (calculated from) other field values. Due to this, we do not want to assign a value to this field. We want OpenFOAM to solve for it throughout the simulation process. Therefore, we apply the `calculated` boundary condition type to tell OpenFOAM to solve for this field value rather than read in a user prescribed value on the boundary.

### 1.7 Modified Turbulent Viscosity (nuTilda)
The modified turbulent viscosity is not a calculated field, meaning OpenFOAM solved for it directly, hence the `inout` boundary uses `inletOutlet` again. This field is specific to the Spalart-Allmaras turbulence model (which we use for the NACA0012 case) and is, in some cases, referred to as the Spalart-Allmaras variable.

<pre>
dimensions      [0 2 -1 0 0 0 0];

internalField   uniform 4.5e-05;

boundaryField
{
    wing
    {
        type            fixedValue;
        value           uniform 0.0;
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

However, a wall function is not used for this field value on our wall boundary, `wing`. Rather we assign a zero value to the wall. For clarity sake we provide the definition for nuTilda, but leave the in depth discussion for the advanced user guide: $\tilde{\nu} = \sqrt{\tfrac{3}{2}} (U I \ell)$, where $U$ = reference velocity magnitude, $I$ = turbulence intensity, and $\ell$ = turbulence length scale. Here we can see that nuTilda is based on the velocity which at the wall, is zero. Hence, nuTilda is zero at the wall as well. 

### 1.8 Specific Dissipation Rate (omega)
The final value to discuss is the specific dissipation rate, omega. The treatment for omega is largely the same as the other turbulent field values. We use a wall function on out `wing` boundary and `inletOutlet` on the far field domain. The key difference here is the `blended  true;` entry for the wall function. This delves deeper into wall modeling (a subject left for the advanced user guide), however to clarify for this guide: the blended key blends the physics of different viscous layers near the wall. Here we implement this blending, but the need for this blending is case dependent.

<pre>
dimensions      [0 0 -1 0 0 0 0];

internalField   uniform 100;

boundaryField
{
    wing
    {
        type            omegaWallFunction;
        value           $internalField;
        blended         true;
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

## 2. Transport, Turbulence, and Mesh Properties - constant
The constant directory contains information related to turbulence and transport properties (and in other cases, thermophysical properties). Additionally, the mesh used for the simulation resides in `constant/polyMesh`. The file structure for the NACA0012 case is shown below for clarity:

<pre>      
|-- constant                 // directory containing mesh, turbulence model, and transport properties
  |-- polyMesh               // directory containing the mesh
    |-- boundary             // list of boundaries and associated mesh cells
    |-- cellZones            // grouping of cells (user defined)
    |-- faces                // list of cell faces
    |-- faceZones            // grouping of cell faces (user defined)
    |-- neighbour            // list of neighbour cell labels
    |-- owner                // list of owner cell labels
    |-- points               // vectors describing mesh cell verticies 
    |-- pointZones           // grouping of point verticies (user defined)
  |-- transportProperties    // fluid transport parameters
  |-- turbulenceProperties   // turbulence parameters
</pre>

### 2.1 Mesh Files (polyMesh)
The mesh is user generated and can be generated using various methods/ tools. This can be done using third party programs or using OpenFOAM's built in tools (such as `snappyHexMesh`). For the NACA0012 case, the mesh is already generated and ready to use for the simulation. 

For the discussion of the `polyMesh` directory, we will limit this section to showing the most pertinent file, `boundary`. This is the file most viewed in the `polyMesh` directory, and shows the various boundaries generated during the meshing process. The remaining files (`cellZones`, `faces`, `faceZones`, `neighbour`, `owner`, `points`, and `pointZones`) all contain organizational data on the mesh. Although it is possible to modify a few select entries within the `boundary` file without breaking the mesh (a topic left for the advanced user guide) it is highly recommended to never try and make manual adjustments to the remaining files. Although possible in theory to make modificationss to these files successfully, it is very error prone and not an intended feature. If the physical mesh needs to be adjusted, the best practice is to always regenerate the mesh and have OpenFOAM modify these files for you. Below we can see the boundary file for our NACA0012 case:

<pre>      
4                                       // total number of boundaries in mesh
(
    symmetry1                           // name of boundary
    {
        type            symmetry;       // type of boundary
        inGroups        1(symmetry);
        nFaces          4032;
        startFace       7938;
    }
    symmetry2
    {
        type            symmetry;
        inGroups        1(symmetry);
        nFaces          4032;
        startFace       11970;
    }
    wing
    {
        type            wall;
        inGroups        1(wall);
        nFaces          126;
        startFace       16002;
    }
    inout
    {
        type            patch;
        nFaces          126;
        startFace       16128;
    }
)
</pre>

From the `boundary` file we first notice the number `4`. This number indicates the total number of boundaries defined in our mesh. As we saw from Sec.1, we indeed have four boundaries: two symmetry planes, the wing itself, and the far field domain. Each one of these boundaries is defined here. Within each boundary entry there is an accompanying dictionary providing extra information for OpenFOAM regarding the boundary. The `type` key tells OpenFOAM what type of boundary we have. As expected, the symmetry planes are type `symmetry`, the wing itself is a `wall` boundary, and the far field is a `patch` (allowing fluid to flow through). Similar boundary types will be grouped together in OpenFOAM for organization, hence the `inGroups` key. `nFaces` tells OpenFOAM how many cell faces are contained within the given boundary. `startFace` tells OpenFOAM which cell is the first cell making up a boundary. All mesh cells in OpenFOAM are numbered, and these two keys help OpenFOAM identify boundaries.

### 2.2 transportProperties
The `transportProperties` file contains fluid specific properties which help define what kind of fluid is being simulated (most common air but of course other fluids can be modeled such as water or various gases). In a general sense, `transportProperties` is not the only file containing fluid parameters. For example, `thermophysicalProperties` also contains fluid parameters but is not included in our NACA0012 case as we do not simulate thermodynamic properties for this simulation. 

<pre>      
transportModel Newtonian;  // transport model being used

nu    1.5e-5;              // dynamic viscosity
Pr    0.7;                 // Prandtl number
Prt   1.0;                 // turbulent Prandtl number
</pre>

The first entry tells OpenFOAM which transport model to use. The Newtonian transport model used in the NACA0012 case assumes a constant dynamic viscosity (nu). Hence the following entry, `nu`, where we give this constant value for OpenFOAM to use. The value used here, $1.5e-5$ is a typical value used for modeling air. 

The following two entries are the Prandtl number and turbulent Prandtl number. The Prandtl number is dimensionless quantity, a ratio of momentum diffusivity (kinematic viscosity, $\nu$) to to thermal diffusivity ($\alpha$). The Prandtl number alone does not help describe fluid behaviour for turbulent flow, hence the inclusion of the turbulent Prandtl number, `Prt`. Together, these quantities help identify if momentum diffusivity or thermal diffusivity dominates the fluid flow for both laminar and turbulent flow. Values for `Pr` `Prt` of 0.7 and 1.0 respectively are typical for modeling air.

### 2.3 turbulenceProperties
The `turbulenceProperties` file informs OpenFOAM on how us, the user, wishes to model turbulence. We can see how turbulence modeling is defined below in this file:

<pre>      
simulationType RAS;                     // type of simulation to run
RAS                                     // dictionary containing turbulence model parameters
{ 
    RASModel        SpalartAllmaras;    // specific turbulence model to use
    turbulence      on;                 // whether to model turbulence or only laminar flow
    printCoeffs     off;                // whether to print turbulence model coefficients
} 
</pre>

For our NACA0012 case, we elect a Reynolds Averaged Simulation (`RAS`). There are other options available for the user which are outlined in the advanced user guide. Within the `RAS` dictionary we choose to use the `SpalartAllmaras` turbulence model. This is a very commonly used *one-equation* (solves a single transport equation) model using the 'Spalart-Allmaras variable', `nuTilda`. We elect this model typically due to it's simplicity and low computational cost. An exhaustive discussion on turbulence models in OpenFOAM can be found in the advanced user guide.

The following entry, `turbulence  on;` tells OpenFOAM to model turbulent flow, not just laminar flow. `printCoeffs  off;` refers to the coefficients used in the Spalart-Allmaras turbulence model equation. These coefficients are beyond the scope of this user guide, and for the purposes of our NACA0012 case, we do not need to adjust these coefficients for this turbulence model hence we do not print these coefficients. For more advanced applications, these coefficients may need to be adjusted which would make `printCoeffs  on;` a sensible entry.

## 3. Flow Discretization, Simulation Run Parameters, and Solver Settings - system


<pre>      
|-- system               // directory global simulation parameters
  |-- controlDict        // define solver, and simulation runtime parameters
  |-- decomposeParDict   // decompose the simulation domain to run in parallel
  |-- fvSchemes          // divergence schemes and time stepping scheme
  |-- fvSolution         // iterative solution parameters
</pre>


### 3.1 Solver and Simulation Runtime Parameters 

### 3.2 Decomposition of Domain

### 3.3 Divergence Schemes

### 3.4 Iterative Solution Parameters


## 4. Run, Clean, and Post-processing Files

{% include links.html %}

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

### Preamble
OpenFOAM (Open-source Field Operation And Manipulation) is a free finite-volume open-source CFD solver. OpenFOAM is primarily written in C++ and comes with libraries to help facilitate numerical operations on field values. OpenFOAM also has a wide range of utilities for pre- and post-processing, such as mesh generation/quality checks and Paraview (for post-process visualization). There are three main branches of OpenFOAM: ESI OpenCFD, The OpenFOAM Foundation, and Extended Project. DAFoam only supports the ESI OpenCFD version, the OpenFOAM version discussed within this document.

To help with clarity, below is the general file structure for OpenFOAM simulations. As a general overview: `0` contains boundary conditions and initial field values, `constant` handles flow properties (such as turbulence model and fluid modeling parameters), and `system` controls the numerical discretization, equation solutions, etc. This document serves as detailed documentation to these directories.

<pre>
- 0.orig               // initial fields and boundary conditions
- constant             // flow and turbulence property information
- system               // flow discretization, setup, time step etc.
- paraview.foam        // dummy file used by Paraview to load results
</pre>

### Follow Along
This document contains basic information related to setting up an OpenFOAM simulation (in a general sense). This is a live project: more will be added as time goes on. When setting up an OpenFOAM simulation there are a few basic steps to follow:

<pre>
1. Select appropriate turbulence model and generate the required mesh
2. Define boundary conditions
3. Define fluid properties in constant/transportProperties and constant/thermophysicalProperties
4. Define solution parameters in system/fvSchemes and system/fvSolution
5. Define simulation parameters in system/controlDict
</pre>

These steps will be elaborated on in the coming sections. To conclude this document there will be two simulation tutorial cases: a steady state airfoil simulation (using the simpleFoam solver) and an unsteady 2D vortex shedding around a circle simulation (using the pimpleFoam solver). It is intended that the user reads this documentation carefully to gain an understanding of OpenFOAM and how to properly set up a CFD simulation in the framework. Following this, the user should follow along in the tutorial cases to recreate the simulation and post-process using Paraview (download paraview for free [here](https://www.paraview.org/download/)). 

## 1. Selecting Turbulence Model & Mesh Requirements
The focus on this section is to briefly go over the various turbulence models in OpenFOAM and list pertinent information on each model which will allow the reader to carefully select the model most suitable for their needs. The wall modelling (wall functions) will also be discussed as well as mesh requirements when using wall functions. The turbulence model is defined in `constant/turbulenceProperties`. The basic format for `turbulenceProperties` is the following:

<pre>
simulationType      RAS;               // which type of simulation to run

RAS                                    // RAS sub-dictionary
{
    RASModel        SpalartAllmaras;   // which RANS model to use
    turbulence      on;                // turn on/off turbulence modeling
    printCoeffs     on;                // print turbulence model coefficients

    SpalartAllmarasCoeffs              // model coefficients (only needed here if user wishes to change coefficient values)
    {                                  
        sigmaNut    0.66666;           // default values in SA
        kappa       0.41;
        Cb1         0.1355;
        Cb2         0.622;
        Cw2         0.3;
        Cw3         2.0;
        Cv1         7.1;
        Cs          0.3;
    }
}
</pre>

OpenFOAM supports `laminar`, `RAS` (Reynolds Averaged Stress), `DES` (Detached Eddy Simulation), and `LES` (Large Eddy Simulation). It should be noted that `DES` is a sub-model of `LES`. If choosing `laminar`, the sub-dictionary is not needed (only needed for `LES` and `RAS`). Model coefficients do not need to be defined within `turbulenceProperties`. If the coefficients are not listed then OpenFOAM uses default values. If one or more of these coefficients needs to be changed then the value should be adjusted in `constant/turbulenceProperties`.

In a general sense, `RAS` (`RANS`) is the industry workhorse for turbulence modelling. It is the most affordable, runs for steady and unsteady simulations, and is robust. `LES` and `DES` are far more computationally expensive and therefore are not used as often as `RAS`. For a majority of simulations, `RAS` can/will work just fine. `LES` and `DES` are better suited for capturing intricate flow details (eddies) on a refined mesh.

The following sections contain a comprehensive list of available turbulence models in OpenFOAM v2206. It is intended that the user selects a model based on their particular needs (comparing `Good For` and `Bad For` columns). The `Requires Wall Functions` column signifies whether the turbulence model is expecting wall functions or not. If yes, a wall function *must* be used on the fields listed under `Required Boundary Conditions` for any `wall` boundaries within the simulation domain. The `Supports Wall Functions` column indicates whether the user has the option to use wall functions (yes) or if the user should not implement wall functions with the selected turbulence model (no). In `Sec. 1.4` the available wall functions are listed alongside yPlus and mesh refinement requirements. The final column, the minimum `Required Boundary Conditions` to run the simulation, serves as a starting point for `Sec. 2.0` where boundary conditions will be discussed in more detail. Please note that boundary conditions for pressure, velocity, temperature etc. are excluded from the below lists as those are case specific. The `Required Boundary Conditions` column *only* covers the boundary conditions needed for a particular turbulence model.

### 1.1 RAS (Reynolds-Averaged Stress) Models
| **Model** | **Good For** | **Bad For** | **Requires Wall Functions** | **Supports Wall Functions** | **Required Boundary Conditions** |
|-----------|--------------|-------------|-----------------------------|-----------------------------|----------------------------------|
| **laminar** | Laminar flow | Turbulent/transitional flow | No | No | Standard only (U, p, T etc.) |
| **Spalart-Allmaras** | External aerodynamics, High speed flow, Turbomachinery, mildly complex internal/external flow, Wall bounded flow | Flows with high separation/transition | No | No | nuTilda |
| **kEpsilon** | Free shear flow, Attached flow, Fully developed turbulence, General industrial flows, High Re | Complex flows with severe pressure gradient, flow separation, strong streamline curvature, Low Re, Rotating flow| Yes | - | k, epsilon |
| **realizableKE** | Complex shear flow, Moderate swirls/vorticies, Vortex shedding, Flow separation, Near-wall behaviour (over kEpsilon), Jet impingmemnt, Recirculating flow | Adverse pressure gradients, Flow separation | Yes | - | k, epsilon |
| **RNGkEpsilon** | High strain rate flow, Swirls/Vorticies, Flow Separation, Near-wall behaviour (over kEpsilon) | Adverse pressure gradients, Flow separation | Yes | - | k, epsilon |
| **kEpsilonPhitF** | Laminar to turbulent flow transition | Not as robust as standard kEpsilon, Limited validation | Yes | - | k, epsilon, phit, f |
| **kEpsilonLopesdaCosta** | Turbulence development in porous domains (modeled by the powerLawLopesdaCosta porosity model), Low Re | Non-porous media, High Re | No | No | k, epsilon |
| **LaunderSharmaKE** | Low Re, Wall bounded flow | High Re with wall functions | No | No | k, epsilon |
| **LamBremhorstKE** | Low Re, Near wall modeling | High Re | No | No | k, epsilon |
| **LienCubicKE** | Anisotropic turbulence | Less robust, Sensitive to mesh/flow | No | No | k, epsilon |
| **ShihQuadraticKE** | Flow separation, Flow curvature handling (both over standard kEpsilon) | Limited validation, less robust for industrial applications | No | No | k, epsilon |
| **kOmega** | Free shear, Low Re, Complex boundary layer flows under adverse pressure gradient, Flow separation, Exernal aerodynamics, Turbomachinery | Free shear flow, Laminar to turbulent flow transition, Inlet sensitivity | No | Yes | k, omega |
| **kOmegaSST** | *Most used RANS model*: Low Re, Flows with separation, adverse pressure gradients, external aerodynamics, turbomachinery, Heat transfer, Transitional flows (over standard kOmega) | Transitional and strong swirl not captured well, Rotational frames | No | Yes | k, omega |
| **kOmegaSSTLM** | Laminar to turbulent flow transition, Turbomachinery | Complex setup requiring transition correlations | No | No | ReThetat, gammaInt, gammaIntEff, k, omega |
| **kOmegaSSTSAS** | Hybrid RANS–LES-like modeling, Unsteady separated flows, Scale-Adaptive simulation variant | Costly, Grid-sensitive, Not for simple steady cases | No | No | k, omega |
| **kkLOmega** | Blended kEpsilon/kOmega, Transitional boundary layers | More complex than SST with limited benefit | No | Yes | k, kL, kt, omega |
| **EBRSM** | Complex anisotropic turbulence, Separation, Curvature, Swirling flows, Secondary flow in ducts, Jet impingmemnt | More expensive than eddy viscosity models, Less robust model, Simple attached flows (overkill) | No | No | k, epsilon, f |
| **LRR** | Reynolds-stress anisotropy, Swirling flows, Curvature | Computationally expensive, Less robust than k–epsilon/omega | No | No | k, epsilon |
| **SSG** | Same as LRR but improved stability/accuracy in complex flows | Computationally expensive, Requires fine mesh | No | No | k, epsilon |
| **LienLeschziner** | Low Re, Near wall damping | Less general purpose than SST or realizableKE | No | No | k, epsilon |
| **kL** | Transitional and low Re boundary layer modelling | Not widely validated | No | No | k, L, Rt |
| **qZeta** | Low Re boundary layer modelling, Flow separation | Not as widely validated, Less robust than SST or IDDES | No | No | k, epsilon, q, zeta |

### 1.2 Large Eddy Simulation (LES) Models
| **Model** | **Good For** | **Bad For** | **Requires Wall Functions** | **Supports Wall Functions** | **Required Boundary Conditions** |
|-----------|--------------|-------------|-----------------------------|-----------------------------|----------------------------------|
| **DeardorffDiffStress** | Early LES model with prognostic SGS kinetic energy, Atmospheric boundary layers | Outdated, Poor accuracy in complex shear flows | No | Yes | nut |
| **dynamicKEqn** | Inhomogeneous flows, Unsteady flows | More computationally expensive, Can be unstable on coarse grids | No | Yes | k |
| **dynamicLagrangian** | Dynamic Smagorinsky with Lagrangian averaging, Accurate in complex (inhomogeneous) flows | Computationally heavier, Sensitive to averaging parameters | No | Yes | nut |
| **kEqn** | Robust/Widely used, Good compromise between accuracy and cost | Transitional or strongly inhomogeneous turbulence | No | Yes | k |
| **Smagorinsky** | Robust, Good for canonical LES (channel, shear flows, mixing layers), Homogenous isotropic turbulence | Overdamps turbulence, Near wall treatment, Transitional regions, Flow with backscatter, Complex geometry | No | Yes | nut |
| **WALE** | Near-wall behavior (improved over Smagorinsky) good for wall-bounded flows, Laminar to turbulent flow transition, Rotating flow | Can underpredict in isotropic turbulence | No | Yes | nut |

### 1.3 Detached Eddy Simulation (DES)
| **Model** | **Good For** | **Bad For** | **Requires Wall Functions** | **Supports Wall Functions** | **Required Boundary Conditions** |
|-----------|--------------|-------------|-----------------------------|-----------------------------|----------------------------------|
| **kOmegaSSTDES** | External aerodynamics, Flows separation, Bluff body aerodynamics | Grid-induced separation (“grey area problem”), Sensitive to boundary layer mesh | Yes | - | k, omega, nut |
| **kOmegaSSTDDES** | Improves DES by delaying switch from RANS→LES inside attached boundary layers, turbomachinery | Sensitive to mesh quality, Can underpredict small-scale turbulence | Yes | - | k, omega, nut |
| **kOmegaSSTIDDES** | Reduces grey-area issue, Robust for complex industrial flow separation and wall-bounded turbulence | Requires fine LES mesh in separated regions | Yes | - | k, omega, nut, IDDESDelta |
| **SpalartAllmarasDES** | Relatively cheap, Internal/external flow | Grid-induced separation if mesh not adequate, Not robust in massively separated flows | No | No | nuTilda |
| **SpalartAllmarasDDES** | Reduces grey-area problem, Better boundary layer shielding | Limited accuracy for complex 3D separated flows compared to SST-based variants | No | No | nuTilda |
| **SpalartAllmarasIDDES** | Robust and cheaper than SST-IDDES, used in aerospace and automotive LES/RANS hybrids | Free shear flows, Mesh sensitive | No | No | nuTilda, IDDESDelta |

### 1.4 Wall Functions And Accompanying Mesh Requirements
When running an OpenFOAM simulation (CFD simulations in general) the choice is up to the user as to fully resolve the boundary layer or to model the boundary layer (approximate the effects of the boundary layer but do not resolve the boundary layer). To model the boundary layer, OpenFOAM has a variety of wall functions to use. These wall functions and turbulence models go hand-in-hand: some of the above listed turbulence models support the use of wall functions while in some cases the implimentation is required. Other turbulence models should not have wall functions implemented as they fully resolve the boundary layer.

When implementing wall functions it becomes imperative to mesh according to the yPlus requirements of the turbulence model/wall functions. Fig. 1 shows a schematic of a velocity boundary layer. A boundary layer is divided into two main parts: the `outer layer` (where flow re-joins the bulk fluid behaviour) and the `inner layer` (where the boundary layer develops). Within the inner layer, the boundary layer is further divided into three sub-categories: the `viscous sub-layer`, the `buffer layer`, and the `log-law` layer.

<img src="/images/user_guide/BoundaryLayerDiagram.pgn" style="width:500px !important;" />

Fig. 1. Velocity Boundary Layer Schematic. The red line is the velocity profile, the curved blue line is uPlus, and the straight blue line is the log-law line.

yPlus is the non-dimensional distance from the first near-wall cell center to the wall boundary. It is used to determine to what extent the boundary layer is being resolved. If yPlus is about unity or less then the boundary layer is said to be fully resolved. Generally, though this can depend on the exact CFD setup, it is commonly accepted that the viscous sub-layer, buffer layer, and log-law layer can be found within the following yPlus ranges:

<pre>
Viscous sub-layer: (0 , 5)
Buffer layer:      (5 , 30)
Log-law layer:     (30 , 300)
</pre>

The `log-law` layer gets its name from a linear relationship: the `Law of The Wall` states that the bulk turbulent flow velocity at a certain point is proportional to the logarithm of the distance between the point and the wall boundary. This linear relationship can be seen in Fig. 1 where the velocity profile (red line) is near parallel to the log-law line. OpenFOAM supports `Log-law wall functions`. These are wall functions which use the `Law of The Wall` to predict or model the effects of the boundary layer. In light of this, log-law wall functions should be accompanied by an average yPlus value within the range `[30 , 300]`.

If choosing to use wall functions, OpenFOAM organizes the supported wall functions into 6 main groups:

<pre>
1. nutWallFunctions
2. epsilonWallFunctions
3. kqRWallFunctions
4. omegaWallFunctions
5. fWallFunctions
6. v2WallFunctions
</pre>

The following table lists all of the wall functions supported by OpenFOAM:

| **Wall Function** | **Used For** | **Apply To** | **Condition** | **yPlus** |
|-------------------|--------------|--------------|---------------|-----------|
| **nutWallFunction** | High Re | nut | `nutWallFunction` | `Log-law`: 3 - 300 |
| **nutLowReWallFunction** | Low Re | nut | `nutLowReWallFunction` | `Viscous sub-layer`: ~1 |
| **nutUWallFunction** | High Re | nut | `nutUWallFunction` | `Log-law`: 3 - 300 |
| **nutkWallFunction** | High Re | nut | `nutkWallFunction` | `Log-law`: 3 - 300 |
| **nutUSpaldingWallFunction** | High Re | nut | `nutUSpaldingWallFunction` | `Log-law`: 3 - 300 |
| **epsilonWallFunction** | High Re | epsilon | `epsilonWallFunction` | `Log-law`: 3 - 300 |
| **epsilonLowReWallFunction** | Low Re | epsilon | `epsilonLowReWallFunction` | `Viscous sub-layer`: ~1 |
| **kqRWallFunction** | High Re | k, q, R | `zeroGradient` for k, `kqRWallFunction` for q and R | `Log-law`: 3 - 300 |
| **kLowReWallFunction** | Low Re | k | `kLowReWallFunction` | `Viscous sub-layer`: ~1 |
| **omegaWallFunction** | High and low Re | omega | `omegaWallFunction` | `Log-law`: 3 - 300 if High Re, `Viscous sub-layer`: ~1 if Low Re |
| **fWallFunction** | High and low Re | f | `fWallFunction` | `Log-law`: 3 - 300 |
| **V2WallFunction** | High and low Re | v2 | `v2WallFunction` | `Log-law`: 3 - 300 |

After choosing a turbulence model that suits the needs of the simulation, the user should then decide whether to fully resolve the boundary layer or not. If not fully resolving the boundary layer (using a wall function from the above list) then the mesh yPlus requirements should be satisfied as outlined by the final column in the above table. If the user is fully resolving the boundary layer then the above table is not needed and yPlus should be about unity or less.


## 2. Boundary Conditions
The boundary conditions (and initial field values) are defined in the 0.orig folder. The name of this folder is not random/arbitrary. The `0` is the time (indicating that these are field values at time t=0s). The `orig` portion denotes that these are the *original* boundary conditions. These boundary conditions will be copied into other time directories during the simulation which usually are deleted once the run is over. Hence a `0.orig` folder is made and preserved. The logic of boundary conditions can best be described by Fig. 2 below where boundary conditions are set for outer domains:

<img src="/images/user_guide//analysis_discretization.png" style="width:700px !important;" />

Fig. 2. A schematic description of the internal and boundary fields for a 2D simulation domain

Changes made to boundary conditions should occur within the `0.orig` directory. When running a simulation the user should copy the `0.orig` directory to the same location and rename it to `0` (this tells OpenFOAM to use these boundary conditions to start the simulation). Below is a list of field values used in OpenFOAM. The list contains some of the most commonly used field values in `0.orig` though is not exhaustive.

<pre>
0.orig      
|-- epsilon    // turbulent kinetic energy dissipation rate
|-- k          // turbulent kinetic energy
|-- nut        // turbulent viscosity
|-- nuTilda    // modified turbulent viscosity
|-- omega      // specific dissipation rate
|-- alphat     // turbulent thermal diffusivity
|-- p          // pressure
|-- U          // velocity
|-- T          // temperature
|-- h          // enthalpy
|-- e          // internal energy
|-- p_rgh      // absolute pressure minus hydrostatic pressure 
|-- phi        // face flux
|-- rho        // density
|-- psi        // compressibility
</pre>

To understand the basic setup of a boundary condition file in `0.orig` the below `0.orig/U` file from the Sec. 6 airfoil tutorial case can be analyzed. Though this will be discussed in detail in Sec. 6, for clarity purposes it should be noted here that this simulation contains a `wing` boundary (wall), an `inout` boundary (far field domain), and two symmetry planes, one for either side of the air foil. These boundaries collectively may be referred to as patches within OpenFOAM. As a final note, the far field fluid flow is 10m/s in the positive x-direction.

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

The wing boundary takes on a `fixedValue uniform (0 0 0);` condition. This enforces a no slip boundary condition at the wall. This is also equivalent to using `type noSlip;` on the wing (either will work). The `symmetry` boundary condition will ensure an identical flow field over the two symmetry planes present. The `inletOutlet` boundary condition automatically applies `fixedValue` when the flow enters the simulation domain with the values given by the `inletValue` key, and `zeroGradient` when the flow exits the domain. Here, the user can use `$internalField` to specify the far field domain conditions: prescribe the same as the internalField value defined above (i.e., `uniform (10 0 0)`). The `value` key for the `inout` patch prescribes an initial value for this patch, and this value will be automatically updated (depending on whether the flow enters or leaves the domain) when the simulation starts. When adding the boundary conditions to a the simulation there are a few key points to keep in mind: which field values need boundary conditions specified in `0.orig`, which type of boundary condition to use for eatch patch and the accompanying value, the `internalField` value, and finally the `dimensions` key (which units to use). 

*Continue here next, discuss how to tell which field values need BCs, what their values should be, and which type to use. Lastly, include calculations for turbulence quantities*

## 3. Fluid Properties - Under development
The constant folder contains the mesh files (polyMesh directory) as well as flow and turbulence property definitions:

<pre>
constant         
|-- polyMesh               // directory containing the files
  |-- boundary             // mesh boundary patch names and types
  |-- faces.gz             // mesh faces
  |-- neighbour.gz         // face neighbour info
  |-- owner.gz             // face owner info
  |-- points.gz            // baseline mesh point coordinates
|-- transportProperties    // transport model definition
|-- turbulenceProperties   // turbulence model
</pre>

As seen below, from the polyMesh/boundary file, are the same boundary names as seen in 0.orig/U. The boundary file can be lightly adjusted manually: users can change the name of boundaries (such as changing the `wing` boundary name to `airfoil` for example), the type of boundary present, and delete boundaries. However, though these values can be changed without destroying the mesh, mesh manipulation should not take place manually. Manually adjusting the other files in polyMesh/ or the other entries (nFaces, startFace, inGroups etc.) is a difficult and inefficient method of adjusting the mesh and will most likely destroy the mesh. If the mesh must be adjusted the best practice is to regenerate the mesh.

<pre>
4    // number of boundaries defined in file (modifiable)
(
    symmetry1                          // name of boundary (modifiable)
    {
        type            symmetry;      // type of boundary (modifiable)
        inGroups        1(symmetry);   // group of boundary
        nFaces          4032;          // number of faces in boundary
        startFace       7938;          // starting face of boundary
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

The following two files, transportProperties and turbulenceProperties, are relatively straightforward. The transportProperties defines flow properties which may be adjusted to model a different fluid:

<pre>
transportModel Newtonian;   // transport model to use

nu 1.5e-5;                  // molecular viscosity
Pr 0.7;                     // Prandtl number
Prt 1.0;                    // turblent Prandtl number
</pre>

The turbulenceProperties file elects which turbulence model to use:

<pre>
simulationType RAS;
RAS 
{ 
    RASModel             SpalartAllmaras;   // which RAS model to use
    turbulence           on;                // model turbulence
    printCoeffs          off;               // whether or not to print turbulence model coefficients
} 
</pre>

## 4. Solution Parameters
## 5. Simulation Parameters
## 6. Tutorial Cases: 2D Steady Airfoil & 2D Vortex Shedding



















{% include links.html %}

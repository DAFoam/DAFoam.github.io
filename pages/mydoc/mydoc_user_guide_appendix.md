---
title: Appendix
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: user-guide-appendix.html
folder: mydoc
---
{% include note.html content="This webpage is under construction." %}

## Mesh generation for OpenFOAM

## DES and LES simulations in OpenFOAM

Below is an OpenFOAM tutorial for performing a DES simulation of an airfoil. The case involves a three-dimensional airfoil positioned near the center of a computational domain whose dimensions are much larger than the airfoil's chord length. The flow conditions are as follows:

- Reynolds number based on chord: $Re_c = \frac{U_\infty c}{\nu} = 6 \times 10^6$
- Streamwise far-field velocity: $U_x = 51.4815$ m/s
- Characteristic length (local chord length): $c = 1.0$ m
- Kinematic viscosity of the fluid: $\nu = 8.58 \times 10^{-6}$ m²/s
- Turbulence model: $k\text{-}\omega$ SST model

### Initial condition from simpleFoam case
Before running the DES simulation, we first use simpleFoam to obtain an initial flow field. The converged RANS solution can then be used as the initial flow field for the DES running. Since the main focus is the DES simulation, the setup of the RANS case can simply follow the standard OpenFOAM tutorials. Here, we only provide a brief description of the `constant/turbulenceProperties` and `system/controlDict` files.

#### Turbulence Properties Configuration

The `constant/turbulenceProperties` file is configured as follows:
```foam
simulationType RAS;

RAS
{
    RASModel        kOmegaSST;
    turbulence      on;
    printCoeffs     on;
}
```

#### Control Dictionary Configuration

The `system/controlDict` file contains:
```foam
application     simpleFoam;

startFrom       startTime;

startTime       0;

stopAt          endTime;

endTime         10000;
```

## DES case
Next, we will proceed to run the $k\text{-}\omega$ SST IDDES simulation using the RANS solution as the initial condition. The length scale is set to $\delta_\text{max}$, defined as the maximum edge length of a mesh cell.



{% include links.html %}

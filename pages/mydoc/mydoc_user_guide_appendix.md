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

### DES case
Next, we will proceed to run the $k\text{-}\omega$ SST IDDES simulation using the RANS solution as the initial condition. This hybrid approach combines the advantages of RANS modeling in the boundary layer regions with LES capabilities in separated flow regions, allowing for accurate prediction of complex turbulent structures while maintaining computational efficiency. The length scale is set to $\delta_\text{max}$, defined as the maximum edge length of a mesh cell.

#### Turbulence Properties Configuration

The `constant/turbulenceProperties` file is configured as follows:
```foam
simulationType      LES;
LES
{
    LESModel        kOmegaSSTIDDES;
    printCoeffs     no;
    turbulence      yes;
    delta           IDDESDelta;
    IDDESDeltaCoeffs
    {
        hmax           maxDeltaxyz;
        maxDeltaxyzCoeffs
        {
        }
    }
}
```

#### Control Dictionary Configuration

The `system/controlDict` file contains:
```foam
application     pimpleFoam;
startFrom       latestTime;
startTime       0;
stopAt          endTime;
endTime         10000;
deltaT          0.00001;
writeControl    adjustable;
writeInterval   0.0065;
purgeWrite      30;
writeFormat     ascii;
writePrecision  8;
writeCompression off;
timeFormat      general;
timePrecision   8;
runTimeModifiable yes;
adjustTimeStep  no;
maxCo           5;
```

#### fvSchemes Configuration

The `constant/turbulenceProperties` file is configured as follows:
```foam
ddtSchemes
{
    default         backward;
}
gradSchemes
{
    default         Gauss linear;
    grad(p)         Gauss linear;
}
divSchemes
{
    default         none;
    div(phi,U)      Gauss DEShybrid
        linear                    
        linearUpwind grad(U)      
        hmax
        0.65                      
        1                         
        0.028                     
        0                         
        1                         
        1; 
    div(phi,k)      Gauss limitedLinear 1;
    div(phi,omega) Gauss limitedLinear 1;
    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}
laplacianSchemes
{
    default         Gauss linear corrected;
}
interpolationSchemes
{
    default         linear;
}
snGradSchemes
{
    default         corrected;
}
wallDist
{
    method          meshWave;
    nRequired       yes;
}
```

#### fvSolution Configuration

The `constant/turbulenceProperties` file is configured as follows:
```foam
solvers
{
    p
    {
        solver          GAMG;
        smoother        DICGaussSeidel;
        tolerance       1e-06;
        relTol          0.05;
    }
    pFinal
    {
        $p;
        relTol          0;
    }
    "(U|k|omega)"
    {
        solver          PBiCG;
        preconditioner  DILU;
        tolerance       1e-05;
        relTol          0.1;
    }
    "(U|k|omega)Final"
    {
        $U;
        relTol          0;
    }
}
SIMPLE
{
    nNonOrthogonalCorrectors 0;
    pRefCell        0;
    pRefValue       0;
}
PIMPLE
{
    nOuterCorrectors 1;
    nCorrectors      3;
    nNonOrthogonalCorrectors 1;
    pRefCell        0;
    pRefValue       0;
}
relaxationFactors
{
    fields
    {
    }
    equations
    {
        ".*"        1;
    }
}

```
#### Results from IDDES method


Fig.1 Grids for the NACA0012 airfoil

{% include links.html %}

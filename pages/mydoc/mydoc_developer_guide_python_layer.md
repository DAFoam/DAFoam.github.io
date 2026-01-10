---
title: Python Layer
keywords: developer guide
summary:
sidebar: mydoc_sidebar
permalink: developer-guide-python-layer.html
folder: mydoc
---

## Overview

The Python layer provides the user-facing API for DAFoam and integrates with MPhys for multidisciplinary optimization. For developers who need to wrap DAFoam into their framework or conduct high-level developments, the Python layer is the main entry point. The Python layer consists of two main modules:

1. **[pyDAFoam.py](dafoam/pyDAFoam.py)** - Core solver interface with DAOPTION and PYDAFOAM classes (see below)
2. **[mphys_dafoam.py](dafoam/mphys/mphys_dafoam.py)** - MPhys/OpenMDAO component definitions and coupling

The Python layer communicates with the C++ layer through the Cython interface ([pyDASolvers.so](dafoam/libs/pyDASolvers.so)), enabling efficient data transfer and control flow between high-level Python optimization frameworks and low-level CFD computations.

## pyDAFoam.py - Core Solver Interface

### DAOPTION Class

The `DAOPTION` class defines all configuration options for DAFoam solvers. Options are categorized into three levels:

**Basic Options** - Used for every solver and case:
- `solverName`: Solver type (e.g., DASimpleFoam, DARhoSimpleFoam, DAPisoFoam)
- `primalMinResTol`: Convergence tolerance for primal solver (default: 1.0e-8)
- `primalBC`: Boundary conditions that override the "0" folder
- `primalInitCondition`: Initial field values
- `function`: Objective and constraint function definitions
- `inputInfo`: Input variable definitions (design variables, boundary conditions, etc.)

**Intermediate Options** - Used for special situations:
- `primalVarBounds`: Bounds to prevent solution divergence
- `adjEqnSolMethod`: Adjoint equation solution method
- `normalizeStates`: State normalization for better conditioning

**Advanced Options** - Case-specific performance tuning:
- `maxResConLv4JacPCMat`: Preconditioner memory reduction
- `adjPartDerivFDStep`: Finite difference step for partial derivatives
- `adjPCLag`: Preconditioner lag for adjoint solver

### PYDAFOAM Class

The `PYDAFOAM` class is the main interface to initialize and manage DAFoam C++ solvers. PYDAFOAM will be called/used in the DAFoam builder defined in mphys_dafoam.py (see the next section). PYDAFOAM's Key responsibilities:

**Initialization**:
- Creates DASolver C++ object through Cython interface
- Initializes OpenFOAM mesh and flow fields by calling  initSolver()
- Configures input/output variables based on `inputInfo` and `outputInfo`
- setup connectivity and interfaces with pyGeo, IDWarp, etc.

**Key Methods**:
- `__call__()`: Solves the primal flow equations
- `setMesh()`: Associates an IDWarp mesh object for geometry changes
- `getOption()` / `setOption()`: Get/set DAOption parameters

## mphys_dafoam.py - MPhys Integration

The `mphys_dafoam.py` module implements the MPhys Builder API and defines OpenMDAO components that wrap DAFoam's flow solver capabilities, enabling seamless integration with multidisciplinary optimization frameworks and standardizing the interface for coupling with other physics solvers (structural, thermal, etc.). One of the main purposes of mphys_dafoam.py is to setup the MDO problem, illustrated as an OpenMDAO N2 diagram below. In the following, we will elaborate on how mphys_dafoam.py setups such an N2 diagram.

<img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/dafoam_n2.png" style="width:1000px !important;" />

*Figure 1: N2 diagram for a typical DAFoam aerodynamic optimization case.*

### DAFoamBuilder Class

`DAFoamBuilder` is the **main entry point** for using DAFoam in optimization workflows. It implements the MPhys Builder API to create and connect DAFoam components. In a typical runScript.py, the builder is instantiated and added to the MPhys multipoint group:

```python
# Example from runScript.py
dafoam_builder = DAFoamBuilder(
    options=daOptions,  # daOptions is a dict defined in runScript.py
    mesh_options=meshOptions, # meshOptions is a dict defined in runScript.py
    scenario="aerodynamic"
)
dafoam_builder.initialize(self.comm)
```

Here DAFoamBuilder is defined in [mphys_dafoam.py:21-64](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L21-L64):
```python
DAFoamBuilder(
    options,              # DAFoam options (daOption dict)
    mesh_options=None,    # IDWarp mesh warping options
    scenario="aerodynamic",  # "aerodynamic", "aerostructural", or "aerothermal"
    run_directory=""      # Directory to run the case
)
```

The `scenario` parameter configures coupling behavior:
- `"aerodynamic"`: Standard aerodynamic analysis (no coupling)
- `"aerostructural"`: Enables structural coupling with force transfer
- `"aerothermal"`: Enables thermal coupling with heat transfer

In the following, we elaborate on the methods and members defined in the DAFoamBuilder class.

**Builder Initialization** ([mphys_dafoam.py:67-78](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L67-L78)):

The `initialize()` method creates the PYDAFOAM solver instance:
```python
self.DASolver = PYDAFOAM(options=self.options, comm=comm)
if self.mesh_options is not None:
    mesh = USMesh(options=self.mesh_options, comm=comm)
    self.DASolver.setMesh(mesh)  # add the design surface family group
```
This line call the PYDAFOAM class defined in pyDAFoam.py to initialize all OpenFOAM flow fields and meshes. NOTE: in PYDAFOAM, we will call the C++ layer library to initialize OpenFOAM (e.g., createMesh, createTime, createFields). If `mesh_options` is provided, it also creates an IDWarp `mesh` object and associates it with the solver.

**Overview of Key Builder Methods**:

The following are the key builder methods. They will NOT be directly used in DAFoam. Instead, these methods will be used in Mphys to set up the MDO problem. Each of this method will call key DAFoam components defined in mphys_dafoam.py. We will elaborate on these DAFoam components in the next subsection.

1. **`get_solver()`** ([mphys_dafoam.py:80-82](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L80-L82))
   - Returns the DASolver object
   - Used by RLT (Radial, Linear, Tangent) transfer schemes in MDO

2. **`get_coupling_group_subsystem()`** ([mphys_dafoam.py:85-93](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L85-L93))
   - Creates and returns a `DAFoamGroup` containing:
     - DAFoamSolver (primal and adjoint solution)
     - DAFoamWarper (mesh deformation, if enabled)
     - MDO coupling components (forces for aero-structural, thermal for aero-thermal, etc.)

3. **`get_mesh_coordinate_subsystem()`** ([mphys_dafoam.py:95-98](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L95-L98))
   - Returns `DAFoamMesh` component
   - Outputs design surface coordinates as initial geometry

4. **`get_pre_coupling_subsystem()`** ([mphys_dafoam.py:100-107](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L100-L107))
   - Returns `DAFoamPrecouplingGroup`
   - Handles geometry design variable changes (e.g., twist, shape changes)
   - Contains DAFoamWarper for pre-coupling mesh deformation

5. **`get_post_coupling_subsystem()`** ([mphys_dafoam.py:109-110](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L109-L110))
   - Returns `DAFoamPostcouplingGroup`
   - Contains `DAFoamFunctions` component for computing objectives/constraints

### OpenMDAO Component Classes

#### DAFoamGroup

**Purpose**: OpenMDAO Group containing the main solver and optional coupling components. It does not do the actual computation, it just group certain components together to facilitate MDO.

**Structure** ([mphys_dafoam.py:125-181](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L125-L181)):
- **deformer**: DAFoamWarper component (if `use_warper=True`)
- **solver**: DAFoamSolver component (always included)
- **thermal**: DAFoamThermal component (if `thermal_coupling=True`)
- **forcecoupling**: DAFoamForces component (if `struct_coupling=True`)

The group automatically promotes inputs/outputs based on coupling configuration. The following figure shows the N2 diagram for the DAFoamGroup for the aerodynamic, aerothermal, and aerostructural scenarios.

<img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/dafoam_group_aero.png" style="width:200px !important;" />
    <img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/dafoam_group_aerothermal.png" style="width:200px !important;" />
    <img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/dafoam_group_aerostruct.png" style="width:200px !important;" />

*Figure 2: N2 diagram for the DAFoamGroup: Left: Aero-only, Mid: Aero-thermal, Right: Aero-Struct.*

#### DAFoamSolver

**Purpose**: An ImplicitComponent that solves primal nonlinear equations and adjoint linear systems ([mphys_dafoam.py:232-605](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L232-L605)). This component does the most critical calculation!

**Key Methods**:
- `setup()`: Declares inputs (from `inputInfo`) and outputs (from `outputInfo`)
- `solve_nonlinear()`: Solves primal equations to find w such that R(w, x) = 0
- `linearize()`: Assembles explicit Jacobian matrices (dR/dw, dR/dx), NOTE: this method is not currently used in DAFoam; DAFoam uses Jacobian-free adjoint.
- `apply_linear()`: compute the matrix vector products for states and volume mesh coordinates, i.e., [dR/dW]^T * psi, [dR/dXv]^T * psi
- `solve_linear()`: Solves adjoint equations [dR/dw]^T * ψ = [dF/dw]^T

**Inputs** (defined by `inputInfo` in daOption):
- Design variables (shape, angle of attack, flow conditions, etc.)
- Volume coordinates (e.g., `aero_vol_coords`) if mesh warping is enabled

**Outputs** (defined by `outputInfo` in daOption):
- State variables (aero_states for coupling with other solvers)
- Function values (for optimization)

A typical DAFoamSolver component (`solver`) can be seen in the Fig. 1 above.

**Primal and Adjoint Solution Pipeline**:

The DAFoamSolver orchestrates the flow and adjoint computations through OpenMDAO's implicit component interface:

*Primal Pipeline* (Forward Pass):
1. **`setup()`**: Declares input/output variables for the solver
2. **OpenMDAO calls DAFoamSolver's `solve_nonlinear()` method**:
   - Calls `DASolver()` (PYDAFOAM object) to solve primal equations
   - The PYDAFOAM object's internal `__call__` method calls C++ DASolver via Cython to execute the flow solver (e.g., DASimpleFoam)
   - Returns converged state variables `aero_states` satisfying residual: `R = 0`
   - Call DAFoamFunctions's `compute` method and return the objective and constraint functions

*Adjoint Pipeline* (Reverse Pass for Sensitivity Analysis):
1. **OpenMDAO enters reverse mode**
2. **`linearize()` is skipped** - DAFoam uses Jacobian-free adjoint method
3. **DAFoamFunctions**:
   - Computes partial derivatives `dF/dw` and `dF/dx`
   - This is done by calling the `compute_jacvec_product()` method in DAFoamFunctions
4. **`apply_linear()`**:
   - Computes matrix-vector products: `[dR/dw]^T * psi` and `[dR/dx]^T * psi`
   - apply_linear calls C++ routine `calcJacTVecProduct` defined in `pyDASolvers.so` to compute these products without explicitly forming Jacobian matrices
4. **`solve_linear()` **:
   - Solves the adjoint equation: `[dR/dw]^T * ψ = [dF/dw]^T`
   - Calls `solveLinearEqn()` to solve the adjoint system
   - Returns adjoint variables `ψ`
5. **Compute total derivatives**: Once `ψ` is available, the total derivatives are computed as: `total = dF/dx - [dR/dx]^T * ψ`.

**Example Flow for an Optimization Step**:
```
Optimizer
  ↓
OpenMDAO Problem.compute_totals()
  ↓
[Forward Pass] DAFoamSolver.solve_nonlinear() → PYDAFOAM() → C++ DASolver (primal flow solve)
  ↓
[Reverse Pass]
  - DAFoamFunctions.compute_jacvec_product() → compute dF/dx and dF/dw
  - DAFoamSolver.solve_linear() → [dR/dw]^T * ψ = [dF/dw]^T → C++ adjoint solve for ψ
  - DAFoamSolver.apply_linear() → compute [dR/dx]^T * ψ
  - Compute total deriv → dF/dx - [dR/dx]^T * ψ
  ↓
Optimizer receives total derivatives to update the design variables
```

This design provides:
- **Efficiency**: Jacobian-free adjoint avoids storing large matrices
- **Accuracy**: Automatic differentiation through C++ ensures consistent derivatives
- **Modularity**: Each component computes only its local derivatives

#### DAFoamWarper

**Purpose**: An ExplicitComponent that performs volume mesh deformation using IDWarp ([mphys_dafoam.py:797-853](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L797-L853)).

**Functionality**:
- Takes surface coordinates (`x_aero`) as input
- Outputs deformed volume mesh coordinates (`aero_vol_coords`)
- Used for geometry-related design variables and aero-structural coupling

DAFoamWarper is called by these two components mentioned above:
- **DAFoamPrecouplingGroup**: Deforms mesh based on geometry DVs before primal solve. See the `aero_pre` component in Fig. 1.
- **DAFoamGroup**: Deforms mesh inside coupling loop (aerostructural/aerothermal). See the `deformer` component in Fig. 2 right.

#### DAFoamFunctions

**Purpose**: An ExplicitComponent that computes objective and constraint function values ([mphys_dafoam.py:680-795](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L680-L795)).

**Inputs**:
- States (aero_states from DAFoamSolver): Flow solution variables
- Volume coordinates (if mesh warping is enabled): Deformed mesh
- Other design variables defined in `inputInfo`

**Outputs**:
- Function values defined in `daOption["function"]` (e.g., CD, CL, totalPressure, etc.)

**Key Methods**:
- `compute()`: Evaluates functions defined in `daOption["function"]`
- `compute_jacvec_product()`: Computes function derivatives (dF/dx, dF/dw)

**Examples of Functions**:
- Forces: CD (drag), CL (lift), CMX/CMY/CMZ (moments)
- Thermodynamic: totalPressure, totalTemperature, massFlowRate
- Geometric: volume, area, location
- Custom: user-defined functions via DAFunction classes

A typical DAFoamFunctions component (`aero_post`) can be seen in the Fig. 1 above.

#### DAFoamForces

**Purpose**: An ExplicitComponent that extracts surface forces for aerostructural coupling ([mphys_dafoam.py:997-1098](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L997-L1098)).

**Inputs**:
- States (aero_states): Flow solution variables
- Volume coordinates (aero_vol_coords): Deformed mesh

**Outputs**:
- `f_aero`: Surface nodal forces for structural solver

**Derivatives**:
- `df_aero/daero_states`: Force sensitivity to flow states
- `df_aero/daero_vol_coords`: Force sensitivity to mesh coordinates

A typical DAFoamForces component (`forces`) can be seen in the Fig. 2 right.

#### DAFoamThermal

**Purpose**: An ExplicitComponent that extracts surface thermal coupling vars for aerothermal coupling ([mphys_dafoam.py:855-945](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L855-L945)).

**Inputs**:
- States (aero_states): Flow solution variables
- Volume coordinates (aero_vol_coords): Deformed mesh

**Outputs**:
- `T_conduct` or `q_convect`: Thermal coupling variables, could be either the near wall temperature or heat transfer parameters.

**Functionality**:
- Computes surface heat flux from flow solution
- Transfers thermal loads to structural thermal solver
- Similar structure to DAFoamForces but for thermal quantities

#### DAFoamMesh

**Purpose**: An ExplicitComponent that provides initial surface mesh coordinates ([mphys_dafoam.py:607-678](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys/mphys_dafoam.py#L607-L678)). Note: this component does not have any inputs. In other words, this component will never change the initial geometry.

**Output**: `x_aero0` - Initial aerodynamic surface coordinates before any deformation

### Geometry Parameterization

Geometry parameterization is handled outside the DAFoam components and is defined in the `runScript.py` script. The process involves three key steps:

#### Geometry Definition (runScript.py)

In the user's `runScript.py`, the geometry is parameterized using `pyGeo` (DVGeometry) and `OM_DVGEOCOMP`. For example:

```python
# Add the geometry component with FFD parameterization
self.add_subsystem("geometry", OM_DVGEOCOMP(file="FFD/wingFFD.xyz", type="ffd"))
# The following two calls connect surface coords between mesh-geo and geo-scenario. Check Fig. 1 above
self.connect("mesh.x_aero0", "geometry.x_aero_in")
self.connect("geometry.x_aero0", "scenario1.x_aero")
```

The geometry component takes the initial surface coordinates (`x_aero0`) from DAFoamMesh and outputs the deformed coordinates (`x_aero0`) based on design variable changes (e.g., FFD control points, shape functions, etc.). `OM_DVGEOCOMP` is defined in in the [pyGeo repo](https://github.com/mdolab/pygeo): `pygeo/mphys/mphys_pygeo.py`.

#### Design Variables (DVS) Component Setup

Design variables are added to the problem via the `dvs` (design variable system) component, which is an `IndepVarComp` that serves as the top-level source for all design variables. Again `dvs` has no inputs.

```python
# From runScript.py
self.add_subsystem("dvs", om.IndepVarComp(), promotes=["*"])
self.dvs.add_output("shape", val=np.array([0] * len(shapes)))
self.dvs.add_output("patchV", val=np.array([U0, aoa0]))
# other connections calls
```

The `dvs` component is promoted to the top level (via `promotes=["*"]`), making its outputs directly available to all downstream components (geometry, scenario, etc.). This allows the optimizer to directly manipulate design variables without intermediate connections.

#### Mesh Deformation Pipeline

The mesh deformation process follows this pipeline:

1. **Design Variables** (DVS component): Specify shape, FFD control points, twist angle, etc.
2. **Geometry Component** (pyGeo/OM_DVGEOCOMP): Deforms the surface mesh based on design variables
3. **Warper** (DAFoamWarper): Uses IDWarp to propagate surface deformations to the volume mesh
4. **DAFoam Solver** (DAFoamSolver): Receives deformed volume mesh coordinates (`aero_vol_coords`) as input

This separation keeps geometry parameterization flexible and independent from the flow solver, allowing users to easily swap between different parameterization strategies (FFD, CST, spline-based, etc.) without modifying DAFoam code.

## Key Takeaways

1. **DAFoamBuilder** is the entry point - it creates and configures all components
2. **DAFoamSolver** is an implicit component - it solves both primal and adjoint equations
3. **Component modularity** - Each component has a single responsibility (solver, warper, functions, coupling)
4. **Automatic differentiation** - Partial derivatives are computed automatically through C++ layer
5. **MPhys integration** - Standard builder API enables easy integration with MDO frameworks
6. **Flexible coupling** - Supports aerodynamic, aerostructural, and aerothermal scenarios



{% include links.html %}

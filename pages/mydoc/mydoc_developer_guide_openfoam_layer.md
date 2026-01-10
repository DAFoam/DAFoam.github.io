---
title: OpenFOAM Layer
keywords: developer guide
summary:
sidebar: mydoc_sidebar
permalink: developer-guide-openfoam-layer.html
folder: mydoc
---

This chapter was written by [Ping He](https://github.com/friedenhe).

# OpenFOAM Layer Architecture

The OpenFOAM layer (`src/adjoint`) is the core C++ implementation of DAFoam's discrete adjoint solver. It is responsible for computing sensitivities, managing state variables, and coordinating primal and adjoint computations. This layer bridges OpenFOAM's physics solvers with DAFoam's optimization framework.

## Core Architecture:

The `src/adjoint` directory contains 22 major classes, each with specific responsibilities. Here we first elaborate on the main entry point class: DASolver.

### DASolver: Core Primal/Adjoint Solver Class (main entry point of the C++ layer)

**Purpose:** Abstract base class and master orchestrator that coordinates all primal and adjoint computations across different OpenFOAM solvers.

**Key Files:**
- `DASolver.H` - Base class declaration
- `DASolver.C` - Base class implementation (~4381 lines)
- `DASolver/*/` - Solver-specific child class directories

---

## DASolver Class Hierarchy

DASolver uses **runtime polymorphism** to support multiple OpenFOAM solvers. Each solver has its own child class that inherits from DASolver and implements solver-specific logic.

### Class Hierarchy Structure

```
DASolver (Abstract Base)
├── DASimpleFoam          Steady incompressible flow (SIMPLE)
├── DARhoSimpleFoam       Steady compressible flow (SIMPLE)
├── DARhoSimpleCFoam      Steady compressible (consistent formulation)
├── DAPimpleFoam          Transient incompressible flow (PIMPLE)
├── DAPimpleDyMFoam       Transient incompressible with dynamic mesh
├── DARhoPimpleFoam       Transient compressible flow (PIMPLE)
├── DAInterFoam           Two-phase flow (volume of fluid)
├── DAScalarTransportFoam Passive scalar transport
├── DASolidDisplacementFoam Solid mechanics / structural
├── DAHeatTransferFoam    Heat transfer analysis
├── DATurboFoam           Turbomachinery (with MRF)
├── DAHisaFoam            Hybrid RANS-LES advanced turbulence
├── DATopoChtFoam         Conjugate heat transfer topology optimization
└── DAIrkPimpleFoam       Implicit Runge-Kutta PIMPLE (advanced time integration)
```

### Runtime Selection Mechanism

The solver type is selected at runtime using OpenFOAM's registration tables. Here's the complete implementation:

#### Entry Point from Python Layer

**File:** [DASolvers.C, line 22](https://github.com/mdolab/dafoam/blob/v4.0.3/src/pyDASolvers/DASolvers.C#L22)

The Python wrapper (`DASolvers` class) calls:

```cpp
// In DASolvers constructor
DASolverPtr_.reset(DASolver::New(argsAll, pyOptions));
```

This is called from the Cython layer (`pyDASolvers.pyx`) which interfaces with Python.

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">
<a data-toggle="collapse" href="#cfdCode">DASolver Initialization: Complete Flow (click to expand)</a>
</h4>
</div>
<div id="cfdCode" class="panel-collapse collapse">
<div class="panel-body">

1. Python Calls the Cython Layer

From Python user script (e.g., `runScript.py`):

```python
# Python dictionary with solver configuration
daOptions = {
    "solverName": ["str", "DASimpleFoam"],
    "primalMinResTol": ["float", 1e-7],
    "primalMinIters": ["int", 10],
    # ... more options ...
}

# Call Cython wrapper
pyDASolvers_instance = pyDASolvers(daOptions)
```

2. Cython Calls C++ DASolver::New()

**File:** [pyDASolvers.pyx](https://github.com/mdolab/dafoam/blob/v4.0.3/src/pyDASolvers/pyDASolvers.pyx)

The Cython code converts Python dictionary to C++ and calls:

```cpp
// In C++ wrapper class DASolvers
DASolverPtr_.reset(DASolver::New(argsAll, pyOptions));
```

3. DASolver::New() Routes to Correct Child Class

**File:** [DASolver.C, lines 111-141](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DASolver/DASolver.C#L111-L141)

The `New()` method:
1. Reads `"solverName"` from pyOptions dictionary
2. Searches runtime selection table for matching constructor
3. Calls the constructor of the appropriate child class

4. Base Class Constructor Initializes Common Infrastructure

**File:** [DASolver.C, lines 35-107](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DASolver/DASolver.C#L35-L107)

```cpp
DASolver::DASolver(
    char* argsAll,
    PyObject* pyOptions)
    : argsAll_(argsAll),
      pyOptions_(pyOptions),
      // ... member initializations ...
{
    // Lines 57-60: Set up OpenFOAM Time and Mesh
    #include "setArgs.H"
    #include "setRootCasePython.H"

    // Lines 64-66: Create DAOption from Python options
    daOptionPtr_.reset(new DAOption(meshPtr_(), pyOptions_));

    // Lines 72-101: Extract solver options
    dictionary allOptions = daOptionPtr_->getAllOptions();
    primalMinResTol_ = daOptionPtr_->getOption<scalar>("primalMinResTol");
    primalMinIters_ = daOptionPtr_->getOption<label>("primalMinIters");
    // ... extract more options ...
}
```

5. Child Class Constructor Initializes Solver-Specific Components

**File:** [DASimpleFoam.C, lines 41-78](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DASolver/DASimpleFoam/DASimpleFoam.C#L41-L78)

```cpp
DASimpleFoam::DASimpleFoam(
    char* argsAll,
    PyObject* pyOptions)
    : DASolver(argsAll, pyOptions),  // Line 44: Call base class constructor
      // ... member initializations ...
{
    // Solver-specific initialization
    // Fields, models, and parameters are initialized here
}
```

6. Python Gets Reference to DASolver Instance

The Cython wrapper returns a handle to the C++ DASolver object, which Python can use for:
- Calling `solvePrimal()` to run CFD simulations
- Calling `calcJacTVecProduct()` to compute sensitivities
- Querying objective function values

</div>
</div>
</div>

### Pure Virtual Methods initSolver() and runPrimal() (Must be Implemented by Child Classes)

Child classes **must** override these methods:

```cpp
// Solver initialization - sets up all solver-specific fields and models
virtual void initSolver() = 0;

// Main primal solution routine - runs the OpenFOAM solver
virtual label solvePrimal() = 0;
```

#### Critical Method: calcJacTVecProduct

This is the heart of the adjoint computation using **reverse-mode automatic differentiation**.

**Signature:**
```cpp
void calcJacTVecProduct(
    const word inputName,          // Name of input (e.g., "PatchVelocity")
    const word inputType,          // Type (e.g., "patch", "field")
    const double* input,           // Input design variable values
    const word outputName,         // Output (e.g., "Force")
    const word outputType,         // Output type
    const double* seed,            // Seed vector (RHS)
    double* product)               // Result: dOutput/dInput^T * seed
```

**What It Computes:**

This method computes the transpose Jacobian-vector product. The discrete adjoint method requires computing matrix-vector products with the transpose Jacobian. Instead of forming the full Jacobian matrix (which is expensive and memory-intensive), `calcJacTVecProduct` uses reverse-mode AD.

```
product = [dOutput/dInput]^T * seed
```

More specifically:
- If output is a function F and input is a design variable X:
  ```
  product = (∂F/∂X)^T * seed = (∂F/∂X) * seed
  ```
- If output is state U and input is design variable X:
  ```
  product = (∂U/∂X)^T * seed
  ```

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">
<a data-toggle="collapse" href="#cfdCode">Detailed Implementation Flow for calcJacTVecProduct (click to expand)</a>
</h4>
</div>
<div id="cfdCode" class="panel-collapse collapse">
<div class="panel-body">

**:**

```cpp
1. Create Input/Output Objects
   ├─> DAInput: Converts design variable array to OpenFOAM field
   │   └─> Example: DAInputPatchVelocity, DAInputVolCoord
   └─> DAOutput: Computes output from fields
       └─> Example: DAOutputFunction (drag, lift, etc.)

2. Reset and Prepare AD Tape
   ├─> Clear CoDiPack tape
   ├─> Activate tape for recording
   └─> Set tape mode to "overwrite" to reuse memory

3. Forward Sweep (Tape Recording)
   ├─> Register input design variables with AD tape
   │   └─> setAD(globalADTape_) on input array
   │
   ├─> Execute daInput->run(inputList)
   │   └─> Updates OpenFOAM fields from input array
   │       Example: Boundary conditions, mesh displacement
   │
   ├─> Update mesh and boundary conditions
   │   ├─> meshMovement if necessary
   │   └─> correctBoundaryConditions()
   │
   ├─> Execute daOutput->run(outputList)
   │   └─> Computes outputs (functions, field values, etc.)
   │       All operations recorded on AD tape
   │
   └─> Register output values with AD tape
       └─> extractGradient() from output array

4. Reverse Sweep (Differentiation)
   ├─> Assign seed values to output derivatives
   │   └─> globalADTape_.setGradient(output_index, seed_value)
   │
   ├─> Execute reverse sweep
   │   └─> globalADTape_.evaluate()
   │       Computes ∂output/∂input for all intermediate values
   │
   └─> Deactivate tape (setPassive)

5. Extract Gradient to Output Vector
   ├─> assignStateGradient2Vec(input_array, product_vector)
   └─> product = [∂output/∂input]^T * seed
```
</div>
</div>
</div>


#### 5. Linear Equation Solving

```cpp
label solveLinearEqn(const KSP ksp, const Vec rhsVec, Vec solVec)
```

- Solves linear systems using PETSc Krylov Subspace methods
- Used for:
  - Adjoint equation solution
  - Implicit adjoint coupling
  - Preconditioner applications
- Deactivates AD after solution

## Complete Execution Flow: From Python to Gradients

```
Python Optimizer (e.g., OpenMDAO/pyOptSparse/SNOPT)
    │
    ├─> 1. Create DASolver
    │   └─> daSolver = DASolver::New(pyOptions)
    │       └─> Selects child class (e.g., DASimpleFoam)
    │
    ├─> 2. Initialize solver
    │   └─> daSolver->initSolver()
    │       ├─> daOption->read(pyOptions)
    │       ├─> daModel->initialize()
    │       ├─> daStateInfo->initialize()
    │       └─> Child_daSolver->initSolver()
    │           └─> Creates U, p, phi, turbulence model
    │
    ├─> 3. Run primal solver
    │   └─> daSolver->solvePrimal()
    │       ├─> (DASimpleFoam) SIMPLE iteration loop
    │       ├─> Solve momentum and pressure equations
    │       ├─> Update turbulence model
    │       └─> Compute objective functions
    │
    ├─> 4. Compute objectives
    │   └─> daSolver->calcAllFunctions()
    │       └─> F_drag = ∫_wall (p + τ) dA
    │
    ├─> 5. For each design variable:
    │   └─> daSolver->calcJacTVecProduct()
    │       ├─> Create DAInput, DAOutput
    │       ├─> Activate AD tape
    │       ├─> Forward sweep: meshDisp → field updates → F
    │       ├─> Reverse sweep: F → ∂F/∂meshDisp
    │       └─> product = ∂F/∂meshDisp^T * λ
    │
    └─> 6. Return gradient vector to optimizer
        └─> Optimizer updates design variables
```

---

## Summary: DASolver Architecture

**DASolver provides:**
1. **Abstraction layer** for multiple OpenFOAM solvers through inheritance
2. **Base functionality** shared by all solvers (adjoint solving, AD infrastructure)
3. **Extensibility** - new solvers added by creating child class with two methods
4. **Adjoint computation** via reverse-mode AD through `calcJacTVecProduct`
5. **Residual management** coordinated with DAResidual child classes

---

## Summary: Architecture Overview

| Class | Role | Key Output |
|-------|------|-----------|
| DASolver | Orchestrator | Sensitivities dF/dX |
| DAOption | Configuration | Options dictionary |
| DAModel | Physics | Turbulence derivatives |
| DAIndex | Indexing | State variable mapping |
| DAField | Fields | Field-vector conversion |
| DAResidual | Residuals | R and ∂R/∂U |
| DAStateInfo | Registration | State variable metadata |
| DAFunction | Objectives | F and ∂F/∂U |
| DAInput | Design Vars | Field perturbations |
| DAJacCon | Sparsity | Coloring strategy |
| DALinearEqn | Solve | Adjoint variables λ |
| DAMisc | Extensions | Modified BC/schemes |

This class hierarchy enables DAFoam to support multiple solvers, physics models, and optimization scenarios while maintaining code reusability and extensibility.

{% include links.html %}

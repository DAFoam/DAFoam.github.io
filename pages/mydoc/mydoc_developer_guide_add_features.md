---
title: How to Add a New Feature
keywords: developer guide
summary:
sidebar: mydoc_sidebar
permalink: developer-guide-add-features.html
folder: mydoc
---

# Developer Guide: Adding New Features to DAFoam

DAFoam's unified architecture with a single library and standardized interfaces makes adding new features significantly faster. This guide covers the most common extension points.

---

## 1. Add a New C++ Parameter (DAOption)

Parameters in DAFoam are centrally managed through the `DAOption` class, which bridges Python and C++ configuration.

### Step 1: Add Default Value in Python Layer

**File:** [dafoam/pyDAFoam.py](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/pyDAFoam.py)

In the `DAOPTION` class `__init__` function:

```python
# Provide default values - DAFoam infers type from the value
self.testOption = 3.0           # float parameter
self.testIntOption = 10         # int parameter
self.testStringOption = "test"  # str parameter
self.testListOption = [1.0, 2.0, 3.0]  # list parameter
# For dict options, leave empty (no default needed)
self.testDictOption = {}
```

**Why this matters:**
- Default values help DAFoam determine the data type
- These are used when users don't override the option
- Options are passed to C++ layer during initialization

### Step 2: Access in C++ Code

**File:** Any C++ source file in `src/adjoint/`

```cpp
// Example: DASimpleFoam.C
scalar testOption = daOptionPtr_->getOption<scalar>("testOption");
label testIntOption = daOptionPtr_->getOption<label>("testIntOption");
word testStringOption = daOptionPtr_->getOption<word>("testStringOption");
scalarList testListOption = daOptionPtr_->getOption<scalarList>("testListOption");

Info << "My test option is: " << testOption << endl;
```

**Key methods:**
- `getOption<T>(name)` - Get option value
- `setOption<T>(name, value)` - Set option value
- `getAllOptions()` - Get dictionary of all options

### Step 3: Override in User Script

**File:** `runScript.py`

```python
daOptions = {
    "solverName": "DASimpleFoam",
    "testOption": 15.2,
    "testIntOption": 20,
    "testStringOption": "mytest",
    "testListOption": [1.5, 2.5, 3.5],
    # ... other options
}
```

### Step 4: Update Option Dynamically (If Needed)

Since options are passed only once during initialization, to update them dynamically later in the optimization, you can run:

```cpp
// In C++ code
daOptionPtr_->updateDAOption(name, newValue);
```

---

## 2. Add a New C++ Function and Expose to Python

This requires modifications across all three layers of DAFoam: C++, Cython, and Python.

### Three-Layer Modification Workflow

#### Layer 1: Add Method in C++ Base Class

**File:** [src/adjoint/DASolver/DASolver.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DASolver/DASolver.H)

Add to the `DASolver` class (in public section):

```cpp
// Print mesh information - example function
void printMeshSize()
{
    label nCells = meshPtr_->nCells();
    label nPoints = meshPtr_->nPoints();
    label nFaces = meshPtr_->nFaces();

    Info << "Mesh Statistics:" << endl;
    Info << "  Cells: " << nCells << endl;
    Info << "  Points: " << nPoints << endl;
    Info << "  Faces: " << nFaces << endl;
}
```

#### Layer 2: Wrap in Cython Wrapper Class

**File:** [src/pyDASolvers/DASolvers.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/pyDASolvers/DASolvers.H)

Add to `DASolvers` class:

```cpp
void printMeshSize()
{
    DASolverPtr_->printMeshSize();
}
```

**File:** [src/pyDASolvers/pyDASolvers.pyx](https://github.com/mdolab/dafoam/blob/v4.0.3/src/pyDASolvers/pyDASolvers.pyx)

In the Cython `cppclass` declaration:

```cython
cppclass DASolvers:
    void printMeshSize()
```

Add Python wrapper:

```cython
def printMeshSize(self):
    """Expose printMeshSize to Python."""
    self._thisptr.printMeshSize()
```

#### Layer 3: Expose in Python Interface

**File:** [dafoam/pyDAFoam.py](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/pyDAFoam.py)

In the `DAFOAM` class `__call__` method:

```python
def printMeshSize(self):
    """Print mesh size statistics."""
    self.solver.printMeshSize()
```

### Usage in runScript.py

```python
prob.run_model()
prob.model.scenario1.coupling.solver.DASolver.printMeshSize()
```

---

## 3. Add a New Objective/Constraint Function (DAFunction)

DAFoam automatically computes adjoint derivatives for new functions using automatic differentiation, so you only need to implement the function value computation.

### Step 1: Create New Function Class

**File:** Create `src/adjoint/DAFunction/DAFunctionCustom.H`

Reference actual implementations: [DAFunctionForce.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAFunction/DAFunctionForce.H), [DAFunctionMassFlowRate.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAFunction/DAFunctionMassFlowRate.H)

```cpp
/*---------------------------------------------------------------------------*\
    DAFoam  : Discrete Adjoint with OpenFOAM
\*---------------------------------------------------------------------------*/

#ifndef DAFunctionCustom_H
#define DAFunctionCustom_H

#include "DAFunction.H"
#include "addToRunTimeSelectionTable.H"

namespace Foam
{

class DAFunctionCustom : public DAFunction
{
protected:
    /// DATurbulenceModel object
    const DATurbulenceModel& daTurb_;

public:
    TypeName("custom");  // Name used in daOptions["function"]["functionName"]["type"]

    //- Construct from components
    DAFunctionCustom(
        const fvMesh& mesh,
        const DAOption& daOption,
        const DAModel& daModel,
        const DAIndex& daIndex,
        const word functionName);

    //- Destructor
    virtual ~DAFunctionCustom()
    {
    }

    /// Calculate the value of objective function
    virtual scalar calcFunction();
};

} // End namespace Foam

#endif
```

**File:** Create `src/adjoint/DAFunction/DAFunctionCustom.C`

Reference actual implementation: [DAFunctionForce.C](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAFunction/DAFunctionForce.C)

```cpp
/*---------------------------------------------------------------------------*\
    DAFoam  : Discrete Adjoint with OpenFOAM
\*---------------------------------------------------------------------------*/

#include "DAFunctionCustom.H"

namespace Foam
{

defineTypeNameAndDebug(DAFunctionCustom, 0);
addToRunTimeSelectionTable(DAFunction, DAFunctionCustom, dictionary);

DAFunctionCustom::DAFunctionCustom(
    const fvMesh& mesh,
    const DAOption& daOption,
    const DAModel& daModel,
    const DAIndex& daIndex,
    const word functionName)
    : DAFunction(
        mesh,
        daOption,
        daModel,
        daIndex,
        functionName),
      daTurb_(daModel.getDATurbulenceModel())
{
    // Constructor logic specific to your function
}

scalar DAFunctionCustom::calcFunction()
{
    /*
    Description:
        Compute your custom objective function value.
        This function is called during optimization.
        DAFoam automatically computes derivatives dF/dU and dF/dX
        using reverse-mode automatic differentiation.

    Output:
        Returns scalar function value (automatically reduced across processors)
    */

    // Example: compute maximum velocity magnitude
    const volVectorField& U = mesh_.thisDb().lookupObject<volVectorField>("U");

    scalar maxVelocity = 0.0;
    forAll(U, cellI)
    {
        maxVelocity = max(maxVelocity, mag(U[cellI]));
    }

    // Reduce across all processors if running in parallel
    reduce(maxVelocity, maxOp<scalar>());

    // Scale output if specified in daOptions
    scalar scale = functionDict_.getScalar("scale", 1.0);

    return maxVelocity * scale;
}

} // End namespace Foam
```

### Step 2: Register in Build System

**File:** [src/adjoint/Make/files](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/Make/files)

Add line:

```
DAFunction/DAFunctionCustom.C
```

### Step 3: Use in runScript.py

```python
daOptions = {
    "function": {
        "custom_obj": {
            "type": "custom",        # Must match TypeName
            "patches": ["wing"],     # Patches to use
            "scale": 1.0             # Scaling factor
        }
    }
}

# In configure() function (for OpenMDAO):
self.add_objective("custom_obj", scaler=1.0, ref=1.0)
```

**Important:** DAFoam automatically computes derivatives `dF/dU` and `dF/dX` using reverse-mode automatic differentiation. You only implement `calcFunction()`!

---

## 4. Add a New Design Variable/Input (DAInput)

Design variables (inputs) control what parameters the optimizer can modify. DAFoam automatically computes `dR/dX` and `dF/dX` for any new input using automatic differentiation.

### Step 1: Create New Input Class

**File:** Create `src/adjoint/DAInput/DAInputCustom.H`

Reference actual implementations: [DAInputVolCoord.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAInput/DAInputVolCoord.H), [DAInputPatchVelocity.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAInput/DAInputPatchVelocity.H)

```cpp
/*---------------------------------------------------------------------------*\
    DAFoam  : Discrete Adjoint with OpenFOAM
\*---------------------------------------------------------------------------*/

#ifndef DAInputCustom_H
#define DAInputCustom_H

#include "DAInput.H"
#include "addToRunTimeSelectionTable.H"

namespace Foam
{

class DAInputCustom : public DAInput
{
protected:
    // Any custom member variables for your input type
    label patchID_;

public:
    TypeName("custom");  // Name used in daOptions["inputInfo"]["inputName"]["type"]

    //- Construct from components
    DAInputCustom(
        const word inputName,
        const word inputType,
        fvMesh& mesh,
        const DAOption& daOption,
        const DAModel& daModel,
        const DAIndex& daIndex);

    //- Destructor
    virtual ~DAInputCustom()
    {
    }

    /// Assign input array values to OpenFOAM fields
    virtual void run(const scalarList& input);

    /// Return number of design variables for this input
    virtual label size()
    {
        // Return the number of design variables this input controls
        return 1;  // Example: single scalar parameter
    }

    /// Return 1 if distributed across processors, 0 if global
    virtual label distributed()
    {
        return 0;  // Global variable (not distributed)
    }
};

} // End namespace Foam

#endif
```

**File:** Create `src/adjoint/DAInput/DAInputCustom.C`

Reference actual implementation: [DAInputVolCoord.C](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAInput/DAInputVolCoord.C)

```cpp
/*---------------------------------------------------------------------------*\
    DAFoam  : Discrete Adjoint with OpenFOAM
\*---------------------------------------------------------------------------*/

#include "DAInputCustom.H"

namespace Foam
{

defineTypeNameAndDebug(DAInputCustom, 0);
addToRunTimeSelectionTable(DAInput, DAInputCustom, dictionary);

DAInputCustom::DAInputCustom(
    const word inputName,
    const word inputType,
    fvMesh& mesh,
    const DAOption& daOption,
    const DAModel& daModel,
    const DAIndex& daIndex)
    : DAInput(
        inputName,
        inputType,
        mesh,
        daOption,
        daModel,
        daIndex),
      patchID_(-1)
{
    // Constructor logic specific to your input type
    // Example: get patch ID from inputInfo
    dictionary inputDict = daOption_.getAllOptions().subDict("inputInfo").subDict(inputName);
    word patchName = inputDict.getWord("patch");
    patchID_ = mesh_.boundaryMesh().findPatchID(patchName);

    if (patchID_ < 0)
    {
        FatalErrorIn("DAInputCustom::DAInputCustom")
            << "Patch " << patchName << " not found!"
            << abort(FatalError);
    }
}

void DAInputCustom::run(const scalarList& input)
{
    /*
    Description:
        Assign input design variable values to OpenFOAM fields.
        This is called during each optimization iteration.
        DAFoam automatically computes derivatives dR/dInput and dF/dInput
        using reverse-mode automatic differentiation.

    Input:
        input: array of design variable values from optimizer
    */

    // Example: modify boundary condition on a patch
    volVectorField& U = mesh_.thisDb().lookupObjectRef<volVectorField>("U");

    vectorField& UPatch = U.boundaryFieldRef()[patchID_];

    // Assign x-component of velocity from input[0]
    forAll(UPatch, faceI)
    {
        UPatch[faceI].x() = input[0];
    }

    // Update boundary conditions to enforce changes
    U.correctBoundaryConditions();

    return;
}

} // End namespace Foam
```

### Step 2: Register in Build System

**File:** [src/adjoint/Make/files](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/Make/files)

Add line:

```
DAInput/DAInputCustom.C
```

### Step 3: Use in runScript.py

```python
daOptions = {
    "inputInfo": {
        "custom_var": {            # Design variable name
            "type": "custom",      # Must match TypeName
            "patch": "inlet"       # Patch to modify
        }
    }
}

# In configure() function (for OpenMDAO):
self.add_input("custom_var", val=np.array([10.0]))
self.add_design_var("custom_var", lower=1.0, upper=50.0, scaler=0.1)
```

**Automatic features:**
- Partial derivatives `dR/dX` and `dF/dX` computed automatically
- AD tape automatically records all field operations in `run()`
- Integrated with adjoint sensitivity computation

---

## 5. Add a New Boundary Condition

Custom boundary conditions can be added to the DAMisc directory.

**File:** `src/adjoint/DAMisc/myCustomBC.H` and `myCustomBC.C`

```cpp
// Copy from OpenFOAM template and modify TypeName
TypeName("myCustomBCName");  // Must be unique, not conflict with OpenFOAM
```

**File:** [src/adjoint/Make/files](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/Make/files)

```
DAMisc/myCustomBC.C
```

Recompile and use in OpenFOAM boundary file with the custom TypeName.

---

## 6. Add a New Turbulence Model

Adding a new turbulence model requires two main components:

### Part 1: Create Dummy Model Class (if not in OpenFOAM)

**File:** `src/newTurbModels/models/mySA.H` and `mySA.C`

Keep only:
- Initialization of turbulence variables (`nuTilda_`, `k_`, `omega_`)
- All virtual functions with empty implementations
- Empty `correct()` method

**File:** `src/newTurbModels/compressible/makeMySACompressible.C`

```cpp
// Register compressible version
makeRASModel(mySA)

// Similarly for incompressible/incompressibleMakeMySA.C
```

### Part 2: Create DAFoam Adjoint-Compatible Version

**File:** [src/adjoint/DAModel/DATurbulenceModel/DAMySA.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAModel/DATurbulenceModel)

```cpp
class DAMySA : public DATurbulenceModel
{
public:
    TypeName("mySA");  // Name used in daOption["turbulenceModel"]

    DAMySA(...);
    virtual ~DAMySA(){};

    virtual void calcResiduals(const dictionary& options);
    virtual void correctBoundaryConditions();
    virtual void updateIntermediateVariables();
};
```

**File:** Create `src/adjoint/DAModel/DATurbulenceModel/DAMySA.C`

```cpp
void DAMySA::calcResiduals(const dictionary& options)
{
    // Implement turbulence model residuals
    // R_nuTilda = dP/dn - dD/dn  (Spalart-Allmaras example)

    const volScalarField& nuTilda = _;
    volScalarField& nuTildaRes_ = _;

    // Production term
    // Dissipation term
    // Etc.
}
```

**File:** [src/adjoint/Make/files](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/Make/files)

```
DAModel/DATurbulenceModel/DAMySA.C
```

---

## 7. Add New MDO Coupling Variables

For multi-disciplinary optimization (e.g., aero-structural coupling), you need to expose coupling variables.

### Part 1: Create Output Extraction Class

**File:** `src/adjoint/DAOutput/DAOutputForceCoupling.H`

```cpp
class DAOutputForceCoupling : public DAOutput
{
public:
    TypeName("forceCoupling");

    label size() const { return nSurfaceNodes_ * 3; }  // 3D forces
    label distributed() const { return 1; }  // Each processor handles its own nodes

    virtual void calcOutput(...);
};
```

**File:** `src/adjoint/DAOutput/DAOutputForceCoupling.C`

```cpp
void DAOutputForceCoupling::calcOutput(...)
{
    // Extract surface nodal forces
    // Iterate over patches
    // Compute pressure and shear forces: F = (p*I + tau) * n
    // Assign to output array distributed across processors
}
```

### Part 2: Create Python Component

**File:** [dafoam/mphys/mphys_dafoam.py](https://github.com/mdolab/dafoam/blob/v4.0.3/dafoam/mphys)

```python
class DAFoamForces(om.ExplicitComponent):
    """Extract aerodynamic forces for structural coupling."""

    def setup(self):
        self.add_input("volume_coords", val=np.zeros(nVol*3), distributed=True)
        self.add_output("f_aero", val=np.zeros(nSurf*3), distributed=True)

    def compute(self, inputs, outputs):
        # Call C++ to extract forces
        self.DASolver.calcOutput("forceCoupling", inputs, outputs)

    def compute_jacvec_product(self, inputs, d_inputs, d_outputs, mode):
        # Compute derivatives for adjoint
        self.DASolver.calcJacTVecProduct("forceCoupling", ...)
```

Add to DAFoamGroup:

```python
group.add_subsystem("forces", DAFoamForces())
```

### Part 3: Configure in runScript.py

```python
daOptions["outputInfo"] = {
    "f_aero": {
        "type": "forceCoupling",
        "patches": ["surface"]
    }
}

# Connect to structural solver
prob.model.connect("aero.f_aero", "struct.f_aero")
```

---

## 8. Add a New Solver

Adding a completely new OpenFOAM solver requires three main classes:

### Components Needed

1. **DAStateInfo** - Register all state variables and their dependencies
2. **DAResidual** - Compute residual equations
3. **DASolver** - Main solver implementation (primal solution routine)

### Template Structure

**File:** [src/adjoint/DAStateInfo/DAStateInfoMyNewSolver.H](https://github.com/mdolab/dafoam/blob/v4.0.3/src/adjoint/DAStateInfo)

```cpp
class DAStateInfoMyNewSolver : public DAStateInfo
{
public:
    TypeName("MyNewSolver");

    DAStateInfoMyNewSolver(...);
    virtual ~DAStateInfoMyNewSolver(){};

    virtual void setStateInfo(dictionary& stateInfo);
};
```

Implement `setStateInfo()` to register state variables:

```cpp
void DAStateInfoMyNewSolver::setStateInfo(dictionary& stateInfo)
{
    stateInfo.set("U", {
        "type": volVectorField,
        "comps": 3,
        "function": "UEqn"
    });

    stateInfo.set("p", {
        "type": volScalarField,
        "comps": 1,
        "function": "pEqn"
    });
}
```

**File:** `src/adjoint/DAResidual/DAResidualMyNewSolver.C`

Implement residual computation for each equation.

**File:** `src/adjoint/DASolver/DAMyNewSolver/DAMyNewSolver.C`

Implement `solvePrimal()` - the main solver loop:

```cpp
label DAMyNewSolver::solvePrimal()
{
    while (this->loop(runTime))
    {
        // Solve all equations
        // Update fields
        // Check convergence
    }
    return 0;
}
```

---

## Build and Test

### Build

```bash
cd $HOME/dafoam/repos/dafoam
./Allmake
```

**Advantages of v4:**
- First build: ~10 minutes
- Rebuild after changes: <<10 minutes
- Automatic parallel build on all CPU cores
- No need for `Allclean` - incremental compilation only rebuilds changed files

### Test Your Changes

```bash
cd $HOME/mount/examples/NACA0012/
./preProcessing.sh
python runScript_v4.py -task=run_model
```

---

## Key Design Principles

1. **Automatic Derivatives:** DAFoam automatically computes all partial derivatives for new functions and inputs using CoDiPack AD - you only implement the forward computation!

2. **Unified Library:** All solvers (incompressible, compressible, solid) compile to one library - easier maintenance and faster builds.

3. **Standardized Interfaces:** All new features follow the same pattern (Type, H/C files, registration), making code more consistent and maintainable.

4. **Type Names:** All classes have unique `TypeName()` which is used for runtime selection - make sure it doesn't conflict with existing OpenFOAM types.

5. **Registration:** Use `addToRunTimeSelectionTable()` macro to register new classes in OpenFOAM's runtime selection system.

---

## Example: Complete Workflow

To add a new function for maximum velocity:

1. **Create** `DAFunctionMaxVelocity.H/C` with `calcFunction()` computing `max(|U|)`
2. **Register** in `src/adjoint/Make/files`
3. **Build** with `./Allmake` (~30 seconds)
4. **Use** in `runScript.py` with type name
5. DAFoam automatically computes `dMaxVel/dU`, `dMaxVel/dX` - done!

{% include links.html %}

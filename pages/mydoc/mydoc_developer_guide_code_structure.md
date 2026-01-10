---
title: DAFoam Code Structure
keywords: developer guide
summary:
sidebar: mydoc_sidebar
permalink: developer-guide-code-structure.html
folder: mydoc
---

This chapter was written by [Ping He](https://github.com/friedenhe).

## Overview

DAFoam has a three-layer architecture consisting of C++, Cython, and Python layers. This design allows DAFoam to leverage the computational efficiency of C++ while providing a user-friendly Python interface for optimization workflows. Each layer takes source code or libraries as input in the vertical direction and outputs libraries to the horizontal direction.

## Three-Layer Architecture

<img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/dafoam_layers.png" style="width:1000px !important;" />

*Figure 1: DAFoam has three code layers: C++, Cython, and Python. Each layer takes source code or libraries as input in the vertical direction and outputs libraries to the horizontal direction.*

### C++ Layer

The C++ layer implements the core DAFoam functionality, including:
- Flow solvers and adjoint solvers
- Residual computations
- State variable management
- Objective/constraint functions
- Design variable inputs
- Turbulence models
- Boundary conditions

**Source Code Location:** `dafoam/src/adjoint/`

**Input:** OpenFOAM libraries (`OpenFOAM/platforms/linux64Gccxxxxxx/lib`). Note: DAFoam's C++ layer use OpenFOAM's libraries, such as libOpenFoam.so, libfiniteVolume.so.

**Output:** Three shared libraries, and they are saved to the `OpenFOAM/sharedLibs/` folder
- `libDASolver.so` - Main solver library
- `libDASolverADR.so` - Automatic differentiation (reverse mode) library
- `libDASolverADF.so` - Automatic differentiation (forward mode) library

### Cython Layer

The Cython layer does not do actual computation. Instead, it serves as the bridge between C++ and Python, providing:
- Python bindings to C++ classes and functions
- Type conversion between Python and C++ data structures
- Memory management across language boundaries

**Source Code Location:** `dafoam/src/pyDASolvers/`

**Input:** DAFoam's C++ layer libraries (`libDASolver*.so`)

**Output:** The Cython layer will compile the `pyDASolvers.so` libraries, and it is saved to the `dafoam/libs` folder. When, the `pip install .` command is run, this pyDASolvers.so lib will be copied to the miniconda's `site-packages/dafoam/` folder and become importable by the Python layer. Note: we have three versions of the Cython libs, and they are saved to `dafoam/libs/`, `dafoam/libs/ADR/`, `dafoam/libs/ADF/`.

### Python Layer

The Python layer provides the user-level API and MDO integration:
- OpenMDAO component definitions
- MPhys integration for multidisciplinary optimization
- High-level solver control and configuration
- Post-processing and visualization interfaces

**Source Code Location:** `dafoam/pyDAFoam.py`  (Main DAFoam solver interface) and `dafoam/mphys/mphys_dafoam.py` (MPhys integration for MDO coupling). When the `pip install .` command is run, these Python modules will be copied to the miniconda's `site-packages/dafoam/` folder and become importable

## Compilation Process

### Build Command

DAFoam uses a single, unified build command to compile the source:

```bash
./Allmake
```

**Notes:** DAFoam will conduct parallel build using maximum available cores, and it will intelligent incremental compilation and only rebuilds changed files. The first build will take ~10 minutes, and most of the bebuild will take around 1 minute.  Do NOT run `Allclean` before rebuilding. DAFoam automatically detects changes and compiles only modified files.

### Build Process Flow

1. **C++ Compilation**
   - Compiles source files in `src/adjoint/` against OpenFOAM libraries
   - Generates three shared libraries: `libDASolver.so`, `libDASolverADR.so`, `libDASolverADF.so`
   - Installs libraries to `OpenFOAM/sharedLibs/`

2. **Cython Compilation**
   - Compiles `src/pyDASolvers/pyDASolvers.pyx` with C++ libraries
   - Generates `pyDASolvers.so`
   - Installs to `dafoam/libs/` and subdirectories

3. **Python Installation**
   - Installs Python modules to `site-packages/dafoam/`
   - No compilation needed for pure Python files

## Testing and Continuous Integration

### GitHub Actions Workflows

DAFoam uses GitHub Actions for automated testing and deployment:

**Test Workflow:**
- Triggered on pull requests and commits
- Runs regression tests across multiple configurations
- Verifies compilation on different platforms
- Generates code coverage reports

**Code Coverage:**
- Integrated with Codecov
- Tracks C++ and Python test coverage
- Reports displayed in pull requests

**Deployment:**
- Automated Docker image builds - After successful tests, the latest DAFoam build is pushed to the `dafoam/opt-packages:latest` Docker image, making it available for users to pull and use

### Running Tests Locally

For any new changes, please make sure all the tests pass. Tests can be run from the DAFoam repository:

```bash
cd dafoam/tests
./Allrun
```

This runs the complete test suite including:
- Unit tests for individual components
- Integration tests for complete workflows
- Regression tests comparing against reference solutions


{% include links.html %}

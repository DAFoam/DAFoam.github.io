---
title: Background
keywords: developer guide
summary:
sidebar: mydoc_sidebar
permalink: developer-guide-background-try.html
folder: mydoc
---

## Computational Fluid Dynamics (General Introduction)

Computational Fluid Dynamics (CFD) is the numerical solution of the Navier--Stokes (NS) equations that describe fluid motion. The Navier--Stokes equations have no analytical solutions, so we need to solve them on a discretized domain (a mesh). The solution process typically starts with converting the continuous NS equations into the discretized form, reformulate the discretized NS equations into algebraic equations (i.e., matrix-vector product format; Ax=b), and then repeatedly solving large sparse algebraic systems to drive the discretized residuals (R=Ax-b) to zero.

This section shows a simple CFD example by using the finite-volume method to solve **steady-state, incompressible, laminar flow** in a lid-driven cavity.

---

### 1) Governing equations: incompressible, laminar Navier–Stokes (2D)

For this **2D lid-driven cavity example**, we solve the incompressible Navier–Stokes equations for a Newtonian fluid with constant density $\rho$ and viscosity $\mu$ in **steady state**:

**Continuity (mass conservation) - 2D**
$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0
$$

**Momentum equations (steady) - 2D**

$x$-momentum:
$$
\rho \left( u \frac{\partial u}{\partial x} + v \frac{\partial u}{\partial y} \right) = -\frac{\partial p}{\partial x} + \mu \left( \frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} \right)
$$

$y$-momentum:
$$
\rho \left( u \frac{\partial v}{\partial x} + v \frac{\partial v}{\partial y} \right) = -\frac{\partial p}{\partial y} + \mu \left( \frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2} \right)
$$

where:
- $u(x,y)$ is the horizontal (x-direction) velocity component
- $v(x,y)$ is the vertical (y-direction) velocity component
- $p(x,y)$ is pressure
- No body forces (no gravity, no external forces in this example)

**Why is this system difficult?**
- **Nonlinear**: The advection terms $u \frac{\partial u}{\partial x}$ and $v \frac{\partial u}{\partial y}$ make the equations nonlinear
- **Coupled**: The pressure $p$ is unknown and is determined by the constraint $\nabla \cdot \mathbf{u} = 0$ (continuity). There is no pressure equation, so we must enforce continuity indirectly through a coupling algorithm

---

### 2) Discretizing the domain: mesh and control volumes (2D)

For our **2D lid-driven cavity**, we use a structured **quadrilateral (quad) mesh** to discretize the square domain $[0,1] \times [0,1]$.

**Mesh concepts for 2D**

A mesh partitions the continuous 2D domain into small cells (control volumes). Each cell is a small rectangle where we will store and compute the unknowns ($u, v, p$).

**Key mesh terminology in 2D:**

- **Mesh cell (control volume)**: A small rectangular element in the 2D domain. For a uniform quad mesh, all cells are identical. Example: if we have $4 \times 4$ cells, each cell has width and height of $0.25 \times 0.25$ (since domain is $[0,1] \times [0,1]$).

- **Mesh face**: The boundary edge of a 2D cell. A rectangular cell has exactly **4 faces**:
  - **West face**: the left edge (at constant $x$)
  - **East face**: the right edge (at constant $x$)
  - **South face**: the bottom edge (at constant $y$)
  - **North face**: the top edge (at constant $y$)

  Each face has an associated length $L_f$ and an outward unit normal vector $\mathbf{n}_f$ (perpendicular to the face, pointing out of the cell).

- **Mesh center (cell center)**: The geometric center point of a cell $(x_c, y_c)$, where we store the main unknowns: $u(x_c, y_c)$, $v(x_c, y_c)$, and $p(x_c, y_c)$.

- **Cell area** $A_P$: In 2D, this is the physical area of the cell. For a uniform quad mesh, all cells have the same area. For our example with $n_x \times n_y$ cells: $A_P = \frac{1}{n_x} \times \frac{1}{n_y}$.

- **Face flux** $\phi_f$: The flow rate (volume per unit time per unit depth) crossing a face. Computed as:
  $\phi_f = u_f \cdot n_{f,x} \cdot L_f + v_f \cdot n_{f,y} \cdot L_f = \mathbf{u}_f \cdot \mathbf{n}_f \cdot L_f$
  where $\mathbf{u}_f = (u_f, v_f)$ is the velocity at the face, $\mathbf{n}_f = (n_{f,x}, n_{f,y})$ is the outward unit normal, and $L_f$ is the face length.

**Mesh visualization:**

<img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/cfd_mesh_structure.png" style="width:600px !important;" />

*Figure 1: 2D Lid-Driven Cavity Mesh (4×4 cells shown). Red circles (●) mark cell centers where velocity $(u_P, v_P)$ and pressure $p_P$ are stored. The red box highlights one cell and its four faces (east, west, north, south). Boundary conditions are specified on the domain edges: no-slip walls (u=0, v=0) on bottom/left/right, and moving lid (u=1, v=0) on top.*

**Why finite volume?**

Finite-volume CFD stores unknowns as **cell-center values** (or cell averages) and enforces conservation by balancing **fluxes across all faces** of each cell. This approach is naturally conservative: what flows out of one cell flows into a neighboring cell.

A generic transport equation in conservative form:
$$
\nabla\cdot(\mathbf{u}\,q) = \nabla\cdot(\Gamma \nabla q) + S
$$
integrated over a control volume $V_P$ becomes:
$$
\sum_{f\in \partial V_P} (\mathbf{u}q)_f \cdot \mathbf{n}_f A_f
=
\sum_{f\in \partial V_P} \Gamma_f (\nabla q)_f \cdot \mathbf{n}_f A_f
+
S_P V_P
$$

Here $\partial V_P$ denotes the boundary (all faces) of cell $P$. The left-hand side is the sum of **convective fluxes across all faces**; the right-hand side is the sum of **diffusive fluxes** plus **source terms**.

**Discrete conservation in 2D:**

For a specific cell $P$ in our cavity, the discrete $x$-momentum equation is:

$$\rho \left[ (u_f)_E L_E - (u_f)_W L_W + (v_f)_N L_N - (v_f)_S L_S \right]_{u\text{-momentum}} = D_P + G_P$$

where:
- $(u_f)_E, (u_f)_W, (v_f)_N, (v_f)_S$ are face velocities at the four faces
- $L_E, L_W, L_N, L_S$ are the face lengths
- $D_P$ is the net diffusion term
- $G_P = -\left(\frac{\partial p}{\partial x}\right)_P A_P$ is the pressure gradient term

The key insight: the **same face flux** appears in both adjacent cells with **opposite signs**. Momentum leaving cell $P$ equals momentum entering its neighbor—automatic conservation.

**Flux visualization:**

<img src="{{ site.url }}{{ site.baseurl }}/images/developer_guide/cfd_flux_calculation.png" style="width:600px !important;" />

*Figure 2: Flux Exchange Between Adjacent Cells. Cell P (yellow, center) exchanges momentum with four neighbors (E, W, N, S) through shared faces. Arrows show the direction of flux at each face. The conservation principle states that the sum of all fluxes must balance: $\phi_E + \phi_W + \phi_N + \phi_S = 0$ in steady state, ensuring what flows out equals what flows in.*

---

## #3) Turning PDEs into algebra: fluxes, interpolation, and linear systems (2D)

**Face values and interpolation (2D example)**

Since unknowns are **stored only at cell centers**, we must **interpolate** velocity to the cell faces when computing fluxes.

**For the 2D lid-driven cavity:**

Consider a cell $P$ and its east neighbor $E$. The east face lies halfway between them (at the boundary). To compute the flux through the east face:
- We need $u$ and $v$ at the east face
- These are typically approximated as the **average** of cell $P$ and cell $E$:
  $$u_{\text{east face}} = \frac{u_P + u_E}{2}, \quad v_{\text{east face}} = \frac{v_P + v_E}{2}$$

This is a simple **linear interpolation** (second-order accurate on uniform grids).

**For the diffusion terms** (viscous terms like $\mu \frac{\partial^2 u}{\partial x^2}$):
- We compute gradients using **central differences** between neighboring cell centers
- Example: $\frac{\partial u}{\partial x}\big|_{\text{east face}} \approx \frac{u_E - u_P}{\Delta x}$ where $\Delta x$ is the distance between cell centers

**Discrete momentum equations in 2D (cell P)**

After finite-volume discretization, the $x$-momentum equation for cell $P$ becomes an **algebraic equation**:

$$a_P u_P = a_E u_E + a_W u_W + a_N u_N + a_S u_S + b_P - \frac{\partial p}{\partial x}\bigg|_P \cdot A_P$$

Similarly for the $y$-momentum equation:

$$a_P v_P = a_E v_E + a_W v_W + a_N v_N + a_S v_S + b_P - \frac{\partial p}{\partial y}\bigg|_P \cdot A_P$$

where:
- $a_P, a_E, a_W, a_N, a_S$ are **coefficients** arising from discretization of advection and diffusion
- $b_P$ is a known source term
- The pressure gradient terms drive the flow

**Why is this form useful?** It relates the velocity at cell $P$ to its four neighbors (E, W, N, S). This creates a **sparse system of linear equations** that can be solved iteratively.

**The pressure problem: enforcing mass conservation (2D)**

In our 2D cavity, there is **no equation for pressure**. Instead, pressure is determined by requiring that the **continuity equation** is satisfied:

$$\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0$$

In discrete form, for each cell $P$:
$$\frac{u_E - u_W}{2\Delta x} + \frac{v_N - v_S}{2\Delta y} = 0$$

or equivalently, the sum of face fluxes must be zero:
$$\phi_E + \phi_W + \phi_N + \phi_S = 0$$

**This creates a coupling:** velocity and pressure are not independent. We use a **pressure-correction method** (like SIMPLE) to handle this coupling iteratively.

**Correcting velocity with pressure (discrete form):**

The pressure-correction method works by first computing an intermediate velocity $\mathbf{u}^*$ without the pressure gradient, then correcting it using the computed pressure field:

$$u_P := u_P^* - \Delta t \frac{p_E - p_W}{2\Delta x} \cdot \frac{A_P}{\rho}$$

$$v_P := v_P^* - \Delta t \frac{p_N - p_S}{2\Delta y} \cdot \frac{A_P}{\rho}$$

where:
- $u_P^*, v_P^*$ are the intermediate (tentative) velocity components before pressure correction
- $p_E, p_W, p_N, p_S$ are pressures at the four neighboring cell centers
- $\Delta x, \Delta y$ are grid spacings
- $A_P$ is the cell area, $\rho$ is density, $\Delta t$ is a time step parameter

This correction drives the mass imbalance to zero, enforcing continuity in the next iteration.

---

### 4) How we solve it: iterative steady-state algorithm (high level)

A typical steady incompressible workflow (SIMPLE-like) looks like:

1. Start with initial guesses $\mathbf{u}^{(0)}, p^{(0)}$
2. Solve momentum equations using current pressure to get an intermediate velocity $\mathbf{u}^*$
3. Solve a pressure-correction equation so that the corrected velocity satisfies continuity
4. Correct velocity and pressure
5. Repeat until residuals and mass imbalance are below tolerances

In production codes, each “solve” is a sparse linear solve (e.g., CG, BiCGStab, GMRES with preconditioning), and under-relaxation is often used for stability.

## Computational Fluid Dynamics (OpenFOAM Implementations)

### Initializing runTime and mesh

In OpenFOAM, every application starts by initializing two core objects: **runTime** and **mesh**.

**runTime object:**
- Created by calling `#include "Time.H"` in an OpenFOAM solver, `runTime` is a `Time` object
- Manages time-stepping and I/O control
- Handles time-dependent execution (even for steady-state solvers)
- Controls output directories and time folders


**mesh object:**
- Created by calling `#include "fvMesh.H"` in an OpenFOAM solver, `mesh` is a `fvMesh` object
- Represents the computational domain as a structured collection of cells, faces, and vertices
- Stores mesh geometry and connectivity
- Acts as a **container for all field data** (velocity, pressure, etc.)

**Key concept:** The `mesh` object encapsulates the entire finite-volume mesh structure from our general CFD discussion (cells, faces, boundary conditions, etc.). It is the central data structure that OpenFOAM uses to manage all spatial discretization.

### Flow variables: storing data on the mesh

In OpenFOAM, all flow variables (velocity **U**, pressure **p**, etc.) are **field objects** stored directly on the mesh. Each field is tied to the mesh and knows about all cells, internal faces, and boundary faces.

**Creating velocity and pressure fields:**

```cpp
Foam::volVectorField U(
    Foam::IOobject("U", runTime.timeName(), mesh,
                   Foam::IOobject::MUST_READ, Foam::IOobject::AUTO_WRITE),
    mesh
);

Foam::volScalarField p(
    Foam::IOobject("p", runTime.timeName(), mesh,
                   Foam::IOobject::MUST_READ, Foam::IOobject::AUTO_WRITE),
    mesh
);
```

- **`volVectorField`**: A field of vectors (3D) defined at cell centers (volume-averaged)
- **`volScalarField`**: A field of scalars defined at cell centers
- Each field has **two components**: internal field + boundary field

### Understanding field components

#### `U.internalField()` - Internal cell values

Contains the velocity values at **all internal cell centers** (cells not on the boundary).

```cpp
Foam::scalarField& Uint = U.ref().internalFieldRef();  // Access internal field
// Equivalent to: u_P, u_E, u_W, u_N, u_S, ... for all cells in our discretization example
```

**In CFD terms:** This is the storage for all $u_P$ values for every cell $P$ in the domain.

- Size: equal to the number of internal cells (`mesh.nCells()`)
- Ordered sequentially (cell 0, 1, 2, ...)
- These are the **primary unknowns** solved in the momentum equations

#### `U.boundaryField()` - Boundary condition values

Contains velocity values at **all boundary cell centers** and stores the boundary condition type (Dirichlet, Neumann, cyclic, etc.).

```cpp
Foam::fvPatchVectorField& Upatch = U.boundaryFieldRef()[patchID];
// Example: Dirichlet BC on "lid" patch: U = (1, 0, 0)
```

**In CFD terms:** These are the **Dirichlet boundary conditions** (no-slip walls, moving lid) specified on the domain boundaries from our lid-driven cavity example.

**Structure:**
- Multiple patches (e.g., "bottom", "left", "right", "top")
- Each patch stores BC type and values
- Example: moving lid patch has `U = (1, 0, 0)` (moving at velocity 1 in x-direction)

### Mesh geometry data

OpenFOAM provides access to mesh geometric properties through the `fvMesh` object. These directly correspond to our CFD discretization concepts:

#### `mesh.V()` - Cell volumes

Returns a list of volumes for all cells.

```cpp
const Foam::scalarField& V = mesh.V();  // V[cellI] = cell volume
```

**Equivalence:** $A_P$ in our CFD formulation - the area of each cell (in 2D, the "volume" is actually area).

- Size: `mesh.nCells()` (one value per internal cell)
- Used in finite-volume integration: $\int_V dV = A_P$

#### `mesh.Sf()` - Face area vectors

Returns the **area vector** for each face (magnitude = face area, direction = outward normal).

```cpp
const Foam::surfaceVectorField& Sf = mesh.Sf();  // Sf[faceI] = face area vector
```

**Equivalence:** $L_f \cdot \mathbf{n}_f$ in our CFD - the face area multiplied by the outward unit normal.

**Structure:**
- For internal faces: outward normal relative to the owner cell
- For boundary faces: outward normal from the domain
- **Sign matters:** used to compute fluxes across faces

**Example:** In 2D lid-driven cavity:
- East face of cell $P$: `Sf_E = (L_E, 0)` pointing right
- West face of cell $P$: `Sf_W = (-L_W, 0)` pointing left

#### `mesh.C()` - Cell centers

Returns the coordinates of the geometric center of each cell.

```cpp
const Foam::vectorField& C = mesh.C();  // C[cellI] = (x_c, y_c, z_c)
```

**Equivalence:** $(x_c, y_c)$ in our CFD - the position where velocity and pressure are stored.

- Size: `mesh.nCells()`
- Used for interpolation, gradient computation, and flux calculations
- Ordered same as `U.internalField()` (cell 0, 1, 2, ...)

### Connecting mesh data to finite-volume discretization

**How OpenFOAM uses these components:**

When computing the discrete momentum equation for a cell, OpenFOAM internally:

1. **Accesses cell values:** `U.internalField()[cellI]` → $u_P$
2. **Accesses neighbor values:** through face addressing, gets `U.internalField()[neighborCellI]` → $u_E, u_W, ...$
3. **Accesses face fluxes:** Interpolates to faces using `U.internalField()` at both sides
4. **Applies boundary conditions:** Uses `U.boundaryField()[patchI]` for boundary cells
5. **Integrates over volume:** Uses `mesh.V()[cellI]` for cell volume weighting
6. **Computes face contributions:** Uses `mesh.Sf()[faceI]` to get face normal and area

**Complete mapping to CFD discretization:**

| CFD Concept | OpenFOAM Implementation |
|---|---|
| Cell values $u_P, u_E, u_W, u_N, u_S$ | `U.internalField()[cellI]` and neighbors |
| Boundary values $u_{\text{boundary}}$ | `U.boundaryField()[patchI]` |
| Cell volume $A_P$ | `mesh.V()[cellI]` |
| Face area & normal $L_f \mathbf{n}_f$ | `mesh.Sf()[faceI]` |
| Cell center position $(x_c, y_c)$ | `mesh.C()[cellI]` |
| Discrete momentum equation assembly | Handled by `fvMatrix` (Finite-Volume Matrix) |

### Summary: The data flow in OpenFOAM

```
runTime → manages time stepping and I/O
    ↓
mesh → stores all geometry (cells, faces, connectivity)
    ├─ mesh.V()        → cell volumes (A_P)
    ├─ mesh.Sf()       → face area vectors (L_f · n_f)
    └─ mesh.C()        → cell centers (x_c, y_c)
    ↓
U, p → flow fields stored on mesh
    ├─ U.internalField()  → cell-center velocities (u_P, u_E, etc.)
    └─ U.boundaryField()  → boundary conditions
    ↓
fvMatrix assembly → builds discrete equations using mesh data
```

When you write OpenFOAM solvers, you're working directly with these objects to implement the finite-volume discretization and solvers described in the general CFD section.

{% include links.html %}

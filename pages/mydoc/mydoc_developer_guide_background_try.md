---
title: Background
keywords: developer guide
summary:
sidebar: mydoc_sidebar
permalink: developer-guide-background-try.html
folder: mydoc
---

## Computational Fluid Dynamics (General Introduction)

Computational Fluid Dynamics (CFD) is the numerical solution of the Navier--Stokes (NS) equations that describe fluid motion. The Navier--Stokes equations have no analytical solutions, so we need to solve them on a discretized domain (a mesh). The solution process typically starts with converting the continuous NS equations into the discretized form, reformulate the discretized NS equations into matrix-vector product format (Ax=b), and then repeatedly solving large sparse algebraic systems to drive the discretized residuals (R=Ax-b) to zero.

This section shows a simple CFD example by using the finite-volume method to solve **steady-state, incompressible, laminar flow**.

---

## 1) Governing equations: incompressible, laminar Navier–Stokes

For an incompressible Newtonian fluid with constant density $\rho$ and viscosity $\mu$, the steady-state equations are:

**Continuity (mass conservation)**
$$
\nabla \cdot \mathbf{u} = 0
$$

**Momentum (steady)**
$$
\rho (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \mu \nabla^2 \mathbf{u} + \mathbf{f}
$$

where:
- $\mathbf{u}=(u,v,w)$ is velocity,
- $p$ is pressure,
- $\mathbf{f}$ is a body force (often zero in basic examples).

Even in this “simple” setting, the system is nonlinear (because of $(\mathbf{u}\cdot\nabla)\mathbf{u}$) and **coupled** (because pressure enforces $\nabla\cdot\mathbf{u}=0$).

---

## 2) Discretizing the domain: mesh and control volumes

### 2.1 Mesh concepts
A mesh partitions the domain into small cells (control volumes). In 2D these can be triangles/quads; in 3D tetrahedra/hexahedra/polyhedra.

Key geometric objects used by finite-volume methods:
- **Cell volume/area** $V_P$
- **Faces** $f$ of a cell (each face has an area $A_f$ and outward unit normal $\mathbf{n}_f$)
- **Face flux** $\phi_f = (\mathbf{u}_f \cdot \mathbf{n}_f) A_f$

### 2.2 Why finite volume?
Finite-volume CFD stores unknowns as **cell averages** (or cell-center values) and enforces conservation by balancing **fluxes across faces**.

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

This “sum of face fluxes = sources” viewpoint is the core of FVM.

---

## 3) Turning PDEs into algebra: fluxes, interpolation, and linear systems

### 3.1 Face values and schemes
Fluxes require values at faces (e.g., $\mathbf{u}_f$, $q_f$, $(\nabla q)_f$). Since unknowns are stored at cells, we reconstruct face quantities from neighboring cells.

Common choices:
- **Diffusion**: central gradients (second order on smooth meshes).
- **Convection**: upwind/limited schemes (stable for high Reynolds number flow).

### 3.2 Discrete momentum equation (cell $P$)
After discretization, each velocity component equation typically becomes:
$$
a_P u_P = \sum_{N} a_N u_N + b_P - \left(\frac{\partial p}{\partial x}\right)_P V_P
$$
and similarly for $v$ (and $w$ in 3D). The coefficients $a_P, a_N$ come from the discretized advection–diffusion operator.

### 3.3 Pressure–velocity coupling
For incompressible flow, pressure is not given by an equation of state; instead, it acts as a Lagrange multiplier to enforce:
$$
\nabla\cdot \mathbf{u} = 0
$$

Practical solvers therefore use a pressure–velocity coupling algorithm such as:
- **SIMPLE / SIMPLEC / PISO** (common in OpenFOAM)
- **Projection methods** (common in teaching codes)

---

## 4) How we solve it: iterative steady-state algorithm (high level)

A typical steady incompressible workflow (SIMPLE-like) looks like:

1. Start with initial guesses $\mathbf{u}^{(0)}, p^{(0)}$
2. Solve momentum equations using current pressure to get an intermediate velocity $\mathbf{u}^*$
3. Solve a pressure-correction equation so that the corrected velocity satisfies continuity
4. Correct velocity and pressure
5. Repeat until residuals and mass imbalance are below tolerances

In production codes, each “solve” is a sparse linear solve (e.g., CG, BiCGStab, GMRES with preconditioning), and under-relaxation is often used for stability.

---

## 5) Worked example: steady 2D lid-driven cavity (incompressible laminar)

To make the ideas concrete, we use the classic **lid-driven cavity**:
- Square domain $[0,1]\times[0,1]$
- No-slip walls on all boundaries
- Top wall (lid) moves with $u=1, v=0$
- Steady laminar recirculation forms inside

Below is a compact **finite-volume-style** Python example using a **projection method** on a uniform Cartesian mesh with a **staggered arrangement** (velocities on faces, pressure in cell centers). While simplified, it demonstrates the essential CFD loop:

- build face fluxes and diffusion terms
- compute a tentative velocity $\mathbf{u}^*$
- solve a Poisson equation for pressure
- correct $\mathbf{u}$ to satisfy $\nabla\cdot\mathbf{u}=0$
- pseudo-time march until steady state

> Notes:
> - This code is intentionally minimal for teaching/documentation.
> - It uses pseudo-time stepping to converge to a steady solution.
> - It uses simple iterative solvers (Jacobi/Gauss–Seidel-like updates) to keep dependencies low.


{% include links.html %}

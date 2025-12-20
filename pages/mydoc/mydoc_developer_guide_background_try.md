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

For an incompressible Newtonian fluid with constant density \(\rho\) and viscosity \(\mu\), the steady-state equations are:

**Continuity (mass conservation)**
$$
\nabla \cdot \mathbf{u} = 0
$$

**Momentum (steady)**
\[
\rho (\mathbf{u}\cdot\nabla)\mathbf{u} = -\nabla p + \mu \nabla^2 \mathbf{u} + \mathbf{f}
\]

where:
- \(\mathbf{u}=(u,v,w)\) is velocity,
- \(p\) is pressure,
- \(\mathbf{f}\) is a body force (often zero in basic examples).

Even in this “simple” setting, the system is nonlinear (because of \((\mathbf{u}\cdot\nabla)\mathbf{u}\)) and **coupled** (because pressure enforces \(\nabla\cdot\mathbf{u}=0\)).

---

## 2) Discretizing the domain: mesh and control volumes

### 2.1 Mesh concepts
A mesh partitions the domain into small cells (control volumes). In 2D these can be triangles/quads; in 3D tetrahedra/hexahedra/polyhedra.

Key geometric objects used by finite-volume methods:
- **Cell volume/area** \(V_P\)
- **Faces** \(f\) of a cell (each face has an area \(A_f\) and outward unit normal \(\mathbf{n}_f\))
- **Face flux** \(\phi_f = (\mathbf{u}_f \cdot \mathbf{n}_f) A_f\)

### 2.2 Why finite volume?
Finite-volume CFD stores unknowns as **cell averages** (or cell-center values) and enforces conservation by balancing **fluxes across faces**.

A generic transport equation in conservative form:
\[
\nabla\cdot(\mathbf{u}\,q) = \nabla\cdot(\Gamma \nabla q) + S
\]
integrated over a control volume \(V_P\) becomes:
\[
\sum_{f\in \partial V_P} (\mathbf{u}q)_f \cdot \mathbf{n}_f A_f
=
\sum_{f\in \partial V_P} \Gamma_f (\nabla q)_f \cdot \mathbf{n}_f A_f
+
S_P V_P
\]

This “sum of face fluxes = sources” viewpoint is the core of FVM.

---

## 3) Turning PDEs into algebra: fluxes, interpolation, and linear systems

### 3.1 Face values and schemes
Fluxes require values at faces (e.g., \(\mathbf{u}_f\), \(q_f\), \((\nabla q)_f\)). Since unknowns are stored at cells, we reconstruct face quantities from neighboring cells.

Common choices:
- **Diffusion**: central gradients (second order on smooth meshes).
- **Convection**: upwind/limited schemes (stable for high Reynolds number flow).

### 3.2 Discrete momentum equation (cell \(P\))
After discretization, each velocity component equation typically becomes:
\[
a_P u_P = \sum_{N} a_N u_N + b_P - \left(\frac{\partial p}{\partial x}\right)_P V_P
\]
and similarly for \(v\) (and \(w\) in 3D). The coefficients \(a_P, a_N\) come from the discretized advection–diffusion operator.

### 3.3 Pressure–velocity coupling
For incompressible flow, pressure is not given by an equation of state; instead, it acts as a Lagrange multiplier to enforce:
\[
\nabla\cdot \mathbf{u} = 0
\]

Practical solvers therefore use a pressure–velocity coupling algorithm such as:
- **SIMPLE / SIMPLEC / PISO** (common in OpenFOAM)
- **Projection methods** (common in teaching codes)

---

## 4) How we solve it: iterative steady-state algorithm (high level)

A typical steady incompressible workflow (SIMPLE-like) looks like:

1. Start with initial guesses \(\mathbf{u}^{(0)}, p^{(0)}\)
2. Solve momentum equations using current pressure to get an intermediate velocity \(\mathbf{u}^*\)
3. Solve a pressure-correction equation so that the corrected velocity satisfies continuity
4. Correct velocity and pressure
5. Repeat until residuals and mass imbalance are below tolerances

In production codes, each “solve” is a sparse linear solve (e.g., CG, BiCGStab, GMRES with preconditioning), and under-relaxation is often used for stability.

---

## 5) Worked example: steady 2D lid-driven cavity (incompressible laminar)

To make the ideas concrete, we use the classic **lid-driven cavity**:
- Square domain \([0,1]\times[0,1]\)
- No-slip walls on all boundaries
- Top wall (lid) moves with \(u=1, v=0\)
- Steady laminar recirculation forms inside

Below is a compact **finite-volume-style** Python example using a **projection method** on a uniform Cartesian mesh with a **staggered arrangement** (velocities on faces, pressure in cell centers). While simplified, it demonstrates the essential CFD loop:

- build face fluxes and diffusion terms
- compute a tentative velocity \(\mathbf{u}^*\)
- solve a Poisson equation for pressure
- correct \(\mathbf{u}\) to satisfy \(\nabla\cdot\mathbf{u}=0\)
- pseudo-time march until steady state

> Notes:
> - This code is intentionally minimal for teaching/documentation.
> - It uses pseudo-time stepping to converge to a steady solution.
> - It uses simple iterative solvers (Jacobi/Gauss–Seidel-like updates) to keep dependencies low.

```python
import numpy as np

def lid_driven_cavity_fv_projection(
    nx=64, ny=64,
    Re=200.0,
    max_iter=5000,
    dt=0.002,
    poisson_iter=80,
    tol_div=1e-6,
    report_every=200
):
    """
    2D incompressible laminar lid-driven cavity (steady solution via pseudo-time stepping).
    Finite-volume-style projection method on a staggered grid:
      - p at cell centers: (nx, ny)
      - u at vertical faces: (nx+1, ny)  (x-velocity)
      - v at horizontal faces: (nx, ny+1) (y-velocity)

    Domain: [0,1]x[0,1], lid velocity u=1 at top boundary, no-slip elsewhere.
    """

    Lx, Ly = 1.0, 1.0
    dx, dy = Lx/nx, Ly/ny

    rho = 1.0
    nu  = 1.0 / Re  # kinematic viscosity

    # Staggered storage
    p = np.zeros((nx, ny), dtype=float)
    u = np.zeros((nx+1, ny), dtype=float)
    v = np.zeros((nx, ny+1), dtype=float)

    # Helper: enforce velocity boundary conditions (no-slip + moving lid)
    def apply_bc(u, v):
        # u at vertical faces: i=0 and i=nx are left/right walls => u=0
        u[0, :]  = 0.0
        u[-1, :] = 0.0
        # bottom wall (y=0): u=0 at faces adjacent to bottom
        u[:, 0]  = 0.0
        # top lid (y=1): u=1 at faces adjacent to top
        u[:, -1] = 1.0

        # v at horizontal faces: j=0 and j=ny are bottom/top walls => v=0
        v[:, 0]  = 0.0
        v[:, -1] = 0.0
        # left/right walls: v=0 at faces adjacent to left/right
        v[0, :]  = 0.0
        v[-1, :] = 0.0

    apply_bc(u, v)

    # Discrete divergence at cell centers from staggered u,v
    def divergence(u, v):
        # div at p-cells (i=0..nx-1, j=0..ny-1)
        du = (u[1:, :] - u[:-1, :]) / dx
        dv = (v[:, 1:] - v[:, :-1]) / dy
        return du + dv

    # Laplacians for u and v (simple 5-point on their respective grids)
    def lap_u(u):
        Lu = np.zeros_like(u)
        # interior faces for u: i=1..nx-1, j=1..ny-2 (avoid boundaries)
        Lu[1:-1, 1:-1] = (
            (u[2:, 1:-1] - 2*u[1:-1, 1:-1] + u[:-2, 1:-1]) / dx**2 +
            (u[1:-1, 2:]   - 2*u[1:-1, 1:-1] + u[1:-1, :-2]) / dy**2
        )
        return Lu

    def lap_v(v):
        Lv = np.zeros_like(v)
        # interior faces for v: i=1..nx-2, j=1..ny-1
        Lv[1:-1, 1:-1] = (
            (v[2:, 1:-1] - 2*v[1:-1, 1:-1] + v[:-2, 1:-1]) / dx**2 +
            (v[1:-1, 2:] - 2*v[1:-1, 1:-1] + v[1:-1, :-2]) / dy**2
        )
        return Lv

    # Pressure gradients interpolated to u- and v-locations
    def gradp_to_u(p):
        # dp/dx at u-faces (nx+1, ny); interior faces i=1..nx-1
        g = np.zeros((nx+1, ny))
        g[1:-1, :] = (p[1:, :] - p[:-1, :]) / dx
        return g

    def gradp_to_v(p):
        # dp/dy at v-faces (nx, ny+1); interior faces j=1..ny-1
        g = np.zeros((nx, ny+1))
        g[:, 1:-1] = (p[:, 1:] - p[:, :-1]) / dy
        return g

    # Build RHS for pressure Poisson: ∇²p = (rho/dt) * div(u*)
    # Use simple Jacobi iterations for Poisson with Neumann-like behavior at boundaries (dp/dn=0)
    def poisson_pressure(p, rhs):
        pn = p.copy()
        for _ in range(poisson_iter):
            p_old = pn.copy()
            pn[1:-1, 1:-1] = (
                (p_old[2:, 1:-1] + p_old[:-2, 1:-1]) * dy**2 +
                (p_old[1:-1, 2:] + p_old[1:-1, :-2]) * dx**2 -
                rhs[1:-1, 1:-1] * dx**2 * dy**2
            ) / (2*(dx**2 + dy**2))

            # "Neumann" boundaries (zero normal gradient) via copying adjacent interior
            pn[0, :]   = pn[1, :]
            pn[-1, :]  = pn[-2, :]
            pn[:, 0]   = pn[:, 1]
            pn[:, -1]  = pn[:, -2]

            # Fix gauge (pressure defined up to a constant)
            pn[0, 0] = 0.0
        return pn

    for it in range(1, max_iter+1):
        # --- Step 1: tentative velocity u*, v* (explicit convection omitted for simplicity) ---
        # For CFD 101, we keep the core idea: diffusion + pressure projection.
        # Adding convection is straightforward but lengthens the code.
        u_star = u + dt * (nu * lap_u(u) - (1.0/rho) * gradp_to_u(p))
        v_star = v + dt * (nu * lap_v(v) - (1.0/rho) * gradp_to_v(p))

        apply_bc(u_star, v_star)

        # --- Step 2: pressure Poisson from divergence of u* ---
        div_star = divergence(u_star, v_star)
        rhs = (rho/dt) * div_star
        p_new = poisson_pressure(p, rhs)

        # --- Step 3: correct velocities to be divergence-free ---
        u_new = u_star - (dt/rho) * gradp_to_u(p_new)
        v_new = v_star - (dt/rho) * gradp_to_v(p_new)
        apply_bc(u_new, v_new)

        # --- Convergence monitoring: max divergence ---
        div_new = divergence(u_new, v_new)
        max_div = np.max(np.abs(div_new))

        u, v, p = u_new, v_new, p_new

        if (it % report_every) == 0 or it == 1:
            umax = np.max(u); vmax = np.max(v)
            print(f"iter={it:5d}  max|div|={max_div:.3e}  umax={umax:.3f}  vmax={vmax:.3f}")

        if max_div < tol_div:
            print(f"Converged: iter={it}, max|div|={max_div:.3e}")
            break

    # Return fields (staggered) and a cell-centered velocity for convenience
    uc = 0.5 * (u[1:, :] + u[:-1, :])
    vc = 0.5 * (v[:, 1:] + v[:, :-1])
    return uc, vc, p


if __name__ == "__main__":
    uc, vc, p = lid_driven_cavity_fv_projection(nx=64, ny=64, Re=200, max_iter=6000)

    # Optional visualization
    try:
        import matplotlib.pyplot as plt
        nx, ny = p.shape
        x = (np.arange(nx) + 0.5) / nx
        y = (np.arange(ny) + 0.5) / ny
        X, Y = np.meshgrid(x, y, indexing="ij")

        plt.figure()
        plt.contourf(X, Y, p, levels=40)
        plt.colorbar()
        plt.title("Pressure (cell-centered)")

        plt.figure()
        skip = 3
        plt.quiver(X[::skip, ::skip], Y[::skip, ::skip],
                   uc[::skip, ::skip], vc[::skip, ::skip])
        plt.title("Velocity vectors (cell-centered)")
        plt.xlabel("x"); plt.ylabel("y")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Plot skipped:", e)




{% include links.html %}

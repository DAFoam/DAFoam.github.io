---
title: "Tutorial: Airfoil agent"
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-airfoil.html
folder: mydoc
---

{% include note.html content="Please follow the instructions from the Overview page to install MDO Agent Deck before using the airfoil agent." %}

---
title: Tutorial: Airfoil agent
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-airfoil.html
folder: mydoc
---

{% include note.html content="Please follow the instructions from the Overview page to install MDO Agent Deck before using the airfoil agent." %}

## What the Airfoil Agent Does

The airfoil agent supports these skills:

- `generate-cfd-mesh`: build CFD mesh and mesh-quality outputs.
- `run-cfd-simulation`: run steady CFD from an existing mesh.
- `run-aero-optimization`: run single-point aerodynamic optimization.

## Detailed Inputs (Click to Expand)

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">
<a data-toggle="collapse" href="#airfoilMeshInputs">`generate-cfd-mesh` inputs (click to expand)</a>
</h4>
</div>
<div id="airfoilMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profile` (`str`, default: `naca0012`): airfoil name (for example `naca0012`, `rae2822`).
- `mesh_cells` (`int`, default: `6000`): target total mesh cell count.
- `blunt_te` (`float`, default: `0.01`): trailing-edge bluntness trim location as x/chord.
- `y_plus` (`float`, default: `50.0`): near-wall mesh target in wall units.
- `mach_number` (`float`, default: `0.3`): freestream Mach number used for mesh sizing.
- `d0` (`float`, default: `-1.0`): first-layer height in meters; negative means auto-estimate from `y_plus` and `mach_number`.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">
<a data-toggle="collapse" href="#airfoilSteadyCfdInputs">`run-cfd-simulation` inputs (click to expand)</a>
</h4>
</div>
<div id="airfoilSteadyCfdInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (`float`, default: `2.0`): angle of attack in degrees.
- `airfoil_profile` (`str`, default: inherited from mesh step): profile name used for CST fitting when needed.
- `mach_number` (`float`, default: inherited from mesh step): freestream Mach number.
- `solver_name` (`str`, default: `None`): optional explicit solver override.
- `max_flow_iters` (`int`, default: `3000`): maximum solver iterations.
- `n_cst_coeffs` (`int`, default: `6`): number of CST coefficients per surface.
- `reynolds_number` (`float`, default: `1000000.0`): Reynolds number.
- `cst_coeffs` (`list[float]`, default: `None`): optional CST vector `[upper..., lower...]`; if omitted, it is fitted automatically.
- `n_cpu_cores` (`int`, default: `1`): MPI ranks/CPU cores.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<h4 class="panel-title">
<a data-toggle="collapse" href="#airfoilAeroOptInputs">`run-aero-optimization` inputs (click to expand)</a>
</h4>
</div>
<div id="airfoilAeroOptInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (`float`, default: `2.0`): initial angle of attack in degrees.
- `airfoil_profile` (`str`, default: inherited from mesh step): airfoil profile.
- `mach_number` (`float`, default: inherited from mesh step): freestream Mach number.
- `solver_name` (`str`, default: `None`): optional solver override.
- `n_cst_coeffs` (`int`, default: `6`): CST coefficients per surface.
- `reynolds_number` (`float`, default: `1000000.0`): Reynolds number.
- `optimizer` (`str`, default: `IPOPT`): optimizer (`IPOPT`, `SNOPT`, `SLSQP`).
- `lift_constraint` (`float`, default: `0.5`): minimum lift coefficient target.
- `max_opt_iters` (`int`, default: `20`): max optimization iterations.
- `thickness_constraint` (`float`, default: `0.5`): minimum normalized thickness (negative disables).
- `le_radius_constraint` (`float`, default: `-1.0`): minimum normalized leading-edge radius (negative disables).
- `cst_coeffs` (`list[float]`, default: `None`): optional initial CST vector.
- `n_cpu_cores` (`int`, default: `1`): MPI ranks/CPU cores.

</div>
</div>
</div>

## Example Prompt

```text
Use the airfoil agent to generate a CFD mesh for NACA0012 at Mach 0.05, with 6000 cells and y+ target of 50.
```

{% include links.html %}


{% include links.html %}

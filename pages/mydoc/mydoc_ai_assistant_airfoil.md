---
title: "Tutorial: Airfoil agent"
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

## Standard Inputs

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilMeshStandardInputs">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="airfoilMeshStandardInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profile` (`str`, default: `naca0012`): airfoil name (for example `naca0012`, `rae2822`).
- `mesh_cells` (`int`, default: `6000`): target total mesh cell count.
- `y_plus` (`float`, default: `50.0`): near-wall mesh target in wall units.
- `mach_number` (`float`, default: `0.3`): freestream Mach number used for mesh sizing.
- `local_refine_box` (`list[list[float]]`, default: `[[1.0, -0.2, -0.1], [2.0, 0.2, 0.1]]`): two box-corner vectors `[[x0, y0, z0], [x1, y1, z1]]` used for the always-on single-level local refinement.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilSteadyCfdStandardInputs">`run-cfd-simulation`  (click to expand)</a>
</div>
</div>
<div id="airfoilSteadyCfdStandardInputs" class="panel-collapse collapse">
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
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilAeroOptStandardInputs">`run-aero-optimization`  (click to expand)</a>
</div>
</div>
<div id="airfoilAeroOptStandardInputs" class="panel-collapse collapse">
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

## Advanced Parameters

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilMeshAdvancedParams">`generate-cfd-mesh`  (click to expand)</a>
</div>
</div>
<div id="airfoilMeshAdvancedParams" class="panel-collapse collapse">
<div class="panel-body">

- `blunt_te` (`float`, default: `0.01`): trailing-edge round percentage expressed as an x/chord trim location; `0.01` means the trim starts at `x = 0.01` from the trailing edge.
- `d0` (`float`, default: `-1.0`): first-layer height in meters; use a negative value to estimate it from `y_plus` and `mach_number`.
- `hyperbolic_sweeps` (`int`, default: `20`): number of smoothing sweeps per layer for hyperbolic extrusion.
- `neighbor_rings` (`int`, default: `5`): neighbor-ring depth used by the hyperbolic extrusion smoother.
- `diffuse_start` (`float`, default: `0.002`): smoothing onset distance in meters for hyperbolic diffusion.
- `max_nonorthogonality_pass` (`float`, default: `70.0`): pass threshold for maximum non-orthogonality.
- `max_nonorthogonality_warning` (`float`, default: `80.0`): warning threshold for maximum non-orthogonality.
- `max_aspect_ratio_pass` (`float`, default: `1000.0`): pass threshold for maximum aspect ratio.
- `max_aspect_ratio_warning` (`float`, default: `5000.0`): warning threshold for maximum aspect ratio.
- `max_skewness_pass` (`float`, default: `4.0`): pass threshold for maximum skewness.
- `max_skewness_warning` (`float`, default: `6.0`): warning threshold for maximum skewness.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilSteadyCfdAdvancedParams">`run-cfd-simulation`   (click to expand)</a>
</div>
</div>
<div id="airfoilSteadyCfdAdvancedParams" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (`float`, default: `0.4`): Mach-number boundary used by the default Mach-based solver selection when `solver_name` is not provided.
- `coef_stddev_pct_pass` (`float`, default: `0.001`): pass threshold for force-coefficient standard deviation in percent.
- `coef_stddev_pct_warning` (`float`, default: `1.0`): warning threshold for force-coefficient standard deviation in percent.
- `residual_drop_orders_pass` (`float`, default: `6.0`): pass threshold for minimum residual drop in log10 orders.
- `residual_drop_orders_warning` (`float`, default: `4.0`): warning threshold for minimum residual drop in log10 orders.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilAeroOptAdvancedParams">`run-aero-optimization`   (click to expand)</a>
</div>
</div>
<div id="airfoilAeroOptAdvancedParams" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (`float`, default: `0.4`): Mach-number boundary used by the default Mach-based solver selection when `solver_name` is not provided.
- `objective_reduction_pct_pass` (`float`, default: `5.0`): pass threshold for objective reduction in percent.
- `objective_reduction_pct_warning` (`float`, default: `1.0`): warning threshold for objective reduction in percent.
- `final_feasibility_pass` (`float`, default: `0.0001`): pass threshold for final feasibility.
- `final_feasibility_warning` (`float`, default: `0.01`): warning threshold for final feasibility.
- `flow_residual_drop_orders_pass` (`float`, default: `7.0`): pass threshold for minimum flow residual drop in log10 orders.
- `flow_residual_drop_orders_warning` (`float`, default: `5.0`): warning threshold for minimum flow residual drop in log10 orders.
- `adjoint_residual_drop_orders_pass` (`float`, default: `5.0`): pass threshold for minimum adjoint residual drop in log10 orders.
- `adjoint_residual_drop_orders_warning` (`float`, default: `3.0`): warning threshold for minimum adjoint residual drop in log10 orders.

</div>
</div>
</div>

## Agent Capability demos

1. **Mesh Generation.** Users can prompt to generate airfoil mesh with desired airfoil profiles, mesh densities, yPlus, and local refinement.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-coarse.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-trame.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-fine.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-local-refine.png" style="width:400px !important;" />

Fig. 1. Top left: Overview of a coarse mesh. Prompt: Generate a cfd mesh for the naca0012 airfoil. Top right: Trame interactive view of the TE mesh. Bottom left: Overview of a fine mesh with a different airfoil. Prompt: Generate a cfd mesh for the rae2822 airfoil with 50K cells, yPlus 3, and ref Mach=0.7. Bottom right: Locally refined mesh. Prompt: Locally refine the above mesh between -0.1 to 1.1 chords from LE, z length of the refinment is 0.5 chords.

2. **CFD Simulation.** Users can prompt to run airfoil CFD simulations with desired airfoil profiles (prescribed in the mesh generation skill), angles of attack, Mach numbers, and Reynolds numbers. 

2. **CFD Mesh Convergence Study.** Users can prompt to conduct a mesh convergence study for an airfoil.

{% include links.html %}

---
title: "Tutorial: Aircraft agent"
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-aircraft.html
folder: mydoc
---

{% include note.html content="Please follow the instructions from the Overview page to install MDO Agent Deck before using the aircraft agent." %}

## What the Aircraft Agent Does

The aircraft agent supports these skills:

- `generate-cfd-mesh`: build the aircraft CFD mesh and mesh-quality outputs.
- `run-cfd-simulation`: run steady aircraft CFD from an existing mesh.
- `run-aero-optimization`: run aerodynamic shape optimization for the aircraft.

## Standard Inputs

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftGenerateCfdMeshInputs">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="aircraftGenerateCfdMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profiles` (`list[str]`, default: `["rae2822", "rae2822", "rae2822"]`): wing airfoil profile names ordered section 0 to section 2.
- `sweeps` (`list[float]`, default: `[35.0, 30.0]`): wing sweep angles in degrees formatted as `[break_sweep_deg, tip_sweep_deg]`.
- `twists` (`list[float]`, default: `[0.0, 0.0]`): wing twist angles in degrees formatted as `[section1_twist_deg, section2_twist_deg]`.
- `chords` (`list[float]`, default: `[8.0, 4.5, 1.7]`): wing chord lengths for the packaged geometry.
- `spans` (`list[float]`, default: `[5.0, 14.0]`): wing panel semi-span values.
- `dihedrals` (`list[float]`, default: `[6.0, 6.0]`): wing dihedral angles in degrees.
- `tail_twist` (`float`, default: `0.0`): tail twist angle in degrees.
- `n_cpus` (`int`, default: `2`): MPI ranks used for the parallel snappyHexMesh passes.
- `max_cell_size` (`float`, default: `None`): target farfield blockMesh cell size.
- `surface_level` (`int`, default: `7`): snappyHexMesh surface refinement level.
- `line_level` (`int`, default: `None`): snappyHexMesh feature-edge refinement level.
- `curvature_level` (`int`, default: `None`): snappyHexMesh curvature refinement level; `-1` disables it.
- `n_boundary_layers` (`int`, default: `8`): number of prism layers.
- `n_layer_outer_iter` (`int`, default: `3`): number of outer iterations in `addLayersControls`.
- `local_refine_box` (`list[list[float]]`, default: `[[1.0, -0.2, -0.1], [2.0, 0.2, 0.1]]`): box corners for the fixed single-level local refinement.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftRunCfdSimulationInputs">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="aircraftRunCfdSimulationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (`float`, default: `2.0`): freestream angle of attack in degrees.
- `mach_number` (`float`, default: `0.3`): freestream Mach number.
- `solver_name` (`str`, default: `None`): optional explicit solver override.
- `max_flow_iters` (`int`, default: `3000`): maximum flow iterations.
- `reynolds_number` (`float`, default: `1000000.0`): freestream Reynolds number.
- `primal_func_std_tol` (`float`, default: `1e-6`): primal function standard deviation tolerance.
- `airfoil_profiles` (`list[str]`, default: inherited from `generate-cfd-mesh`): wing airfoil profiles used for CST fitting when needed.
- `n_cst_coeffs` (`int`, default: `6`): number of CST coefficients per surface.
- `cst_coeffs` (`list[float]`, default: `None`): optional flattened aircraft wing CST coefficient vector.
- `reference_area` (`float`, default: `None`): optional aerodynamic reference area.
- `reference_length` (`float`, default: `None`): optional aerodynamic reference length.
- `chords` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing chord values.
- `spans` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing semi-span values.
- `sweeps` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing sweep values.
- `twists` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing twist values.
- `dihedrals` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing dihedral values.
- `tail_twist` (`float`, default: inherited from `generate-cfd-mesh`): tail twist angle.
- `pressure_profile_fractions` (`list[float]`, default: `[0.2, 0.5, 0.9]`): spanwise fractions used for pressure-profile plots.
- `n_cpu_cores` (`int`, default: `1`): MPI ranks/CPU cores.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftRunAeroOptimizationInputs">`run-aero-optimization` (click to expand)</a>
</div>
</div>
<div id="aircraftRunAeroOptimizationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (`float`, default: `2.0`): initial freestream angle of attack in degrees.
- `airfoil_profiles` (`list[str]`, default: inherited from `generate-cfd-mesh`): wing airfoil profiles used for CST fitting when needed.
- `mach_number` (`float`, default: inherited from `generate-cfd-mesh`): freestream Mach number.
- `solver_name` (`str`, default: `None`): optional explicit solver override.
- `reynolds_number` (`float`, default: `1000000.0`): freestream Reynolds number.
- `optimizer` (`str`, default: `IPOPT`): optimization algorithm.
- `lift_constraint` (`float`, default: `0.5`): target lift coefficient equality constraint.
- `le_radius_constraint` (`float`, default: `-1.0`): lower bound on normalized leading-edge radius.
- `thickness_constraint` (`float`, default: `0.5`): lower bound on normalized aircraft wing thickness.
- `volume_constraint` (`float`, default: `1.0`): lower bound on normalized aircraft wing volume.
- `max_opt_iters` (`int`, default: `50`): maximum optimization iterations.
- `primal_func_std_tol` (`float`, default: `1e-6`): primal function standard deviation tolerance.
- `n_cst_coeffs` (`int`, default: `6`): number of CST coefficients per surface.
- `cst_coeffs` (`list[float]`, default: `None`): optional flattened aircraft wing CST coefficient vector.
- `reference_area` (`float`, default: `None`): optional aerodynamic reference area.
- `reference_length` (`float`, default: `None`): optional aerodynamic reference length.
- `chords` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing chord values.
- `sweeps` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing sweep values.
- `dihedrals` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing dihedral values.
- `spans` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing semi-span values.
- `twists` (`list[float]`, default: inherited from `generate-cfd-mesh`): wing twist values.
- `tail_twist` (`float`, default: inherited from `generate-cfd-mesh`): tail twist angle.
- `pressure_profile_fractions` (`list[float]`, default: `[0.2, 0.5, 0.9]`): spanwise fractions used for pressure-profile plots.
- `n_cpu_cores` (`int`, default: `1`): MPI ranks/CPU cores.

</div>
</div>
</div>

## Advanced Parameters

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftGenerateCfdMeshAdvanced">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="aircraftGenerateCfdMeshAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `max_nonorthogonality_pass` (`float`, default: `70.0`): pass threshold for maximum non-orthogonality.
- `max_nonorthogonality_warning` (`float`, default: `80.0`): warning threshold for maximum non-orthogonality.
- `max_aspect_ratio_pass` (`float`, default: `1000.0`): pass threshold for maximum aspect ratio.
- `max_aspect_ratio_warning` (`float`, default: `10000.0`): warning threshold for maximum aspect ratio.
- `max_skewness_pass` (`float`, default: `4.0`): pass threshold for maximum skewness.
- `max_skewness_warning` (`float`, default: `6.0`): warning threshold for maximum skewness.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftRunCfdSimulationAdvanced">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="aircraftRunCfdSimulationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (`float`, default: `0.4`): Mach boundary used by default solver selection.
- `coef_stddev_pct_pass` (`float`, default: `0.01`): pass threshold for force-coefficient standard deviation in percent.
- `coef_stddev_pct_warning` (`float`, default: `10.0`): warning threshold for force-coefficient standard deviation in percent.
- `residual_drop_orders_pass` (`float`, default: `7.0`): pass threshold for minimum residual drop in log10 orders.
- `residual_drop_orders_warning` (`float`, default: `5.0`): warning threshold for minimum residual drop in log10 orders.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftRunAeroOptimizationAdvanced">`run-aero-optimization` (click to expand)</a>
</div>
</div>
<div id="aircraftRunAeroOptimizationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (`float`, default: `0.4`): Mach boundary used by default solver selection.
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

{% include links.html %}

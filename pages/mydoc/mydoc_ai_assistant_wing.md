---
title: "Tutorial: Wing agent"
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-wing.html
folder: mydoc
---

{% include note.html content="Please follow the instructions from the Overview page to install MDO Agent Deck before using the wing agent." %}

## What the Wing Agent Does

The wing agent supports these skills:

- `generate-cfd-mesh`: build the wing CFD mesh and mesh-quality outputs.
- `generate-fea-mesh`: build the wingbox FEA mesh for structural workflows.
- `run-aero-simulation`: run steady aerodynamic CFD from an existing wing mesh.
- `run-aero-optimization`: run aerodynamic shape optimization for the wing.
- `run-aero-struct-simulation`: run coupled aero-structural analysis.
- `run-aero-struct-optimization`: run coupled aero-structural optimization.

## Standard Inputs

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateCfdMeshInputs">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateCfdMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profiles` (list[str], default: ["naca0012", "naca0012"]): section airfoil profile names ordered root to tip.
- `chords` (list[float], default: [1.0, 1.0]): section chord lengths in meters ordered root to tip.
- `spans` (list[float], default: [3.0]): span-segment lengths in meters ordered root to tip.
- `sweeps` (list[float], default: [0.0]): leading-edge sweep angles in degrees ordered root to tip.
- `dihedrals` (list[float], default: [0.0]): dihedral angles in degrees ordered root to tip.
- `twists` (list[float], default: [0.0]): twist angles in degrees ordered from the first non-root section to the tip.
- `mesh_cells` (int, default: 200000): target total volume mesh cell count.
- `y_plus` (float, default: 50.0): target near-wall spacing in wall units (y+) used to estimate the first-layer cell size d0 when it is not provided.
- `mach_number` (float, default: 0.2): freestream Mach number used together with y_plus, reynolds_number, and ref_chord to estimate the near-wall first-layer cell size d0 when it is not provided.
- `reynolds_number` (float, default: 5e6): freestream Reynolds number used together with y_plus, mach_number, and ref_chord to estimate the near-wall first-layer cell size d0 when it is not provided.
- `local_refine_box` (list[list[float]], default: None): optional two-corner local refinement box `[[x0, y0, z0], [x1, y1, z1]]`; leave unset for no local refinement.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateFeaMeshInputs">`generate-fea-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateFeaMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `n_ribs` (int, default: 10): number of ribs in the spanwise direction.
- `n_spars` (int, default: 2): number of spars in the chordwise direction.
- `total_elements_target` (int, default: 3000): requested total number of shell elements.
- `wingbox_span` (float, default: 0.95): fraction of full wing span covered by the wingbox.
- `wingbox_chord_start` (float, default: 0.20): front spar position as a fraction of local chord.
- `wingbox_chord_end` (float, default: 0.80): rear spar position as a fraction of local chord.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number passed through for downstream coupled skills.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): freestream Reynolds number passed through for downstream coupled skills.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): section airfoil profiles passed through for downstream coupled skills.
- `chords` (list[float], default: inherited from generate-cfd-mesh): section chord lengths passed through for downstream coupled skills.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): section sweep angles passed through for downstream coupled skills.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): section dihedral angles passed through for downstream coupled skills.
- `spans` (list[float], default: inherited from generate-cfd-mesh): section spans passed through for downstream coupled skills.
- `twists` (list[float], default: inherited from generate-cfd-mesh): section twists passed through for downstream coupled skills.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroSimulationInputs">`run-aero-simulation` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroSimulationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 2.0): freestream angle of attack in degrees.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): section airfoil profiles used for CST fitting when needed.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): freestream Reynolds number.
- `cst_coeffs` (list[float], default: None): optional flattened wing CST coefficient vector.
- `chords` (list[float], default: inherited from generate-cfd-mesh): section chord lengths.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): section sweep angles.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): section dihedral angles.
- `spans` (list[float], default: inherited from generate-cfd-mesh): section spans.
- `twists` (list[float], default: inherited from generate-cfd-mesh): section twists.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for pressure-profile plots.
- `n_cpu_cores` (int, default: 1): MPI ranks/CPU cores.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroOptimizationInputs">`run-aero-optimization` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroOptimizationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 2.0): initial freestream angle of attack in degrees.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): section airfoil profiles used for CST fitting when needed.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): freestream Reynolds number.
- `optimizer` (str, default: "IPOPT"): optimization algorithm.
- `lift_constraint` (float, default: 0.5): target lift coefficient constraint.
- `le_radius_constraint` (float, default: 0.7): lower bound on normalized leading-edge radius.
- `thickness_constraint` (float, default: 0.5): lower bound on normalized section thickness.
- `volume_constraint` (float, default: 1.0): lower bound on normalized wing volume.
- `max_opt_iters` (int, default: 100): maximum optimization iterations.
- `cst_coeffs` (list[float], default: None): optional flattened wing CST coefficient vector.
- `chords` (list[float], default: inherited from generate-cfd-mesh): section chord lengths.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): section sweep angles.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): section dihedral angles.
- `spans` (list[float], default: inherited from generate-cfd-mesh): section spans.
- `twists` (list[float], default: inherited from generate-cfd-mesh): section twists.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for pressure-profile plots.
- `n_cpu_cores` (int, default: 1): MPI ranks/CPU cores.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroStructSimulationInputs">`run-aero-struct-simulation` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroStructSimulationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 3.0): freestream angle of attack in degrees.
- `airfoil_profiles` (list[str], default: inherited from generate-fea-mesh): section airfoil profiles used for CST fitting when needed.
- `mach_number` (float, default: inherited from generate-fea-mesh): freestream Mach number.
- `reynolds_number` (float, default: inherited from generate-fea-mesh): freestream Reynolds number.
- `cst_coeffs` (list[float], default: None): optional flattened wing CST coefficient vector.
- `struct_material` (str, default: "aluminum"): structural material.
- `struct_panel_thickness` (float, default: 0.01): initial structural shell thickness in meters.
- `struct_safety_factor` (float, default: 1.5): structural safety factor.
- `le_radius_constraint` (float, default: 0.7): lower bound on normalized leading-edge radius.
- `thickness_constraint` (float, default: 0.5): lower bound on normalized section thickness.
- `volume_constraint` (float, default: 1.0): lower bound on normalized wing volume.
- `chords` (list[float], default: inherited from generate-fea-mesh): section chord lengths.
- `sweeps` (list[float], default: inherited from generate-fea-mesh): section sweep angles.
- `dihedrals` (list[float], default: inherited from generate-fea-mesh): section dihedral angles.
- `spans` (list[float], default: inherited from generate-fea-mesh): section spans.
- `twists` (list[float], default: inherited from generate-fea-mesh): section twists.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for pressure-profile plots.
- `n_cpu_cores` (int, default: 1): MPI ranks/CPU cores.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroStructOptimizationInputs">`run-aero-struct-optimization` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroStructOptimizationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `optimizer` (str, default: "SNOPT"): optimization algorithm.
- `lift_constraint` (float, default: 0.5): target lift coefficient equality constraint.
- `angle_of_attack` (float, default: 3.0): initial freestream angle of attack in degrees.
- `airfoil_profiles` (list[str], default: inherited from generate-fea-mesh): section airfoil profiles used for CST fitting when needed.
- `mach_number` (float, default: inherited from generate-fea-mesh): freestream Mach number.
- `reynolds_number` (float, default: inherited from generate-fea-mesh): freestream Reynolds number.
- `max_opt_iters` (int, default: 100): maximum optimization iterations.
- `cst_coeffs` (list[float], default: None): optional flattened wing CST coefficient vector.
- `struct_material` (str, default: "aluminum"): structural material.
- `struct_panel_thickness` (float, default: 0.003): initial structural shell thickness in meters.
- `struct_safety_factor` (float, default: 1.5): structural safety factor.
- `le_radius_constraint` (float, default: 0.7): lower bound on normalized leading-edge radius.
- `thickness_constraint` (float, default: 0.5): lower bound on normalized section thickness.
- `volume_constraint` (float, default: 1.0): lower bound on normalized wing volume.
- `chords` (list[float], default: inherited from generate-fea-mesh): section chord lengths.
- `sweeps` (list[float], default: inherited from generate-fea-mesh): section sweep angles.
- `dihedrals` (list[float], default: inherited from generate-fea-mesh): section dihedral angles.
- `spans` (list[float], default: inherited from generate-fea-mesh): section spans.
- `twists` (list[float], default: inherited from generate-fea-mesh): section twists.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for pressure-profile plots.
- `n_cpu_cores` (int, default: 1): MPI ranks/CPU cores.

</div>
</div>
</div>

## Advanced Parameters

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateCfdMeshAdvanced">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateCfdMeshAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `blunt_te` (float, default: 0.01): trailing-edge bluntness as a fraction of chord.
- `surf_mesh_cells` (int, default: null): explicit surface tessellation cell count override.
- `n_layers` (int, default: null): explicit volume extrusion layer-count override.
- `trailing_edge_shape` (str, default: "rounded"): OpenVSP trailing-edge cap style.
- `tip_cluster` (float, default: 0.1): tip clustering factor.
- `le_cluster` (float, default: 0.1): leading-edge clustering factor.
- `te_cluster` (float, default: 0.1): trailing-edge clustering factor.
- `farfield_scale` (float, default: 20.0): outer-boundary distance scale.
- `d0` (float, default: -1.0): first-layer height in meters; use a negative value to estimate it from y_plus, mach_number, reynolds_number, and ref_chord.
- `hyperbolic_sweeps` (int, default: 10): smoothing sweeps per layer for hyperbolic extrusion.
- `neighbor_rings` (int, default: 10): neighbor-ring depth for the hyperbolic smoother.
- `diffuse_start` (float, default: null): smoothing onset distance in meters.
- `sym_axis` (str, default: "y"): symmetry plane axis passed to the volume mesh generator.
- `sym_decay` (float, default: -1.0): symmetry damping decay length.
- `max_nonorthogonality_pass` (float, default: 70.0): pass threshold for maximum non-orthogonality.
- `max_nonorthogonality_warning` (float, default: 80.0): warning threshold for maximum non-orthogonality.
- `max_aspect_ratio_pass` (float, default: 1000.0): pass threshold for maximum aspect ratio.
- `max_aspect_ratio_warning` (float, default: 10000.0): warning threshold for maximum aspect ratio.
- `max_skewness_pass` (float, default: 4.0): pass threshold for maximum skewness.
- `max_skewness_warning` (float, default: 6.0): warning threshold for maximum skewness.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateFeaMeshAdvanced">`generate-fea-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateFeaMeshAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- No skill-specific advanced parameters are currently defined for generate-fea-mesh.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroSimulationAdvanced">`run-aero-simulation` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroSimulationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (float, default: 0.4): Mach boundary used by default solver selection.
- `solver_name` (str, default: null): explicit solver override; leave unset to use the default wing solver.
- `max_flow_iters` (int, default: 10000): maximum flow iterations written to the case control settings.
- `primal_func_std_tol` (float, default: 5e-3): DAFoam primal function standard deviation tolerance.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance.
- `n_cst_coeffs` (int, default: 6): number of CST coefficients per surface used when prepare fits CST coefficients.
- `reference_area` (float, default: null): aerodynamic reference area override; if unset, the skill uses mean chord times span.
- `reference_length` (float, default: null): aerodynamic reference length override; if unset, the skill uses the mean chord.
- `coef_stddev_pct_pass` (float, default: 0.001): pass threshold for force-coefficient standard deviation in percent.
- `coef_stddev_pct_warning` (float, default: 1.0): warning threshold for force-coefficient standard deviation in percent.
- `residual_drop_orders_pass` (float, default: 6.0): pass threshold for minimum residual drop in log10 orders.
- `residual_drop_orders_warning` (float, default: 3.0): warning threshold for minimum residual drop in log10 orders.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroOptimizationAdvanced">`run-aero-optimization` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroOptimizationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (float, default: 0.4): Mach boundary used by default solver selection.
- `solver_name` (str, default: null): explicit solver override; leave unset to use the default wing solver.
- `max_flow_iters` (int, default: 10000): maximum flow iterations written to the case control settings.
- `primal_func_std_tol` (float, default: 5e-3): DAFoam primal function standard deviation tolerance.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance.
- `n_cst_coeffs` (int, default: 6): number of CST coefficients per surface used when prepare fits CST coefficients.
- `reference_area` (float, default: null): aerodynamic reference area override; if unset, the skill uses mean chord times span.
- `reference_length` (float, default: null): aerodynamic reference length override; if unset, the skill uses the mean chord.
- `objective_reduction_pct_pass` (float, default: 5.0): pass threshold for objective reduction in percent.
- `objective_reduction_pct_warning` (float, default: 1.0): warning threshold for objective reduction in percent.
- `final_feasibility_pass` (float, default: 0.0001): pass threshold for final feasibility.
- `final_feasibility_warning` (float, default: 0.01): warning threshold for final feasibility.
- `flow_residual_drop_orders_pass` (float, default: 6.0): pass threshold for minimum flow residual drop in log10 orders.
- `flow_residual_drop_orders_warning` (float, default: 3.0): warning threshold for minimum flow residual drop in log10 orders.
- `adjoint_residual_drop_orders_pass` (float, default: 5.0): pass threshold for minimum adjoint residual drop in log10 orders.
- `adjoint_residual_drop_orders_warning` (float, default: 1.0): warning threshold for minimum adjoint residual drop in log10 orders.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroStructSimulationAdvanced">`run-aero-struct-simulation` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroStructSimulationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (float, default: 0.4): Mach boundary used by default solver selection.
- `solver_name` (str, default: null): explicit solver override; leave unset to use the default wing solver.
- `primal_min_iters` (int, default: 200): minimum number of primal iterations.
- `primal_func_std_tol` (float, default: 1e-2): DAFoam primal function standard deviation tolerance.
- `primal_func_slope_tol` (float, default: 1e-2): DAFoam primal function slope tolerance.
- `n_cst_coeffs` (int, default: 6): number of CST coefficients per surface used when prepare fits CST coefficients.
- `reference_area` (float, default: null): aerodynamic reference area override; if unset, the skill uses mean chord times span.
- `reference_length` (float, default: null): aerodynamic reference length override; if unset, the skill uses the mean chord.
- `nlbgs_rel_tol` (float, default: 1e-7): relative tolerance for the aerostructural OpenMDAO NonlinearBlockGS solver.
- `nlbgs_abs_tol` (float, default: 2.0): absolute tolerance for the aerostructural OpenMDAO NonlinearBlockGS solver.
- `nlbgs_rel_tol_orders_pass` (float, default: 0.0): pass threshold for final relative NLBGS tolerance drop in log10 orders.
- `nlbgs_rel_tol_orders_warning` (float, default: 2.0): warning threshold for final relative NLBGS tolerance drop in log10 orders.
- `nlbgs_abs_tol_orders_pass` (float, default: 0.0): pass threshold for final absolute NLBGS tolerance drop in log10 orders.
- `nlbgs_abs_tol_orders_warning` (float, default: 2.0): warning threshold for final absolute NLBGS tolerance drop in log10 orders.
- `cd_delta_pass` (float, default: 1.0e-5): pass threshold for absolute CD delta between coupled iterations.
- `cd_delta_warning` (float, default: 1.0e-3): warning threshold for absolute CD delta between coupled iterations.
- `cl_delta_pass` (float, default: 1.0e-4): pass threshold for absolute CL delta between coupled iterations.
- `cl_delta_warning` (float, default: 1.0e-2): warning threshold for absolute CL delta between coupled iterations.
- `coef_stddev_pct_pass` (float, default: 0.001): pass threshold for force-coefficient standard deviation in percent.
- `coef_stddev_pct_warning` (float, default: 1.0): warning threshold for force-coefficient standard deviation in percent.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunAeroStructOptimizationAdvanced">`run-aero-struct-optimization` (click to expand)</a>
</div>
</div>
<div id="wingRunAeroStructOptimizationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `transonic_mach_boundary` (float, default: 0.4): Mach boundary used by default solver selection.
- `solver_name` (str, default: null): explicit solver override; leave unset to use the default wing solver.
- `primal_min_iters` (int, default: 200): minimum number of primal iterations.
- `primal_func_std_tol` (float, default: 1e-2): DAFoam primal function standard deviation tolerance.
- `primal_func_slope_tol` (float, default: 1e-2): DAFoam primal function slope tolerance.
- `n_cst_coeffs` (int, default: 6): number of CST coefficients per surface used when prepare fits CST coefficients.
- `reference_area` (float, default: null): aerodynamic reference area override; if unset, the skill uses mean chord times span.
- `reference_length` (float, default: null): aerodynamic reference length override; if unset, the skill uses the mean chord.
- `nlbgs_rel_tol` (float, default: 1e-7): relative tolerance for the aerostructural OpenMDAO NonlinearBlockGS solver.
- `nlbgs_abs_tol` (float, default: 2.0): absolute tolerance for the aerostructural OpenMDAO NonlinearBlockGS solver.
- `objective_reduction_pct_pass` (float, default: 5.0): pass threshold for objective reduction in percent.
- `objective_reduction_pct_warning` (float, default: 1.0): warning threshold for objective reduction in percent.
- `final_feasibility_pass` (float, default: 0.0001): pass threshold for final feasibility.
- `final_feasibility_warning` (float, default: 0.01): warning threshold for final feasibility.
- `flow_residual_drop_orders_pass` (float, default: 6.0): pass threshold for minimum flow residual drop in log10 orders.
- `flow_residual_drop_orders_warning` (float, default: 3.0): warning threshold for minimum flow residual drop in log10 orders.
- `adjoint_residual_drop_orders_pass` (float, default: 5.0): pass threshold for minimum adjoint residual drop in log10 orders.
- `adjoint_residual_drop_orders_warning` (float, default: 1.0): warning threshold for minimum adjoint residual drop in log10 orders.

</div>
</div>
</div>

## Agent Capability demos

### CFD Mesh Generation 

Users can prompt to generate wing CFD mesh with desired airfoil profiles, chords, sweeps, twists, dihedral, and span. For example, `Generate a cfd mesh for a wing with naca4412 at the root and naca0012 at the tip. The root chord is 1 m and the tip chord is 0.5 m. The tip twist is 1 deg. The semi-span is 3 m. The sweep is 10 degs. Mesh size 200K, yPlus 50.` The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-mesh.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-mesh-trame.png" style="width:400px !important;" />

Fig. 1. Left: Overview of the generated CFD mesh. Top right: Trame interactive view of the CFD mesh.

### FEA Mesh Generation 

Users can prompt to generate wing FEA mesh with desired ribs, spars, and the coverage of the wingbox in chordwise and spanwise direction. For example, `Generate a FEA mesh for this wing with 2 spars and 10 ribs. The total element is about 3000. The wingbox starts and ends from 20% to 80% chord and extends to 90% span.` The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-fea-mesh.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-fea-mesh-trame.png" style="width:400px !important;" />

Fig. 1. Left: Overview of the generated FEA mesh. Top right: Trame interactive view of the FEA mesh.

{% include links.html %}

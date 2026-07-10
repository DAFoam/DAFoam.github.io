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

- `custom_vsp3` (int, default: 0): if set to 1, copy user-supplied aircraft.vsp3 and vsp_design_vars.json from the working directory into this mesh case before applying any requested design-variable geometry changes.
- `airfoil_profiles` (list[str], default: ["rae2822", "rae2822", "rae2822"]): wing airfoil profile names ordered section 0 to section 2.
- `sweeps` (list[float], default: [35.0, 30.0]): wing sweep angles in degrees formatted as [break_sweep_deg, tip_sweep_deg].
- `twists` (list[float], default: [0.0, 0.0]): wing twist angles in degrees formatted as [section1_twist_deg, section2_twist_deg].
- `chords` (list[float], default: [8.0, 4.5, 1.7]): wing chord lengths for the packaged geometry.
- `spans` (list[float], default: [5.0, 14.0]): wing panel semi-span values.
- `dihedrals` (list[float], default: [6.0, 6.0]): wing dihedral angles in degrees.
- `tail_twist` (float, default: 0.0): tail twist angle in degrees.
- `n_cpus` (int, default: 2): MPI ranks used for the parallel snappyHexMesh passes.
- `surface_level` (int, default: 7): snappyHexMesh surface refinement level.
- `n_boundary_layers` (int, default: 8): number of prism layers.
- `local_refine_box` (list[list[float]], default: None): optional two-corner local refinement box `[[x0, y0, z0], [x1, y1, z1]]`; leave unset for no local refinement.

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

- `angle_of_attack` (float, default: 2.0): freestream angle of attack in degrees.
- `fixed_lift_coeff` (float, default: -1.0): automatically vary the angle of attack to compute drag at the prescribed lift coefficient. Set it to -1.0 to disable.
- `mach_number` (float, default: 0.3): freestream Mach number.
- `reynolds_number` (float, default: 1000000.0): freestream Reynolds number.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): wing airfoil profiles used for CST fitting when needed.
- `cst_coeffs` (list[float], default: None): optional flattened aircraft wing CST coefficient vector.
- `chords` (list[float], default: inherited from generate-cfd-mesh): wing chord values.
- `spans` (list[float], default: inherited from generate-cfd-mesh): wing semi-span values.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): wing sweep values.
- `twists` (list[float], default: inherited from generate-cfd-mesh): wing twist values.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): wing dihedral values.
- `tail_twist` (float, default: inherited from generate-cfd-mesh): tail twist angle.
- `n_cpu_cores` (int, default: 1): MPI ranks/CPU cores.

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

- `angle_of_attack` (float, default: 2.0): initial freestream angle of attack in degrees.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): wing airfoil profiles used for CST fitting when needed.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number.
- `reynolds_number` (float, default: 1000000.0): freestream Reynolds number.
- `optimizer` (str, default: "SLSQP"): optimization algorithm.
- `lift_constraint` (float, default: 0.5): target lift coefficient equality constraint.
- `le_radius_constraint` (float, default: 0.7): lower bound on normalized leading-edge radius.
- `thickness_constraint` (float, default: 0.5): lower bound on normalized aircraft wing thickness.
- `volume_constraint` (float, default: 1.0): lower bound on normalized aircraft wing volume.
- `max_opt_iters` (int, default: 100): maximum optimization iterations.
- `cst_coeffs` (list[float], default: None): optional flattened aircraft wing CST coefficient vector.
- `chords` (list[float], default: inherited from generate-cfd-mesh): wing chord values.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): wing sweep values.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): wing dihedral values.
- `spans` (list[float], default: inherited from generate-cfd-mesh): wing semi-span values.
- `twists` (list[float], default: inherited from generate-cfd-mesh): wing twist values.
- `tail_twist` (float, default: inherited from generate-cfd-mesh): tail twist angle.
- `n_cpu_cores` (int, default: 1): MPI ranks/CPU cores.

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

- `max_cell_size` (float, default: null): target farfield `blockMesh` cell size used to size the outer box; if unset, the skill uses the mean wing chord.
- `line_level` (int, default: null): snappyHexMesh feature-edge refinement level; if unset, the skill uses `surface_level + 1`.
- `curvature_level` (int, default: null): snappyHexMesh curvature refinement level; if unset, the skill uses `surface_level + 2`, and `-1` disables curvature refinement.
- `n_layer_outer_iter` (int, default: 3): number of outer iterations used in `addLayersControls`.
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
<a data-toggle="collapse" href="#aircraftRunCfdSimulationAdvanced">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="aircraftRunCfdSimulationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `pressure_profile_fractions` (list[float], default: [0.2, 0.5, 0.9]): spanwise fractions used for pressure-profile plots.
- `transonic_mach_boundary` (float, default: 0.4): Mach boundary used by default solver selection.
- `solver_name` (str, default: null): explicit solver override; leave unset to use the default aircraft solver.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model ("SpalartAllmaras", "kOmegaSST").
- `max_flow_iters` (int, default: 10000): maximum flow iterations written to the case control settings.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance.
- `n_cst_coeffs` (int, default: 6): number of CST coefficients per surface used when `prepare` fits CST coefficients.
- `initialize_from` (str, default: null): warm-start source case name; leave unset for a cold start.
- `reference_area` (float, default: null): aerodynamic reference area override; if unset, the skill uses mean chord times span.
- `reference_length` (float, default: null): aerodynamic reference length override; if unset, the skill uses the mean chord.
- `force_std_pass` (float, default: 0.0001): pass threshold for raw force-coefficient standard deviation.
- `force_std_warning` (float, default: 0.05): warning threshold for raw force-coefficient standard deviation.
- `residual_drop_orders_pass` (float, default: 6.0): pass threshold for minimum residual drop in log10 orders.
- `residual_drop_orders_warning` (float, default: 3.0): warning threshold for minimum residual drop in log10 orders.
- `cp_plot_lower_bound` (float, default: -2.0): lower bound of the Cp axis and colorbar.
- `cp_plot_upper_bound` (float, default: 2.0): upper bound of the Cp axis and colorbar.
- `u_plot_lower_bound` (float, default: -1.0): lower bound of the normalized velocity colorbar.
- `u_plot_upper_bound` (float, default: 1.0): upper bound of the normalized velocity colorbar.

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

- `pressure_profile_fractions` (list[float], default: [0.2, 0.5, 0.9]): spanwise fractions used for pressure-profile plots.
- `transonic_mach_boundary` (float, default: 0.4): Mach boundary used by default solver selection.
- `solver_name` (str, default: null): explicit solver override; leave unset to use the default aircraft solver.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model ("SpalartAllmaras", "kOmegaSST").
- `max_flow_iters` (int, default: 10000): maximum flow iterations written to the case control settings.
- `max_adj_iters` (int, default: 1000): maximum GMRES iterations for the DAFoam adjoint linear solve.
- `pc_fill_level` (int, default: 1): ILU fill level for the DAFoam adjoint preconditioner.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance.
- `n_cst_coeffs` (int, default: 6): number of CST coefficients per surface used when `prepare` fits CST coefficients.
- `reference_area` (float, default: null): aerodynamic reference area override; if unset, the skill uses mean chord times span.
- `reference_length` (float, default: null): aerodynamic reference length override; if unset, the skill uses the mean chord.
- `objective_reduction_pct_pass` (float, default: 5.0): pass threshold for objective reduction in percent.
- `objective_reduction_pct_warning` (float, default: 1.0): warning threshold for objective reduction in percent.
- `final_feasibility_pass` (float, default: 0.0001): pass threshold for final feasibility.
- `final_feasibility_warning` (float, default: 0.01): warning threshold for final feasibility.
- `flow_residual_drop_orders_pass` (float, default: 6.0): pass threshold for minimum flow residual drop in log10 orders.
- `flow_residual_drop_orders_warning` (float, default: 3.0): warning threshold for minimum flow residual drop in log10 orders.
- `adjoint_residual_drop_orders_pass` (float, default: 5.0): pass threshold for minimum adjoint residual drop in log10 orders.
- `adjoint_residual_drop_orders_warning` (float, default: 3.0): warning threshold for minimum adjoint residual drop in log10 orders.
- `cp_plot_lower_bound` (float, default: -2.0): lower bound of the Cp axis and colorbar.
- `cp_plot_upper_bound` (float, default: 2.0): upper bound of the Cp axis and colorbar.
- `u_plot_lower_bound` (float, default: -1.0): lower bound of the normalized velocity colorbar.
- `u_plot_upper_bound` (float, default: 1.0): upper bound of the normalized velocity colorbar.

</div>
</div>
</div>

## Agent Capability demos

### CFD Mesh Generation 

Users can prompt to generate an aircraft CFD mesh with the pre-defined model (wing+fuselage+tails). The default model is similar to Boeing 737 and users can prescribe the desired wing sectional shapes (throgh CST coefficients), chords, sweeps, twists, dihedral, span, as well as the vertical tail rotation. For example, 

`Generate a cfd mesh for the default aircraft configuration. Use 8 cores` 

The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-geometry.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-mesh.png" style="width:400px !important;" />

Fig. 1. Left: The default aircraft geometry. Right: Overview of the generated CFD mesh.

### CFD-based Aerodynamic Simulation

Users can prompt to run CFD simulations for the aircraft with desired Mach number, Reynolds number, and angle of attack. For example, 

`Generate a cfd mesh for the default aircraft configuration. After that, run a cfd with aoa=2degs, The mach is 0.85 and the ref re is 2e7.` 

The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-cfd-p-profile.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-cfd-trame.png" style="width:400px !important;" />

Fig. 2. Left: Pressure profile from the CFD simulation. Right: Trame interactive view of the pressure contour.

### Compare various design options

Users can prompt to run multiple CFD simulations by varying any of the design variables defined in vsp_design_vars.json. For example, 

`Generate a cfd mesh for the default aircraft with about 0.5 million cells. Then, run a CFD simulation with aoa=2deg, Ma=0.85, Re=1e7. Then, run another CFD simulation with the same condition butt increasing the span by 20%. Compare the CD/CL between these two CFD simulations. For both mesh and CFD, use 4 cores.`

The following is the AI generated pictures. We can compare the CD/CL for the original span and +20% span designs.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-vary-span-orig.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-vary-span-20p.png" style="width:400px !important;" />

Fig. 3. Left: Pressure contour of the original span design. Right: Pressure contour of the +20% span design.

### Use customized aircraft configurations

Instead of using the default Boeing 737 configuration in `aircraft.vsp3`, you can use a customized OpenVSP aircraft configuration for the agent. First, download the Cessna 172 configuration file: [aircraft_c172.vsp3](https://github.com/DAFoam/mdo_agent_work/releases/download/v1.0/aircraft_c172.vsp3). The Cessna 172 vsp3 file was downloaded and modified from the [OpenVSP Airshow](https://airshow.openvsp.org/). Rename it to `aircraft.vsp3` and place it in your `mdo_agent_work/results` folder (working directory).

Then, you can ask the agent to simulate your customized configuration. For example:

`Generate a CFD mesh for my customized aircraft.vsp3 geometry. The mesh should have about 0.5 million cells. Then, run a CFD simulation with aoa=2 deg, Ma=0.3, and Re=5e6. Next, run another CFD simulation with the same condition but increase the wing sweep by 20 deg. Compare the CD/CL between these two CFD simulations. For both mesh generation and CFD simulations, use 4 cores.`

Note: You can optionally provide a `vsp_design_vars.json` file to specify which OpenVSP design variables the aircraft agent is allowed to modify. This file should list the component, group, and variable name for each design variable. You can find these names in the OpenVSP GUI by clicking the corresponding variables. If you do not provide a `vsp_design_vars.json` file, the agent will generate one for you based on your prompt.

The following are the AI-generated pictures. We can compare the CD/CL values between the original sweep design and the design with 20 deg increased sweep.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-orig.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-20d.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-orig-p.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-20d-p.png" style="width:400px !important;" />

Fig. 4. Example of using customized aircraft.vsp3. Left: original design. Right: +20 sweep design.

{% include links.html %}

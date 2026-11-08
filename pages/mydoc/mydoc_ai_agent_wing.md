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
- `generate-fea-mesh`: build the wingbox FEA mesh for an existing wing CFD mesh.
- `generate-aero-struct-mesh`: build both the CFD mesh and the wingbox FEA mesh in one case; this is the prerequisite for the aero-structural skills.
- `run-cfd-simulation`: run steady aerodynamic CFD from an existing wing mesh.
- `run-aero-optimization`: run single-point or multipoint aerodynamic shape optimization for the wing.
- `run-aero-struct-simulation`: run coupled aero-structural analysis.
- `run-aero-struct-optimization`: run coupled aero-structural optimization (drag or wingbox-mass objective, single or multiple load factors).

## Standard Inputs

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateCfdMeshInputs">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateCfdMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profiles` (list[str], default: ["naca0012", "naca0012"]): N sectional airfoil profile names ordered wing root to tip.
- `chords` (list[float], default: [1.0, 1.0]): N sectional chord lengths in meters ordered wing root to tip.
- `spans` (list[float], default: [3.0]): N-1 sectional HALF-WING SPAN lengths in meters, one per span segment ordered wing root to tip.
- `sweeps` (list[float], default: [0.0]): N-1 sectional leading-edge sweep angles in degrees, one per span segment ordered wing root to tip.
- `dihedrals` (list[float], default: [0.0]): N-1 sectional dihedral angles in degrees, one per span segment ordered wing root to tip.
- `twists` (list[float], default: [0.0]): N-1 sectional twist angles in degrees, one per span segment ordered wing root to tip. Positive is nose-up.
- `mesh_cells` (int, default: 200000): target total volume mesh cell count for the wing.
- `y_plus` (float, default: 50.0): target near-wall mesh spacing (`y+` or `yPlus`) for the wing mesh generation.
- `mach_number` (float, default: 0.2): reference Mach number (Ma) for wing mesh generation.
- `reynolds_number` (float, default: 5e6): reference Reynolds number for wing mesh generation when altitude is null; with altitude, mesh sizing calculates it after generating the wing geometry.
- `altitude` (float, default: None): optional standard-atmosphere altitude in meters (0 to 20000). When set, the configured OpenVSP wing MAC determines the CFD Reynolds number after geometry generation.
- `local_refine_box` (list[list[float]], default: None): optional two-corner local refinement box `[[x0, y0, z0], [x1, y1, z1]]`. Leave unset for no local refinement.

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
- `total_elements_target` (int, default: 3000): requested total number of shell elements for the wingbox mesh.
- `wingbox_span` (float, default: 0.95): fraction of the modeled HALF-WING SPAN covered by the wingbox layout. Default: 0.95.
- `wingbox_chord_start` (float, default: 0.2): wingbox front spar position as a fraction of local chord.
- `wingbox_chord_end` (float, default: 0.8): wingbox rear spar position as a fraction of local chord.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateAeroStructMeshInputs">`generate-aero-struct-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateAeroStructMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profiles` (list[str], default: ["naca0012", "naca0012"]): N sectional airfoil profile names ordered wing root to tip.
- `chords` (list[float], default: [1.0, 1.0]): N sectional chord lengths in meters ordered wing root to tip.
- `spans` (list[float], default: [3.0]): N-1 sectional HALF-WING SPAN lengths in meters, one per span segment ordered wing root to tip.
- `sweeps` (list[float], default: [0.0]): N-1 sectional leading-edge sweep angles in degrees, one per span segment ordered wing root to tip.
- `dihedrals` (list[float], default: [0.0]): N-1 sectional dihedral angles in degrees, one per span segment ordered wing root to tip.
- `twists` (list[float], default: [0.0]): N-1 sectional twist angles in degrees, one per span segment ordered wing root to tip. Positive is nose-up.
- `mesh_cells` (int, default: 200000): target total volume mesh cell count for the wing.
- `y_plus` (float, default: 50.0): target near-wall mesh spacing (`y+` or `yPlus`) for the wing mesh generation.
- `mach_number` (float, default: 0.2): reference Mach number (Ma) for wing mesh generation.
- `reynolds_number` (float, default: 5e6): reference Reynolds number for wing mesh generation when altitude is null; with altitude, mesh sizing calculates it after generating the wing geometry.
- `altitude` (float, default: None): optional standard-atmosphere altitude in meters (0 to 20000). When set, the configured OpenVSP wing MAC determines the CFD Reynolds number after geometry generation.
- `local_refine_box` (list[list[float]], default: None): optional two-corner local refinement box `[[x0, y0, z0], [x1, y1, z1]]`. Leave unset for no local refinement.
- `n_ribs` (int, default: 10): number of ribs in the spanwise direction.
- `n_spars` (int, default: 2): number of spars in the chordwise direction.
- `total_elements_target` (int, default: 3000): requested total number of shell elements for the wingbox mesh.
- `wingbox_span` (float, default: 0.95): fraction of the modeled HALF-WING SPAN covered by the wingbox layout. Default: 0.95.
- `wingbox_chord_start` (float, default: 0.2): wingbox front spar position as a fraction of local chord.
- `wingbox_chord_end` (float, default: 0.8): wingbox rear spar position as a fraction of local chord.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunCfdSimulationInputs">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="wingRunCfdSimulationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 2.0): freestream angle of attack (AoA) in degrees.
- `fixed_lift_coeff` (float, default: -1.0): automatically vary the angle of attack to compute drag at the prescribed lift coefficient. Set it to -1.0 to disable.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): section airfoil profile names inherited from generate-cfd-mesh.
- `mach_number` (float, default: inherited from generate-cfd-mesh): reference Mach number. Inherited from generate-cfd-mesh if not provided.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): reference Reynolds number. Inherited from generate-cfd-mesh if not provided.
- `altitude` (float, default: inherited from generate-cfd-mesh): optional standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds uses the wing reference length and overrides a supplied value.
- `chords` (list[float], default: inherited from generate-cfd-mesh): section chord lengths inherited from generate-cfd-mesh.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): section leading-edge sweep angles inherited from generate-cfd-mesh.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): section dihedral angles inherited from generate-cfd-mesh.
- `spans` (list[float], default: inherited from generate-cfd-mesh): sectional HALF-WING SPAN lengths in meters inherited from generate-cfd-mesh.
- `twists` (list[float], default: inherited from generate-cfd-mesh): section twist angles inherited from generate-cfd-mesh.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

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

- `angle_of_attack` (float, default: 2.0): initial freestream angle of attack (AoA) in degrees.
- `airfoil_profiles` (list[str], default: inherited from generate-cfd-mesh): section airfoil profile names inherited from generate-cfd-mesh.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number. Inherited from generate-cfd-mesh if not provided.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): freestream Reynolds number. Inherited from generate-cfd-mesh if not provided.
- `altitude` (float, default: inherited from generate-cfd-mesh): optional standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds uses the wing reference length and overrides a supplied value.
- `optimizer` (str, default: "Uno"): optimization algorithm to use. Options are Uno (default), SLSQP, SNOPT, and EGO. The number of CST coefficients per airfoil surface is set by the advanced parameter `profile_fit_coeff_count` (default 6).
- `lift_constraint` (list[float], default: [0.5]): target lift coefficient lower bound for each optimization point. Supply more than one entry for multipoint optimization; its length must equal `multipoint_weight`.
- `multipoint_weight` (list[float], default: [1.0]): objective weight for each optimization point. Provide one entry per `lift_constraint` value; weights must sum to 1.0.
- `active_design_vars` (list[str], default: ["cst_coeffs", "twists"]): design variable groups the optimizer may change. Supported values: cst_coeffs, twists, spans, sweeps, dihedrals, chords (section tip chords), wing_root_chord.
- `le_radius_constraint` (float, default: 0.7): lower bound on leading-edge radius constraint; normalized wrt the baseline radius (1.0). Set to a negative value to disable it.
- `thickness_constraint` (float, default: 0.5): lower bound on airfoil thickness constraint; normalized wrt the baseline thickness (1.0). Set to a negative value to disable it.
- `camber_curvature_constraint` (int, default: 0): camber-line smoothness constraint that prevents wavy optimized airfoil shapes. 1 to enable, 0 to disable (default).
- `volume_constraint` (float, default: 1.0): lower bound on airfoil volume constraint; normalized wrt the baseline volume (1.0). Set to a negative value to disable it.
- `area_constraint` (float, default: -1.0): upper bound on wing planform area constraint; normalized wrt the baseline area (1.0). Set to a negative value to disable it.
- `same_profile_constraint` (int, default: 0): set to 1 to keep the airfoil profile (CST coefficients) of every wing section identical via linear equality constraints; applies only when cst_coeffs is active. Use 0 to disable it.
- `max_opt_iters` (int, default: 50): maximum number of optimization iterations.
- `n_ego_doe_pts` (int, default: 20): number of initial design of experiment (DOE) sample points used by the EGO optimizer.
- `chords` (list[float], default: inherited from generate-cfd-mesh): section chord lengths inherited from generate-cfd-mesh.
- `sweeps` (list[float], default: inherited from generate-cfd-mesh): section leading-edge sweep angles inherited from generate-cfd-mesh.
- `dihedrals` (list[float], default: inherited from generate-cfd-mesh): section dihedral angles inherited from generate-cfd-mesh.
- `spans` (list[float], default: inherited from generate-cfd-mesh): sectional HALF-WING SPAN lengths in meters inherited from generate-cfd-mesh.
- `twists` (list[float], default: inherited from generate-cfd-mesh): section twist angles inherited from generate-cfd-mesh.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

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

- `angle_of_attack` (float, default: 3.0): freestream angle of attack (AoA) in degrees.
- `fixed_force` (int, default: 0): automatically vary the angle of attack to compute drag at the force balance lift=weight. 0: disable. 1: enable
- `airfoil_profiles` (list[str], default: inherited from generate-aero-struct-mesh): section airfoil profile names inherited from generate-aero-struct-mesh.
- `mach_number` (float, default: inherited from generate-aero-struct-mesh): freestream Mach number inherited from generate-aero-struct-mesh when omitted.
- `reynolds_number` (float, default: inherited from generate-aero-struct-mesh): freestream Reynolds number inherited from generate-aero-struct-mesh when omitted.
- `altitude` (float, default: inherited from generate-aero-struct-mesh): optional standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds uses the wing reference length and overrides a supplied value.
- `ref_half_mass` (float, default: 10000.0): reference half-aircraft mass in kg, excluding the modeled half-wingbox mass.
- `struct_panel_thickness` (float, default: 0.01): initial structural shell thickness in meters.
- `stiffener_pitch` (float, default: 0.2): stiffener spacing in meters, transverse to the stiffeners (default 0.2 m).
- `stiffener_height` (float, default: 0.02): initial stiffener height in meters (default 0.02 m).
- `stiffener_thickness` (float, default: 0.005): initial stiffener thickness in meters (default 5 mm).
- `stiffener_flange_fraction` (float, default: 1.0): dimensionless ratio of stiffener flange width to stiffener height.
- `struct_safety_factor` (float, default: 1.5): safety factor used for the structural failure constraint.
- `le_radius_constraint` (float, default: 0.7): lower bound on leading-edge radius constraint; normalized wrt the baseline radius (1.0). Set to a negative value to disable it.
- `thickness_constraint` (float, default: 0.5): lower bound on airfoil thickness constraint; normalized wrt the baseline thickness (1.0). Set to a negative value to disable it.
- `volume_constraint` (float, default: 1.0): lower bound on airfoil volume constraint; normalized wrt the baseline volume (1.0). Set to a negative value to disable it.
- `area_constraint` (float, default: -1.0): upper bound on wing planform area constraint; normalized wrt the baseline area (1.0). Set to a negative value to disable it.
- `chords` (list[float], default: inherited from generate-aero-struct-mesh): section chord lengths inherited from generate-aero-struct-mesh.
- `sweeps` (list[float], default: inherited from generate-aero-struct-mesh): section leading-edge sweep angles inherited from generate-aero-struct-mesh.
- `dihedrals` (list[float], default: inherited from generate-aero-struct-mesh): section dihedral angles inherited from generate-aero-struct-mesh.
- `spans` (list[float], default: inherited from generate-aero-struct-mesh): sectional HALF-WING SPAN lengths in meters inherited from generate-aero-struct-mesh.
- `twists` (list[float], default: inherited from generate-aero-struct-mesh): section twist angles inherited from generate-aero-struct-mesh.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

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

- `optimizer` (str, default: "Uno"): optimization algorithm to use. Options are Uno (default), SLSQP, SNOPT, and EGO. EGO requires a non-empty `struct_dv_interp_eta`.
- `objective` (list[str], default: ["drag"]): objective function for each `load_factor` point: `drag` (wing CD) or `mass` (wingbox mass); its length must equal `load_factor`.
- `n_ego_doe_pts` (int, default: 20): number of initial design of experiment (DOE) sample points used by the EGO optimizer.
- `struct_dv_interp_eta` (list[float], default: []): piecewise-linearly interpolated structural DVs (panels and stiffeners). Set to [0, 1] to interpolate from root to tip, and add intermediate span fractions (e.g. [0, 0.3, 1]) if needed. Empty (default) keeps independent DVs for every panel. EGO requires a non-empty value.
- `angle_of_attack` (float, default: 3.0): initial freestream angle of attack (AoA) in degrees.
- `load_factor` (list[float], default: [1.0]): wing load factor for each optimization point. Supply more than one entry for multipoint optimization; its length must equal `multipoint_weight`.
- `multipoint_weight` (list[float], default: [1.0]): objective weight for each optimization point. Provide one entry per `load_factor` value; weights must sum to 1.0.
- `airfoil_profiles` (list[str], default: inherited from generate-aero-struct-mesh): section airfoil profile names inherited from generate-aero-struct-mesh.
- `mach_number` (float, default: inherited from generate-aero-struct-mesh): freestream Mach number inherited from generate-aero-struct-mesh when omitted.
- `reynolds_number` (float, default: inherited from generate-aero-struct-mesh): freestream Reynolds number inherited from generate-aero-struct-mesh when omitted.
- `altitude` (float, default: inherited from generate-aero-struct-mesh): optional standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds uses the wing reference length and overrides a supplied value.
- `max_opt_iters` (int, default: 100): maximum number of optimization iterations.
- `ref_half_mass` (float, default: 10000.0): reference half-aircraft mass in kg, excluding the modeled half-wingbox mass.
- `struct_panel_thickness` (float, default: 0.003): initial structural shell thickness in meters.
- `stiffener_pitch` (float, default: 0.2): stiffener spacing in meters, transverse to the stiffeners (default 0.2 m).
- `stiffener_height` (float, default: 0.02): initial stiffener height in meters (default 0.02 m).
- `stiffener_thickness` (float, default: 0.005): initial stiffener thickness in meters (default 5 mm).
- `stiffener_flange_fraction` (float, default: 1.0): dimensionless ratio of stiffener flange width to stiffener height.
- `struct_safety_factor` (float, default: 1.5): safety factor used for the structural failure constraint.
- `active_design_vars` (list[str], default: ["cst_coeffs", "twists"]): wing shape design variable groups the optimizer may change. Supported values: cst_coeffs, twists, spans, sweeps, dihedrals, chords (section tip chords), wing_root_chord.
- `le_radius_constraint` (float, default: 0.7): lower bound on leading-edge radius constraint; normalized wrt the baseline radius (1.0). Set to a negative value to disable it.
- `thickness_constraint` (float, default: 0.5): lower bound on airfoil thickness constraint; normalized wrt the baseline thickness (1.0). Set to a negative value to disable it.
- `camber_curvature_constraint` (int, default: 0): camber-line smoothness constraint that prevents wavy optimized airfoil shapes. 1 to enable, 0 to disable (default).
- `volume_constraint` (float, default: 1.0): lower bound on airfoil volume constraint; normalized wrt the baseline volume (1.0). Set to a negative value to disable it.
- `area_constraint` (float, default: -1.0): upper bound on wing planform area constraint; normalized wrt the baseline area (1.0). Set to a negative value to disable it.
- `chords` (list[float], default: inherited from generate-aero-struct-mesh): section chord lengths inherited from generate-aero-struct-mesh.
- `sweeps` (list[float], default: inherited from generate-aero-struct-mesh): section leading-edge sweep angles inherited from generate-aero-struct-mesh.
- `dihedrals` (list[float], default: inherited from generate-aero-struct-mesh): section dihedral angles inherited from generate-aero-struct-mesh.
- `spans` (list[float], default: inherited from generate-aero-struct-mesh): sectional HALF-WING SPAN lengths in meters inherited from generate-aero-struct-mesh.
- `twists` (list[float], default: inherited from generate-aero-struct-mesh): section twist angles inherited from generate-aero-struct-mesh.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

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

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `farfield_scale` (float, default: 20.0): outer-boundary distance scale used to compute the volume-mesh march distance as `farfield_scale * root_chord`.
- `neighbor_rings` (int, default: null): neighbor-ring depth used by the diffusion mesh extrusion smoother. Leave null to auto-scale with total mesh cells; set an int to override.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for wing pressure-profile plots, for example `[0.2, 0.4, 0.8]`.
- `blunt_te` (float, default: 0.01): trailing-edge bluntness as a fraction of chord.
- `surf_mesh_cells` (int, default: null): surface tessellation cell count used for wing.xyz generation density. Set together with n_layers to override mesh_cells-based auto sizing.
- `n_layers` (int, default: null): number of extrusion layers for the volume mesh. Set together with surf_mesh_cells to override mesh_cells-based auto sizing.
- `trailing_edge_shape` (str, default: "rounded"): trailing-edge cap style for OpenVSP. Use `rounded` (default) or `flat`.
- `tip_cluster` (float, default: 0.1): spanwise clustering factor at the tip, where 0 is dense and 1 is uniform.
- `le_cluster` (float, default: 0.1): chordwise clustering factor at the leading edge, where 0 is dense and 1 is uniform.
- `te_cluster` (float, default: 0.1): chordwise clustering factor at the trailing edge, where 0 is dense and 1 is uniform.
- `d0` (float, default: -1.0): first-layer height in meters. Use a negative value to let the wrapper use `y_plus`, `mach_number`, and `reynolds_number` instead.
- `diffusion_sweeps` (int, default: 10): number of smoothing sweeps per layer for diffusion mesh extrusion.
- `diffuse_start` (float, default: null): smoothing onset distance in meters. If null, mesh wrapper default behavior is used.
- `sym_axis` (str, default: "y"): symmetry plane axis passed to the volume mesh generator.
- `sym_decay` (float, default: -1.0): symmetry damping decay length. Use a negative value to let mdo_agent_mesh compute it automatically.
- `max_nonorthogonality_thresholds` (list[float], default: [70.0, 80.0]): [Pass, Warning] thresholds for maximum non-orthogonality.
- `max_aspect_ratio_thresholds` (list[float], default: [1000.0, 10000.0]): [Pass, Warning] thresholds for maximum aspect ratio.
- `max_skewness_thresholds` (list[float], default: [4.0, 6.0]): [Pass, Warning] thresholds for maximum skewness.

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

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingGenerateAeroStructMeshAdvanced">`generate-aero-struct-mesh` (click to expand)</a>
</div>
</div>
<div id="wingGenerateAeroStructMeshAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- Same advanced parameters as `generate-cfd-mesh`.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#wingRunCfdSimulationAdvanced">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="wingRunCfdSimulationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `cst_coeffs` (list[float], default: null): user-supplied wing CST coefficients, ordered section by section as `[upper..., lower...]`. `len(cst_coeffs)` must equal `2 * profile_fit_coeff_count * number_of_sections`. Set this only to parameterize the wing sections with explicit numeric CST values; leave it null (default) to use the named profiles in `airfoil_profiles`.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `plot_tail_fraction` (float, default: 1.0): fraction of the CD/CL/CM history to plot from the end. 1.0 plots the full history; 0.2 plots the final 20 percent.
- `force_std_thresholds` (list[float], default: [0.0001, 0.05]): [Pass, Warning] thresholds for raw force-coefficient standard deviation.
- `initialize_from` (str, default: null): warm-start source case name. When set, the field staged into 0/ is kept instead of resetting to the uniform freestream.
- `max_flow_iters` (int, default: 10000): maximum number of flow iterations written to the case controlDict endTime/writeInterval settings.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for wing pressure-profile plots, for example `[0.2, 0.4, 0.8]`.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum residual drop in log10 orders.

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

- `adjoint_residual_drop_orders_thresholds` (list[float], default: [5.0, 3.0]): [Pass, Warning] thresholds for minimum adjoint residual drop in log10 orders.
- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `cst_coeffs` (list[float], default: null): user-supplied wing CST coefficients, ordered section by section as `[upper..., lower...]`. `len(cst_coeffs)` must equal `2 * profile_fit_coeff_count * number_of_sections`. Set this only to parameterize the wing sections with explicit numeric CST values; leave it null (default) to use the named profiles in `airfoil_profiles`.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `dv_bounds` (dict[str, list[float]], default: {"CSTCoeffs": [-0.4, 0.4], "Twist": [-5.0, 5.0], "Sweep": [-15.0, 15.0], "Dihedral": [0.0, 5.0], "AoA": [0.0, 10.0], "Span": [0.5, 1.5], "Chord": [0.5, 1.5], "Wing_Root_Chord": [1.0, 1.0]}): design-variable lower/upper bounds shared by EGO and regular optimization. All keys are required. Span, Chord (section tip chords), and Wing_Root_Chord (root chord of the whole wing) are multipliers of the baseline value, e.g. [0.9, 1.1] is +-10%; all other keys are absolute values (degrees for Twist, Sweep, Dihedral, AoA). Wing_Root_Chord defaults to be fixed with bounds [1.0, 1.0].
- `final_feasibility_thresholds` (list[float], default: [0.0001, 0.01]): [Pass, Warning] thresholds for final feasibility.
- `flow_residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum flow residual drop in log10 orders.
- `max_adj_iters` (int, default: 1000): maximum GMRES iterations used by the DAFoam adjoint linear solve.
- `max_flow_iters` (int, default: 10000): maximum number of flow iterations written to the case controlDict endTime/writeInterval settings.
- `objective_reduction_pct_thresholds` (list[float], default: [5.0, 1.0]): [Pass, Warning] thresholds for objective reduction in percent.
- `pc_fill_level` (int, default: 1): ILU fill level used by the DAFoam adjoint preconditioner.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for wing pressure-profile plots, for example `[0.2, 0.4, 0.8]`.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `n_multi_start` (int, default: 20): number of multi-start points for the EGO internal EI optimization.
- `ei_tol` (float, default: 0.0001): EGO internal expected improvement (EI) optimization tolerance.
- `ego_seed` (int, default: 0): random seed used by the EGO optimizer DOE and infill sampling.
- `ego_tol` (float, default: 0.001): objective variation tolerance for the EGO optimization.
- `ego_cstr_tol` (float, default: 0.001): constraint tolerance used by EGO and its lift-trim searches.

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

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `cst_coeffs` (list[float], default: null): user-supplied wing CST coefficients, ordered section by section as `[upper..., lower...]`. `len(cst_coeffs)` must equal `2 * profile_fit_coeff_count * number_of_sections`. Set this only to parameterize the wing sections with explicit numeric CST values; leave it null (default) to use the named profiles in `airfoil_profiles`.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `force_std_thresholds` (list[float], default: [0.0001, 0.05]): [Pass, Warning] thresholds for raw force-coefficient standard deviation.
- `initialize_from` (str, default: null): warm-start source case name. When set, the field staged into 0/ is kept instead of resetting to the uniform freestream.
- `nlbgs_abs_tol` (float, default: 2.0): absolute tolerance for the aerostructural OpenMDAO `NonlinearBlockGS` nonlinear block Gauss-Seidel solver.
- `nlbgs_rel_tol` (float, default: 1e-7): relative tolerance for the aerostructural OpenMDAO `NonlinearBlockGS` nonlinear block Gauss-Seidel solver.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for wing pressure-profile plots, for example `[0.2, 0.4, 0.8]`.
- `primal_func_slope_tol` (float, default: 0.0001): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.05): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `primal_min_iters` (int, default: 100): minimum number of primal iterations. This also sets the `nSteps` window used by the primal function standard deviation convergence check.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `struct_material` (str, default: "aluminum"): structural material. Currently only `aluminum` is supported.
- `nlbgs_rel_tol_orders_thresholds` (list[float], default: [0.0, 2.0]): [Pass, Warning] thresholds for final relative NLBGS tolerance drop in log10 orders.
- `nlbgs_abs_tol_orders_thresholds` (list[float], default: [0.0, 2.0]): [Pass, Warning] thresholds for final absolute NLBGS tolerance drop in log10 orders.
- `cd_delta_thresholds` (list[float], default: [1e-5, 0.001]): [Pass, Warning] thresholds for absolute CD delta between coupled iterations.
- `cl_delta_thresholds` (list[float], default: [0.0001, 0.01]): [Pass, Warning] thresholds for absolute CL delta between coupled iterations.

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

- `adjoint_residual_drop_orders_thresholds` (list[float], default: [5.0, 3.0]): [Pass, Warning] thresholds for minimum adjoint residual drop in log10 orders.
- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `cst_coeffs` (list[float], default: null): user-supplied wing CST coefficients, ordered section by section as `[upper..., lower...]`. `len(cst_coeffs)` must equal `2 * profile_fit_coeff_count * number_of_sections`. Set this only to parameterize the wing sections with explicit numeric CST values; leave it null (default) to use the named profiles in `airfoil_profiles`.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `dv_bounds` (dict[str, list[float]], default: {"CSTCoeffs": [-0.4, 0.4], "Twist": [-5.0, 5.0], "Sweep": [-15.0, 15.0], "Dihedral": [0.0, 5.0], "AoA": [0.0, 10.0], "Span": [0.5, 1.5], "Chord": [0.5, 1.5], "Wing_Root_Chord": [1.0, 1.0]}): design-variable lower/upper bounds shared by EGO and regular optimization. All keys are required. Span, Chord (section tip chords), and Wing_Root_Chord (root chord of the whole wing) are multipliers of the baseline value, e.g. [0.9, 1.1] is +-10%; all other keys are absolute values (degrees for Twist, Sweep, Dihedral, AoA). Wing_Root_Chord defaults to be fixed with bounds [1.0, 1.0].
- `final_feasibility_thresholds` (list[float], default: [0.0001, 0.01]): [Pass, Warning] thresholds for final feasibility.
- `flow_residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum flow residual drop in log10 orders.
- `max_adj_iters` (int, default: 1000): maximum GMRES iterations used by the DAFoam adjoint linear solve.
- `nlbgs_abs_tol` (float, default: 2.0): absolute tolerance for the aerostructural OpenMDAO `NonlinearBlockGS` nonlinear block Gauss-Seidel solver.
- `nlbgs_rel_tol` (float, default: 1e-7): relative tolerance for the aerostructural OpenMDAO `NonlinearBlockGS` nonlinear block Gauss-Seidel solver.
- `objective_reduction_pct_thresholds` (list[float], default: [5.0, 1.0]): [Pass, Warning] thresholds for objective reduction in percent.
- `pc_fill_level` (int, default: 1): ILU fill level used by the DAFoam adjoint preconditioner.
- `pressure_profile_fractions` (list[float], default: [0.1, 0.5, 0.9]): spanwise fractions used for wing pressure-profile plots, for example `[0.2, 0.4, 0.8]`.
- `primal_func_slope_tol` (float, default: 0.0001): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.05): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `primal_min_iters` (int, default: 100): minimum number of primal iterations. This also sets the `nSteps` window used by the primal function standard deviation convergence check.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `struct_material` (str, default: "aluminum"): structural material. Currently only `aluminum` is supported.
- `dv_bounds_structure` (dict[str, list[float]], default: {"PanelThickness": [0.002, 0.05], "StiffenerHeight": [0.01, 1.0], "StiffenerThickness": [0.002, 0.05]}): structural sizing design-variable lower/upper bounds in meters (absolute values). All keys are required.
- `n_multi_start` (int, default: 20): number of multi-start points for the EGO internal EI optimization.
- `ei_tol` (float, default: 0.0001): EGO internal expected improvement (EI) optimization tolerance.
- `ego_seed` (int, default: 0): random seed used by the EGO optimizer DOE and infill sampling.
- `ego_tol` (float, default: 0.001): objective variation tolerance for the EGO optimization.
- `ego_cstr_tol` (float, default: 0.001): constraint tolerance used by EGO.

</div>
</div>
</div>


## Agent Capability demos

### CFD Mesh Generation 

Users can prompt to generate wing CFD mesh with desired airfoil profiles, chords, sweeps, twists, dihedral, and span. For example, 

`Generate a cfd mesh for a wing with naca4412 at the root and naca0012 at the tip. The root chord is 1 m and the tip chord is 0.5 m. The tip twist is 1 deg. The semi-span is 3 m. The sweep is 10 degs. Mesh size 200K, yPlus 50.` 

The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-mesh.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-mesh-trame.png" style="width:400px !important;" />

Fig. 1. Left: Overview of the generated CFD mesh. Right: Trame interactive view of the CFD mesh.

### CFD-based Aerodynamic Simulation

Users can prompt to run wing CFD simulations with desired Mach number, Reynolds number, and angle of attack. For example, 

`Generate a cfd mesh for a wing with RAE2822 airfoils. The root chord is 1 m and the tip chord is 0.5 m. The sweep is 15 degs, and the semi span is 4 m. The tip twist is 1 deg. After that, run a cfd with aoa=3degs, The ref mach is 0.8 and the ref re is 1e7.` 

The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-p-profile.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-trame.png" style="width:400px !important;" />

Fig. 2. Left: Pressure profile from the CFD simulation. Right: Trame interactive view of the pressure contour.

### FEA Mesh Generation 

Users can prompt to generate wing FEA mesh with desired ribs, spars, and the coverage of the wingbox in chordwise and spanwise direction. For example, 

`Generate a cfd mesh for a wing with naca4412 at the root and naca0012 at the tip. The root chord is 1 m and the tip chord is 0.5 m. The tip twist is 1 deg. The semi-span is 3 m. The sweep is 10 degs. Mesh size 200K, yPlus 50. Also generate a FEA mesh for this wing with 2 spars and 10 ribs. The total element is about 3000. The wingbox starts and ends from 20% to 80% chord and extends to 90% span.` 

The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-fea-mesh.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-fea-mesh-trame.png" style="width:400px !important;" />

Fig. 3. Left: Overview of the generated FEA mesh. Right: Trame interactive view of the FEA mesh.

### CFD+FEA-based Aero-structural Simulation

Users can prompt to run wing aero-structural simulations with desired Mach number, Reynolds number, and angle of attack. For example, you can follow the above FEA mesh generation chat session and ask 

`Run an aero-structural simulation for this wing with aoa=4 degs, ma 0.3, re 5e6. Use 4 cores` 

The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-aero-struct-flow-res.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-aero-struct-stress.png" style="width:400px !important;" />

Fig. 4. Left: Flow residual of the aero-structural coupled simulation. Right: Trame interactive view of the von-Mises stress of the wing box.

### Aerodynamic Shape Optimization

Users can prompt to run wing aerodynamic shape optimization with desired Mach number, Reynolds number, and target lift constraint. For example,

`Generate a CFD mesh for the wing with 100K cells. Then, run an aerodynamic optimization with Ma=0.3, Re=5e6, and CL=0.3. Run for 50 iterations. Use 48 cores.` 

The case ran on the HPC. After it is finished, you need to resume the chat and ask it to analyze the optimization. The following is the AI generated pictures. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-aero-opt-conv-cd.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-aero-opt-conv-cl.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-aero-opt-pressure.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-aero-opt-trame.png" style="width:400px !important;" />

Fig. 5. Top: Optimization convergence history for CD and CL. Bot left: pressure profiles. Bot right: trame server view.

{% include links.html %}

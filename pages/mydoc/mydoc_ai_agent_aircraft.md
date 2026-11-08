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

- `generate-cfd-mesh`: build the aircraft CFD mesh and mesh-quality outputs, optionally applying OpenVSP geometry changes before meshing.
- `run-cfd-simulation`: run steady aircraft CFD from an existing mesh, at a fixed angle of attack or trimmed to a target lift coefficient.
- `run-aero-optimization`: run single-point or multipoint aerodynamic shape optimization for the aircraft.

## Standard Inputs

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#aircraftGenerateCfdMeshInputs">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="aircraftGenerateCfdMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `custom_vsp3` (int, default: 0): set to 1 to mesh a user-supplied `aircraft.vsp3` in the working directory; leave it 0 to use the packaged default aircraft.
- `n_cpu_cores` (int, default: 2): number of CPU cores (MPI ranks) used for the parallel snappyHexMesh passes. Must be at least 2.
- `surface_level` (int, default: 6): surface mesh refinement level that controls mesh size: level 5 gives about 0.25M cells, and each additional level increases the cell count by about 2.5x.
- `n_boundary_layers` (int, default: 5): number of prism layers used during the layered snappyHexMesh pass.
- `altitude` (float, default: None): optional standard-atmosphere altitude in meters (0 to 20000), inherited by aircraft CFD and optimization cases.
- `local_refine_box` (list[list[float]], default: None): optional two-corner local refinement box `[[x0, y0, z0], [x1, y1, z1]]`. Leave unset for no local refinement.

Aircraft geometry inputs are not fixed. Before meshing, the agent writes `vsp_design_vars.json` with only the geometry changes requested in the prompt, and each selected OpenVSP parameter becomes an extra float input named `Component:Group:Variable` (for example `Wing:XSec_2:Sweep` or `Wing:UpperCoeff_1:Au_0`), with its default read from the baseline `aircraft.vsp3`. For a wing component, the supported changes are airfoil shape (CST coefficients), section twist, span, sweep, dihedral, section tip chord, wing root chord, streamwise position, vertical position, and pitch angle. For a horizontal tail, the supported changes are twist, streamwise position, vertical position, and pitch angle. The packaged aircraft has `Wing` and `Tail` components; for a custom `aircraft.vsp3`, the agent uses its actual component names.

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

- `angle_of_attack` (float, default: 2.0): freestream angle of attack (AoA) in degrees.
- `fixed_lift_trim` (int, default: 0): set to 1 to vary angle of attack and the Tail pitch angle until the prescribed `lift_constraint` and zero pitching moment are reached; leave at 0 for a fixed-AoA simulation.
- `lift_constraint` (float, default: 0.5): target lift coefficient used when `fixed_lift_trim` is 1.
- `mach_number` (float, default: 0.3): freestream Mach number.
- `reynolds_number` (float, default: 1e6): freestream Reynolds number when altitude is null; altitude overrides it using the aircraft reference length.
- `altitude` (float, default: inherited from generate-cfd-mesh): optional standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds is calculated from Mach and aircraft reference length.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

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

- `angle_of_attack` (float, default: 2.0): initial freestream angle of attack (AoA) in degrees.
- `mach_number` (float, default: 0.3): freestream Mach number.
- `reynolds_number` (float, default: 1e6): freestream Reynolds number when altitude is null; altitude overrides it using the aircraft reference length.
- `altitude` (float, default: inherited from generate-cfd-mesh): optional standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds is calculated from Mach and aircraft reference length.
- `optimizer` (str, default: "Uno"): optimization algorithm to use. Options are Uno (default), SLSQP, SNOPT, and EGO. The number of CST coefficients per airfoil surface is set by the advanced parameter `profile_fit_coeff_count` (default 6).
- `lift_constraint` (list[float], default: [0.5]): target lift coefficient lower bound for each optimization point. Supply more than one entry for multipoint optimization; its length must equal `multipoint_weight`.
- `multipoint_weight` (list[float], default: [1.0]): objective weight for each optimization point. Provide one entry per `lift_constraint` value; weights must sum to 1.0.
- `moment_constraint` (int, default: 0): enable the zero pitching-moment equality constraint with 1, trimmed with the Tail pitch angle (select Tail `pitch_angle` in generate-cfd-mesh); use 0 to disable it.
- `stability_constraint` (float, default: -1.0): lower bound on the static stability margin (0.05 means 5%). Set to a negative value to disable it.
- `le_radius_constraint` (float, default: 0.7): lower bound on leading-edge radius constraint; normalized wrt the baseline radius (1.0). Set to a negative value to disable it.
- `thickness_constraint` (float, default: 0.5): lower bound on airfoil thickness constraint; normalized wrt the baseline thickness (1.0). Set to a negative value to disable it.
- `camber_curvature_constraint` (int, default: 0): camber-line smoothness constraint that prevents wavy optimized airfoil shapes. 1 to enable, 0 to disable (default).
- `volume_constraint` (float, default: 1.0): lower bound on the Wing component volume constraint; normalized wrt the baseline volume (1.0). Set to a negative value to disable it.
- `area_constraint` (float, default: -1.0): upper bound on the Wing component planform area constraint; normalized wrt the baseline area (1.0). Set to a negative value to disable it.
- `same_profile_constraint` (int, default: 0): set to 1 to keep the airfoil profile (CST coefficients) of every section of each component identical via linear equality constraints; applies only when CST coefficients are selected design variables. Use 0 to disable it.
- `max_opt_iters` (int, default: 50): maximum number of optimization iterations.
- `n_ego_doe_pts` (int, default: 20): number of initial design of experiment (DOE) sample points used by the EGO optimizer.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

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

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `pressure_profile_fractions` (list[float], default: [0.2, 0.5, 0.9]): fractions of the projected Wing semi-span used for pressure-profile plots.
- `max_cell_size` (float, default: null): target farfield blockMesh cell size used to size the outer box. If null, the skill uses the mean wing chord.
- `line_level` (int, default: null): snappyHexMesh feature-edge refinement level. If null, the skill uses `surface_level + 1`.
- `curvature_level` (int, default: null): snappyHexMesh curvature refinement level. If null, the skill uses `surface_level + 2`. Use `-1` to disable curvature refinement.
- `n_layer_outer_iter` (int, default: 3): number of outer iterations used in `addLayersControls` for snappyHexMesh.
- `max_nonorthogonality_thresholds` (list[float], default: [70.0, 80.0]): [Pass, Warning] thresholds for maximum non-orthogonality.
- `max_aspect_ratio_thresholds` (list[float], default: [1000.0, 10000.0]): [Pass, Warning] thresholds for maximum aspect ratio.
- `max_skewness_thresholds` (list[float], default: [4.0, 6.0]): [Pass, Warning] thresholds for maximum skewness.

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

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `plot_tail_fraction` (float, default: 1.0): fraction of the CD/CL/CM history to plot from the end. 1.0 plots the full history; 0.2 plots the final 20 percent.
- `max_flow_iters` (int, default: 10000): maximum number of flow iterations written to the case controlDict endTime/writeInterval settings.
- `pressure_profile_fractions` (list[float], default: [0.2, 0.5, 0.9]): fractions of the projected Wing semi-span used for pressure-profile plots.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `initialize_from` (str, default: null): warm-start source case name. When set, the field staged into 0/ is kept instead of resetting to the uniform freestream.
- `force_std_thresholds` (list[float], default: [0.0001, 0.05]): [Pass, Warning] thresholds for raw force-coefficient standard deviation.
- `residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum residual drop in log10 orders.

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

- `camera_scale` (float, default: 1.0): camera zoom multiplier for the 3D mesh and flow-field plots. Values below 1.0 zoom in, values above 1.0 zoom out; 1.0 is the default framing.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `max_flow_iters` (int, default: 10000): maximum number of flow iterations written to the case controlDict endTime/writeInterval settings.
- `pressure_profile_fractions` (list[float], default: [0.2, 0.5, 0.9]): fractions of the projected Wing semi-span used for pressure-profile plots.
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
- `dv_bounds` (dict[str, list[float]], default: {"CSTCoeffs": [-0.4, 0.4], "Twist": [-10.0, 10.0], "Sweep": [-20.0, 20.0], "Dihedral": [0.0, 10.0], "Pitch": [-10.0, 10.0], "AoA": [0.0, 10.0], "Span": [0.5, 1.5], "Chord": [0.5, 1.5], "Wing_Root_Chord": [1.0, 1.0]}): design-variable lower/upper bounds shared by EGO and regular optimization. All keys are required. Span, Chord (section tip chords), and Wing_Root_Chord (root chord of the whole wing) are multipliers of the baseline value, e.g. [0.5, 1.5] is +-50%; all other keys are absolute values. Wing_Root_Chord defaults to be fixed with bounds [1.0, 1.0].
- `max_adj_iters` (int, default: 1000): maximum GMRES iterations used by the DAFoam adjoint linear solve.
- `pc_fill_level` (int, default: 1): ILU fill level used by the DAFoam adjoint preconditioner.
- `objective_reduction_pct_thresholds` (list[float], default: [5.0, 1.0]): [Pass, Warning] thresholds for objective reduction in percent.
- `final_feasibility_thresholds` (list[float], default: [0.0001, 0.01]): [Pass, Warning] thresholds for final feasibility.
- `flow_residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum flow residual drop in log10 orders.
- `adjoint_residual_drop_orders_thresholds` (list[float], default: [5.0, 3.0]): [Pass, Warning] thresholds for minimum adjoint residual drop in log10 orders.

</div>
</div>
</div>


## Agent Capability demos

### CFD Mesh Generation 

Users can prompt to generate an aircraft CFD mesh with the pre-defined model (wing+fuselage+tails). The default model is similar to Boeing 737 and users can prescribe the desired wing sectional shapes (through CST coefficients), chords, sweeps, twists, dihedral, span, and position, as well as the horizontal tail twist, position, and pitch angle. For example, 

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

Instead of using the default Boeing 737 configuration in `aircraft.vsp3`, you can use a customized OpenVSP aircraft configuration for the agent. First, download the Cessna 172 configuration file: [aircraft_c172.vsp3](https://github.com/DAFoam/mdo_agent_work/releases/download/files/aircraft_c172.vsp3). The Cessna 172 vsp3 file was downloaded and modified from the [OpenVSP Airshow](https://airshow.openvsp.org/). Rename it to `aircraft.vsp3` and place it in your `mdo_agent_work/results` folder (working directory).

Then, you can ask the agent to simulate your customized configuration. For example:

`Generate a CFD mesh for my customized aircraft.vsp3 geometry. The mesh should have about 0.5 million cells. Then, run a CFD simulation with aoa=2 deg, Ma=0.3, and Re=5e6. Next, run another CFD simulation with the same condition but increase the wing sweep by 20 deg. Compare the CD/CL between these two CFD simulations. For both mesh generation and CFD simulations, use 4 cores.`

Note: You do not need to provide a `vsp_design_vars.json` file. Before meshing, the agent writes this file in the working directory based on your prompt. It lists the OpenVSP component, group, and variable name for each geometry change you requested (for example, the sweep of each wing section), using the actual component names in your `aircraft.vsp3`.

The following are the AI-generated pictures. We can compare the CD/CL values between the original sweep design and the design with 20 deg increased sweep.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-orig.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-20d.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-orig-p.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-aircraft-custom-sweep-20d-p.png" style="width:400px !important;" />

Fig. 4. Example of using customized aircraft.vsp3. Left: original design. Right: +20 sweep design.

{% include links.html %}

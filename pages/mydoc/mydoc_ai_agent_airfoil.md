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

- `generate-cfd-mesh`: build the airfoil CFD mesh and mesh-quality outputs.
- `run-cfd-simulation`: run steady CFD from an existing mesh, at a fixed angle of attack or a prescribed lift coefficient.
- `run-cfd-simulation-unsteady`: run unsteady (time-dependent) CFD from an existing mesh.
- `run-aero-optimization`: run single-point or multipoint aerodynamic shape optimization, using gradient-based (Uno, SLSQP, SNOPT) or surrogate-based (EGO) optimizers.

## Standard Inputs

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilGenerateCfdMeshInputs">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="airfoilGenerateCfdMeshInputs" class="panel-collapse collapse">
<div class="panel-body">

- `airfoil_profile` (str, default: "naca0012"): airfoil profile name, such as naca0012 or rae2822.
- `mesh_cells` (int, default: 6000): target total mesh-cell count for the mesh.
- `y_plus` (float, default: 50.0): target near-wall mesh spacing (`y+` or `yPlus`).
- `mach_number` (float, default: 0.2): reference Mach number (Ma) for mesh generation.
- `reynolds_number` (float, default: 5e6): reference Reynolds number (Re) for mesh generation. Used when altitude is null; otherwise calculated from altitude and Mach.
- `altitude` (float, default: None): optional standard-atmosphere altitude in meters (0 to 20000). When set, Reynolds number is calculated automatically and overrides a supplied value.
- `local_refine_box` (list[list[float]], default: None): optional two-corner local refinement box `[[x0, y0, z0], [x1, y1, z1]]`. Leave unset for no local refinement.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilRunCfdSimulationInputs">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="airfoilRunCfdSimulationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 2.0): freestream angle of attack (AoA) in degrees.
- `fixed_lift_coeff` (float, default: -1.0): automatically vary the angle of attack to compute drag at the prescribed lift coefficient (fixed_lift_coeff). Set it to -1.0 to disable.
- `airfoil_profile` (str, default: inherited from generate-cfd-mesh): airfoil profile name inherited from generate-cfd-mesh.
- `mach_number` (float, default: inherited from generate-cfd-mesh): reference Mach number. Inherited from generate-cfd-mesh if not provided.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): reference Reynolds number inherited from the mesh unless altitude is set; altitude overrides it.
- `altitude` (float, default: inherited from generate-cfd-mesh): standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds is calculated from altitude and Mach.
- `y_plus` (float, default: inherited from generate-cfd-mesh): target near-wall y+ inherited from generate-cfd-mesh.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilRunCfdSimulationUnsteadyInputs">`run-cfd-simulation-unsteady` (click to expand)</a>
</div>
</div>
<div id="airfoilRunCfdSimulationUnsteadyInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 2.0): freestream angle of attack (AoA) in degrees.
- `airfoil_profile` (str, default: inherited from generate-cfd-mesh): airfoil profile name inherited from generate-cfd-mesh.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number. Inherited from generate-cfd-mesh if not provided.
- `n_flow_through` (float, default: 10.0): CFD endTime represented as the number of flow-through times for the airfoil.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): freestream Reynolds number inherited from the mesh unless altitude is set; altitude overrides it.
- `altitude` (float, default: inherited from generate-cfd-mesh): standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds is calculated from altitude and Mach.
- `y_plus` (float, default: inherited from generate-cfd-mesh): target near-wall y+ inherited from generate-cfd-mesh.
- `initialize_from` (str, default: None): warm-start-CFD source case name. When set, the initial field is copied from `initialize_from` folder into this case's `0` folder.
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilRunAeroOptimizationInputs">`run-aero-optimization` (click to expand)</a>
</div>
</div>
<div id="airfoilRunAeroOptimizationInputs" class="panel-collapse collapse">
<div class="panel-body">

- `angle_of_attack` (float, default: 2.0): initial freestream angle of attack (AoA) in degrees.
- `airfoil_profile` (str, default: inherited from generate-cfd-mesh): airfoil profile name inherited from generate-cfd-mesh.
- `mach_number` (float, default: inherited from generate-cfd-mesh): freestream Mach number. Inherited from generate-cfd-mesh if not provided.
- `reynolds_number` (float, default: inherited from generate-cfd-mesh): freestream Reynolds number inherited from the mesh unless altitude is set; altitude overrides it.
- `altitude` (float, default: inherited from generate-cfd-mesh): standard-atmosphere altitude in meters inherited from the mesh; when set, Reynolds is calculated from altitude and Mach.
- `y_plus` (float, default: inherited from generate-cfd-mesh): target near-wall y+ inherited from generate-cfd-mesh.
- `optimizer` (str, default: "Uno"): optimization algorithm to use. Options are Uno (default), SLSQP, SNOPT, and EGO. The number of CST coefficients per airfoil surface is set by the advanced parameter `profile_fit_coeff_count` (default 6).
- `lift_constraint` (list[float], default: [0.5]): target lower-bound lift coefficient constraint. Supply more than one entry for multipoint optimization. len(lift_constraint) must equal len(multipoint_weight).
- `multipoint_weight` (list[float], default: [1.0]): weight array for multipoint optimization; weights must sum to 1.0. len(lift_constraint) must equal len(multipoint_weight). For example, lift targets [0.5, 0.4] use weights [0.6, 0.4].
- `max_opt_iters` (int, default: 20): maximum number of optimization iterations.
- `n_ego_doe_pts` (int, default: 20): number of initial design of experiment (DOE) sample points used by the EGO optimizer.
- `thickness_constraint` (float, default: 0.5): lower bound on airfoil thickness constraint; normalized wrt the baseline thickness (1.0). Set to a negative value to disable it.
- `le_radius_constraint` (float, default: 0.7): lower bound on leading-edge radius constraint; normalized wrt the baseline radius (1.0). Set to a negative value to disable it.
- `volume_constraint` (float, default: 1.0): lower bound on airfoil volume constraint; normalized wrt the baseline volume (1.0). Set to a negative value to disable it.
- `camber_curvature_constraint` (int, default: 0): camber-line smoothness constraint that prevents wavy optimized airfoil shapes. 1 to enable, 0 to disable (default).
- `n_cpu_cores` (int, default: 1): number of CPU cores (MPI ranks) to use.

</div>
</div>
</div>

## Advanced Parameters

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilGenerateCfdMeshAdvanced">`generate-cfd-mesh` (click to expand)</a>
</div>
</div>
<div id="airfoilGenerateCfdMeshAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `blunt_te` (float, default: 0.01): trailing-edge round percentage expressed as an x/chord trim location. The default 0.01 means the trim starts at x = 0.01 from the trailing edge.
- `d0` (float, default: -1.0): first-layer height in meters. Use a negative value to let the wrapper estimate it from `y_plus`, `mach_number`, and `reynolds_number`.
- `diffusion_sweeps` (int, default: 20): number of smoothing sweeps per layer for diffusion extrusion.
- `neighbor_rings` (int, default: 5): neighbor-ring depth used by the diffusion extrusion smoother.
- `diffuse_start` (float, default: 0.002): smoothing onset distance in meters. Diffusion stays off until this marched distance, then starts ramping up.
- `max_nonorthogonality_thresholds` (list[float], default: [70.0, 80.0]): [Pass, Warning] thresholds for maximum non-orthogonality.
- `max_aspect_ratio_thresholds` (list[float], default: [1000.0, 10000.0]): [Pass, Warning] thresholds for maximum aspect ratio.
- `max_skewness_thresholds` (list[float], default: [4.0, 6.0]): [Pass, Warning] thresholds for maximum skewness.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilRunCfdSimulationAdvanced">`run-cfd-simulation` (click to expand)</a>
</div>
</div>
<div id="airfoilRunCfdSimulationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `plot_tail_fraction` (float, default: 1.0): fraction of the CD/CL/CM history to plot from the end. 1.0 plots the full history; 0.2 plots the final 20 percent.
- `cst_coeffs` (list[float], default: null): user-supplied CST coefficients, ordered as `[upper..., lower...]`. len(cst_coeffs) must be 2*profile_fit_coeff_count. Set this only to parameterize the airfoil with explicit numeric values (e.g., to reproduce an optimized shape from its CST coefficients); leave it null (default) to use the named profile in `airfoil_profile`.
- `max_flow_iters` (int, default: 10000): maximum number of flow iterations written to the case controlDict endTime/writeInterval settings.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `use_wall_functions` (str, default: "auto"): wall-function selection. Use `auto` to choose from mesh settings, `1` to force enable, or `0` to force disable. In auto mode, explicit positive `d0` disables wall functions; otherwise y_plus >= 5 enables them.
- `force_std_thresholds` (list[float], default: [0.0001, 0.05]): [Pass, Warning] thresholds for raw force-coefficient standard deviation.
- `residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum residual drop in log10 orders.
- `initialize_from` (str, default: null): warm-start lever (off by default). Case name of a previously converged CFD run whose flow field initializes this run instead of a uniform freestream; leave unset (null) for a cold start. Use it to help a hard case converge (high AoA, or a fine low-y+ mesh). The referenced case must have finished before this run.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilRunCfdSimulationUnsteadyAdvanced">`run-cfd-simulation-unsteady` (click to expand)</a>
</div>
</div>
<div id="airfoilRunCfdSimulationUnsteadyAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `plot_tail_fraction` (float, default: 1.0): fraction of the CD/CL/CM history to plot from the end. 1.0 plots the full history; 0.2 plots the final 20 percent.
- `cst_coeffs` (list[float], default: null): user-supplied CST coefficients, ordered as `[upper..., lower...]`. len(cst_coeffs) must be 2*profile_fit_coeff_count. Set this only to parameterize the airfoil with explicit numeric values (e.g., to reproduce an optimized shape from its CST coefficients); leave it null (default) to use the named profile in `airfoil_profile`.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `use_wall_functions` (str, default: "auto"): wall-function selection. Use `auto` to choose from mesh settings, `1` to force enable, or `0` to force disable. In auto mode, explicit positive `d0` disables wall functions; otherwise y_plus >= 5 enables them.
- `max_cfl` (float, default: 1.0): maximum CFL number for auto time stepping in URANS runs; written to controlDict maxCo.
- `n_saves` (int, default: 5): number of saved fields per flow-through time for URANS runs; writeInterval is set to rounded endTime divided by this value.
- `force_slope_thresholds` (list[float], default: [1e-5, 0.001]): [Pass, Warning] thresholds for the absolute raw force-coefficient tail slope used by unsteady convergence review.

</div>
</div>
</div>

<div class="panel panel-default">
<div class="panel-heading">
<div class="panel-title">
<a data-toggle="collapse" href="#airfoilRunAeroOptimizationAdvanced">`run-aero-optimization` (click to expand)</a>
</div>
</div>
<div id="airfoilRunAeroOptimizationAdvanced" class="panel-collapse collapse">
<div class="panel-body">

- `adjoint_residual_drop_orders_thresholds` (list[float], default: [5.0, 3.0]): [Pass, Warning] thresholds for minimum adjoint residual drop in log10 orders.
- `cp_plot_bounds` (list[float], default: [-2.0, 2.0]): [Lower, upper] bounds of the Cp axis and colorbar shared by the pressure-profile and Cp flow-field plots.
- `cst_coeffs` (list[float], default: null): user-supplied CST coefficients, ordered as `[upper..., lower...]`. len(cst_coeffs) must be 2*profile_fit_coeff_count. Set this only to parameterize the airfoil with explicit numeric values (e.g., to reproduce an optimized shape from its CST coefficients); leave it null (default) to use the named profile in `airfoil_profile`.
- `final_feasibility_thresholds` (list[float], default: [0.0001, 0.01]): [Pass, Warning] thresholds for final feasibility.
- `flow_residual_drop_orders_thresholds` (list[float], default: [6.0, 3.0]): [Pass, Warning] thresholds for minimum flow residual drop in log10 orders.
- `max_adj_iters` (int, default: 1000): maximum GMRES iterations used by the DAFoam adjoint linear solve.
- `max_flow_iters` (int, default: 10000): maximum number of flow iterations written to the case controlDict endTime/writeInterval settings.
- `objective_reduction_pct_thresholds` (list[float], default: [5.0, 1.0]): [Pass, Warning] thresholds for objective reduction in percent.
- `pc_fill_level` (int, default: 1): ILU fill level used by the DAFoam adjoint preconditioner.
- `primal_func_slope_tol` (float, default: 1e-6): DAFoam primal function slope tolerance passed to script_run_dafoam.py.
- `primal_func_std_tol` (float, default: 0.04): DAFoam primal function standard deviation tolerance passed to script_run_dafoam.py.
- `profile_fit_coeff_count` (int, default: 6): number of coefficients used to fit each airfoil surface. For example, `4` fits 4 coefficients for the upper surface and 4 for the lower surface.
- `solver_name` (str, default: null): explicit solver override. Supported values are `DASimpleFoam` (incompressible), `DARhoSimpleFoam` (compressible), `DARhoSimpleCFoam` (compressible/transonic), and `DAHisaFoam` (compressible/transonic/supersonic). Leave unset, `null`, or `none` to use the default Mach-based selection.
- `transonic_mach_boundary` (float, default: 0.4): transonic Mach split used by the default solver selection when `solver_name` is not set.
- `turbulence_model` (str, default: "SpalartAllmaras"): OpenFOAM RANS turbulence model. Supported values are `SpalartAllmaras` (SA) and `kOmegaSST` (SST).
- `u_plot_bounds` (list[float], default: [-1.0, 1.0]): [Lower, upper] bounds of the normalized velocity colorbar for the U flow-field plot.
- `use_wall_functions` (str, default: "auto"): wall-function selection. Use `auto` to choose from mesh settings, `1` to force enable, or `0` to force disable. In auto mode, explicit positive `d0` disables wall functions; otherwise y_plus >= 5 enables them.
- `n_multi_start` (int, default: 20): number of multi-start points for the EGO internal EI optimization.
- `ei_tol` (float, default: 0.0001): EGO internal expected improvement (EI) optimization tolerance.
- `ego_seed` (int, default: 0): random seed used by the EGO optimizer DOE and infill sampling.
- `ego_tol` (float, default: 0.001): objective variation tolerance for the EGO optimization.
- `ego_cstr_tol` (float, default: 0.001): constraint tolerance used by EGO and its lift-trim searches.
- `dv_bounds` (dict[str, list[float]], default: {"CSTCoeffs": [-0.5, 0.5], "AoA": [0.0, 10.0]}): design-variable lower/upper bounds shared by EGO and regular optimization. All keys are required.

</div>
</div>
</div>


## Agent Capability demos

### Mesh Generation 

Users can prompt to generate airfoil mesh with desired airfoil profiles, mesh densities, yPlus, and local refinement.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-coarse.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-trame.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-fine.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-local-refine.png" style="width:400px !important;" />

Fig. 1. Top left: Overview of a coarse mesh. Prompt: `Generate a cfd mesh for the naca0012 airfoil`. Top right: Trame interactive view of the TE mesh. Bottom left: Overview of a fine mesh with a different airfoil. Prompt: `Generate a cfd mesh for the rae2822 airfoil with 50K cells, yPlus 3, and ref Mach=0.7`. Bottom right: Locally refined mesh. Prompt: `Locally refine the above mesh between -0.1 to 1.1 chords from LE, z length of the refinment is 0.5 chords`.

### CFD Simulation 

Users can prompt to run airfoil CFD simulations with desired airfoil profiles (prescribed in the mesh generation skill), angles of attack, Mach numbers, and Reynolds numbers. For example, 

`Generate a cfd mesh for the naca0012 airfoil and run a cfd simulation at Ma=0.3, Re=5e6, and aoa=3 degs. Use 2 CPU cores`. 

Or a supersonic flow case 

`Generate a cfd mesh for rae2822 airfoil with 100K cells, yPlus 5, Re 2e7 and Ma 1.5. Run a cfd with aoa=1 deg use 4 cores.`. 

The following are the agent-generated figures.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-pressure-profile.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-trame-nut.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-supersonic-p.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-supersonic-U.png" style="width:400px !important;" />

Fig. 2. Top left: Airfoil pressure profile. Top right: Visualization of airfoil turbulence variable field in the trame interactive server. Bottom left and right: pressure and velocity contours of the supersonic csaae.

### CFD Unsteady Simulation 

Users can prompt to run airfoil CFD simulations with desired airfoil profiles (prescribed in the mesh generation skill), angles of attack, Mach numbers, and Reynolds numbers. For example, 

`Generate a cfd mesh for naca0012 airfoil with 20K cells, Re 5e6 and Ma 0.3. Run a unsteady cfd simulation with aoa=20 deg use 4 cores.`. 

The following are the agent-generated figures.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-unsteady-pressure-profile.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-unsteady-velocity.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-unsteady-cl.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cfd-unsteady-cd.png" style="width:400px !important;" />

Fig. x. Top left: Airfoil pressure profile. Top right: Visualization of airfoil velocity field in the trame interactive server. Bottom left and right: lift coefficient convergence history and drag coefficient convergence history.

### CFD Mesh Convergence Study

Users can prompt to conduct a mesh convergence study for an airfoil. For example, 

`Conduct a cfd mesh convergence study for the RAE2822 airfoil at Ma=0.75, Re=1e7, and aoa=2 degs. The mesh sizes are 10K, 20K, 50K, and 100K. The yPlus is 3. Use 24 cores. CFD maxIter=5000`. 

The following is the agent-generated figure, one needs to add a follow up prompt to plot this pressure profile comparisoin figure, such as 

`Plot the pressure profile for all cases in one figure to show the difference.` 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-mesh-conv.png" style="width:400px !important;" />

Fig. 3. Pressure profile comparison between different mesh densities.

### CD/CL vs AoA

Users can prompt to simulation CD/CL sweep for various angle of attacks. For example, 

`Generate a cfd mesh for the naca0012 airfoil with 50K cells and yPlus 3. Then, run a sweep of CFD at Ma=0.3 and Re=5e6, and aoa = 2 to 18 degs with 2 deg interval. Use 24 cores. After the simulation is finished, plot cl/cd vs aoa and drop diverged cases.`. 

The following is the agent-generated figure. This case ran on the HPC and you may need to follow up to ask the agent to analyze the result once the job is finished on compute nodes.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cd-aoa.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-cl-aoa.png" style="width:400px !important;" />

Fig. 4. CD/CL vs AoA plots

### Aerodyanamic shape optimization

Users can prompt to run aerodynamic shape optimization. The default objective is drag, the design variables are airfoil shape and angle of attack, the constraints include lift, thickness, volume, and leading edge radius. For example, 

`Generate a cfd mesh for the naca0012 airfoil and run an aero optimization at ma 0.3, re 5e6, cl 0.5. Run the optimization for 20 iters. Use 2 cores`. 

The following is the agent-generated figure. The drag reduction and constraints can be found in the chat window after the optimization is finished. After the optimization is finished, the user can also ask agent to verify the drag reduction generated by the coarse-mesh optimization with a fine mesh. For example 

`The optimization uses a coarse mesh. Verify the optimization drag reduction at CL 0.5 using a fine mesh with 50K cells and yPlus 3. Run two fine mesh CFDs for the baseline and optimized designs and compare with the coarse mesh results.` 

The agent will compare the drag reduciton between coarse and fine mesh for the baseline and optimized designs.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-opt-shape.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-opt-trame.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-opt-cd-hst.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-opt-fine-mesh.png" style="width:400px !important;" />

Fig. 5. Aerodynamic optimization. Top Left: comparison of the pressure and shape between the baseline and optimized designs. Top Right: Visualizing of the pressure for optimized design in trame. Bot left: Optimization convergence history for CD. Bot right: Summary of fine mesh verification.

### Surrogate-based aerodyanamic shape optimization

Users can additionally choose the surrogate-based EGO optimizer rather than a gradient-based one (set through the `optimizer` input of `run-aero-optimization`). Similar to the gradient-based approach, the design variables include the shape of the airfoil and the angle of attack subject to the same lift, thickness, volume, and leading edge radius constraints. For example,

`Run a surrogate based optimization on the NACA0012 airfoil. Set Re to 6.6e5, use 4000 mesh cells, with a velocity of 10m/s velocity. For the lift constraint use 0.5 and set the AOA to 5. Use 80 DOE points for the optimization and set the bounds on the CST coefficient design variables to [-0.5, 0.5]. Use 10 optimization iterations. Use 22 cores for the CFD.`

The following is the agent generated figure. The drag reduction and constraint values are returned to the user by the agent in the chat window.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-SBO-shape.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-SBO-pressure-opt-trame.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-SBO-velocity-opt-trame.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-SBO-pressure-baseline-trame.png" style="width:400px !important;" />

Fig. 6. Surrogate-based aerodynamic shape optimization. Top Left: comparison of the pressure and shape between the baseline and optimized designs. Top Right: Visualizing of the pressure for optimized design in trame. Bot left: Visualizing of the velocity profile for optimized design in trame. Bot right: Visualizing of the pressure for baseline design in trame.

### Aerodynamic multipoint optimization

Users can prompt to run a multipoint optimization by giving one lift constraint and one weight per flight condition (`lift_constraint` and `multipoint_weight` in `run-aero-optimization`). The default objective is the weighted drag, the design variables are airfoil shape and the angle of attack of each flight condition, the constraints include lift for each scenario, thickness, volume, and leading edge radius. For example,

`Generate a multipoint optimization at ma 0.02941, Re 6.67e5, cl [0.5, 0.4], aoa [5 deg, 4 deg], and weights [0.6, 0.4]. Use 4 cores.`

The following is the agent-generated figure. Similar to the aerodynamic shape optimization, the drag reduction and constraints can be found in the chat window after the optimization finishes. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-multipoint-mesh.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-multipoint-pressure-profile.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-multipoint-flowfield-baseline.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-multipoint-flowfield-optimized.png" style="width:400px !important;" />

Fig. 7. Aerodynamic multipoint optimization. Top Left: mesh profile generation. Top Right: comparison of the pressure and shape between the baseline and optimzied designs. Bot Left: baseline flow field plot generated in Paraview. Bot Right: optimized flow field plot generated in Paraview. 

### Generate training samples

Users can prompt to run multiple CFD simulations to generate samples for training machine learning models. For example, 

`Generate training sample points for NACA0012 airfoil for AOA=1 to 5 degs, and Ma from 0.15 to 0.4. Generate 10 samples.`. 

The following is the agent-generated figure.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-lhs-summary.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-airfoil-lhs-folder.png" style="width:400px !important;" />

Fig. 8. Left: summary of the CD/CL for all generated samples. Right: Screenshot of the folder structure that contains all the flow fields for each training sample

{% include links.html %}








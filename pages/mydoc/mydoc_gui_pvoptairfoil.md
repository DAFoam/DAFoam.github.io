---
title: Airfoil aerodynamic optimization plugin pvOptAirfoil
keywords: gui, airfoil
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_pvoptairfoil.html
folder: mydoc
---

PvOptAirfoil is the first in a series of graphical user interface (GUI) plugins that we are developing to streamline the DaFoam optimization process. PvOptAirfoil is designed to make airfoil aerodynamic shape optimization setup more visual throughout the entire process. It can be used for mesh generation and transformation via the DaFOAM Docker image, run-script setup for local optimization using Docker or later exporting to HPC, as well as visualizing optimization results. This GUI is currently in the beta version.

## PvOptAirfoil

![pvOptAirfoil](/images/tutorials/GUI_paraviewFull.png)

For a setup and installation guide refer to [this page](mydoc_gui_overview.html)
<br><br>

### Load The Plugin

Set the environmental variables by running the shell script loadOptGUI.sh, located in the pvOptGUI package

<pre>
. $HOME/pvOptGUI/loadOptGUI.sh
</pre>
<br>

Now run the associated version of Paraview

<pre>
./$ParaView_DIR/bin/paraview
</pre>
<br>

To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click 
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.so and load the shared image
<br>

The plugin acts as a filter, so open a paraview.foam file from the file explorer at the top left of the interface to begin.
- This is an empty dummy file, so create one if you do not have one already
<br>

Then click the green apply button on the left, below the Paraview pipeline window

Finally, load the plugin from the "Filters" menu in the upper toolbar
<br>

A message box should appear indicating whether a working Docker version was successfully found on your system, click *OK*

You should now see the pvOptAirfoil interface in the panel on the left, below the pipeline

pvOptAirfoil writes several files for mesh generation, run script creation, optimization and post-processing results. Select the output folder by clicking the *Select Optimization Folder* button and select the preferred directory.

**NOTE:** We recommend selecting the same folder containing the .foam dummy file, this allows the Paraview pipeline to access written data for user processing
<br><br>

### Generate The Mesh

**NOTE:** This step requires Docker, if Docker is not found when loading the plugin, the generation files will be created without generating the mesh

![MeshGeneration](/images/tutorials/GUI_meshGen.png)

First, confirm the optimization folder is selected, then choose the upper and lower profiles for your airfoil by clicking the *Select Upper Surface Profile* and *Select Lower Surface Profile* buttons and selecting the files from the dialog

Next you can set the approximate number of mesh cells, the boundary layer thickness and the number of cells between the surface and the far field

Experienced users may choose to select the *Toggle Advanced Mesh Settings* to refine their mesh further, in which case the total mesh cells is calculated from these inputs

Finally, select the *Generate Mesh* button to start mesh generation, a few seconds later a message box should appear indicating success or failure and the airfoil's calculated chord length

**NOTE:** To load a generated mesh to the viewing area in Paraview, navigate to your paraview.foam file in the pipeline, and click refresh and apply in the menu below (you may need to scroll)
<br><br>

### Write the Run Script

![Runscript](/images/tutorials/GUI_runscript.png)

To write the run-script, a number of paramaters need to be set

First, select the solver from the dropdown list of supported solvers
- DASimpleFOAM is recommended for mach number below 0.1, incompressible steady-state flow solver for Navier-Stokes equations
- DARhoSimpleFOAM is recommended for mach numbers between 0.1 and 0.6, compressible steady-state flow solver for Navier-Stokes equations (subsonic)
- DARhoSimpleCFOAM is recommended for mach numbers between 0.6 and 1.0, compressible steady-state flow solver for Navier-Stokes equations (transonic)
<br>

Select the optimizer from the dropdown list
- ipopt is the default and is recommended

	**NOTE:** Optimizing with SNOPT requires a license and is not supported for local optimization, more info [here](https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/optimizers/SNOPT.html)
<br>

Input the mach number
- You will recieve a warning if the input mach number does not match the solver
<br>

Input the Reynolds number, a message box will appear asking if you would like to scale the mesh or viscosity, after selection the message box re-appears with the new scaled value

**NOTE:** Scaling geometry is disabled without Docker and viscosity is scaled automatically
<br>

Far Field Pressure
- Not required for DASimpleFOAM solver
<br>

Normalization Density
- Not required for DASimpleFOAM solver
<br>
Temperature
- Not required for DASimpleFOAM solver
<br>

Dynamic Viscosity
- Input disabled, this value is scaled by Reynolds number
<br>

Angle of Attack
- Input disabled, this is an initial condition for the CL Solution, true angle of attack is calculated before optimization by default
<br>

Select the preferred turbulence model from the dropdown list
- Spalart Allmaras
- K-Omega SST
- K-Epsilon
<br>

Experienced users may want to change the turbulence variables. To edit, select the *Toggle Advanced Turbulence Settings* button
- Eddy Viscosity Ratio
- Turbulent Intensity

**NOTE:** Some of these variables are not required and are disabled for certain turbulence models
<br>

Set target lift coefficient
- This value is used to solve for the angle of attack during the first segment of the optimization
<br>

Set number of free form deformation (FFD) points
- These points are distributed outside the airfoil surface and deformed for shape optimization
<br>

Set maximum optimization (adjoint) iterations
- The optimization will end if converged before maximum iterations reached
<br>

Set maximum (minor) flow iterations
- This limits the number of iterations within each major flow iteration, the individual major iteration will also end if flow converges before maximum iterations reached
<br>

Experienced users may wish to change a number of advanced settings in the run-script, to edit the following select the *Toggle Advanced Runscript Settings* button
- Flow convergence tolerance
- Adjoint convergence tolerance
- Feasibility tolerance
- Optimality tolerance
- Minimum relative thickness
- Maximum relative thickness
- Minimum relative volume
- Maximum relative volume
- The user can also input custom DaOptions, refer to [this page](https://dafoam.github.io/doxygen/html/classdafoam_1_1pyDAFoam_1_1DAOPTION.html) for a full list of custom options

**NOTE:** Preset values in this section are typically sufficient for airfoil optimizations
<br>

Finally, you can now click the *Generate Runscript* button to create the rest of the files required for optimization including the DaFOAM runscript.py, these are created in the optimization folder

**NOTE:** If values are changed after generating the run-script, simply click the button again to regenerate the files

![Write](/images/tutorials/GUI_write.png)

A message box should appear where one can see the full runscript in a small editing window by clicking the *Show Details* button, accept by clicking *OK* or run the optimization locally with one core (this requires Docker)
<br><br>

### Optimize

After clicking the *Write Runscript* button at the bottom of the GUI, one should see a message box as described previously. Clicking optimize will run the optimization locally with one core
- If you wish to abort the optimization open the terminal that is currently running paraview (and the optimization) and enter 

<pre><b>
ctrl+\
</b></pre>
<br>

Optimization results are output to the file logOpt.txt in your earlier selected optimization folder

A few seconds after starting the optimization, a python GUI will appear showing the optimization results in real time, we recommend making this window full screen
<br><br>

### Python Graphical User Interface

![pyGUI](/images/tutorials/GUI_pyGUI_post.png)

The python script for the post-processing GUI is written to the optimization folder as soon as the folder is selected, this GUI can view optimization results in real time

The python GUI is launched when the optimization starts, but the user can also load the GUI by clicking the *View Optimization Data* button, located at the bottom of the Paraview interface next to the *Write Runscript* button. Clicking the *View Optimization Data* button will automatically load the python GUI with prior data if there is an output logOpt.txt file in the optimization folder.

To select a different log file you can click the *Open File* button on the right hand side of the python GUI

The dropdown box labeled *Case History* allows one to select the case segment that is being viewed, there are currently two implemented choices that may be contained in your log file
- CL Solution, angle of attack is solved for the target coefficient of lift
- Optimization, selected objective function is optimized
<br>

After selecting the portion of the case you wish to view, one can select an adjoint or flow major iteration number

For every adjoint iteration in the optimization there can be several flow iterations
- Loading a flow iteration will load the corresponding adjoint iteration
- Loading an adjoint iteration will load the *last* corresponding flow iteration

The python GUI also implements the standard Matplotlib toolbar to manipulate plots and export data

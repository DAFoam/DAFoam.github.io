---
title: Airfoil aerodynamic optimization using a GUI
keywords: gui, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_overview.html
folder: mydoc
---

## Overview

To facilitate the DAFoam optimization, we developed a suite of Paraview-based Graphical User Interface (GUI) plugins called pvOptGUI. You can use the plugins to generate mesh, setup and run optimization, and visualize the optimization progress in Paraview. You can also use the plugins to generate the optimization configuration files, e.g., runScript.py, and then run it on an HPC. This GUI is currently in the beta version and has only one plugin (pvOptAirfoil) for airfoil aerodynamic optimization. 

The installation guide for Windows 10/11 is as follows. Linux and MacOS are no longer supported. The pvOptGUI package is essential and Docker is optional.

### pvOptGUI

**Windows 10/11 (64bit)**

Download the [pvOptGUI_Windows10_64bit package](https://github.com/DAFoam/files/releases/download/pvOptGUI/pvOptGUI_Windows10_64bit.zip) and extract it to a desired location
- You may need [7Zip](https://www.7-zip.org/) or other similar software
- To avoid file duplication warnings, move the compressed folder to the desired location and *extract here* to decompress the file.

To load ParaView, open the shortcut *paraview.exe* located in the bin folder of your installation

To load one of the sources contained in the pvOptGUI plugin, click the source tab at the top of the toolbar, then select one of the choices listed in the *PvOptGUI* tab.

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.

###Docker (optional)

Docker is not required to generate the DAFoam run script. However, Docker is needed if you want to do mesh generation, transformation, and running the aerodynamic optimization through the GUI. 

**Windows 10/11**

Download [Docker Desktop](https://docs.docker.com/docker-for-windows/install/) for Windows

After installation, run Docker Desktop. Wait for the notification that says Docker is running.

In your Windows hidden icons on the bottom right of your taskbar, one should see the Docker icon. Right click and open the *Dashboard*
Verify that you are signed in to your Docker account at the top right of the dashboard. You can close the dashboard but keep Docker running.

Open the command prompt and verify docker installation by running:

<pre>
docker -v
</pre>

The major version should be a minimum of 19 to run pvOptGUI docker commands with pvOptAirfoil. Once the Docker is installed and verified, run this command from the terminal to download the DAFoam image:

<pre>
docker pull dafoam/opt-packages:v2.2.7
</pre>

**NOTE:** Docker must be running and *you must be signed in to your Docker account* when launching Paraview to run Docker commands through pvOptGUI plugins. The user can log in at any point while running the plugins

## Mesh Generation


pvOptUMesh is the second graphical user interface (GUI) plugin in the pvOptGUI suite. pvOptUMesh streamlines the process of generating structured meshes from tri-surface mesh (.STL) files using SnappyHexMesh, which can then be used for optimization. This GUI is currently in the beta version.

### Load the case and plugin

First, install and open ParaView following the instructions mentioned on [this page](mydoc_gui_overview.html).

Next, open the pvOptUMesh source, located by opening the *sources* tab of the toolbar then hovering over *pvOptGUI*.

Then open a paraview.foam dummy file in the file select option of this source. A zipped tutorial folder containing an example of this dummy file can be downloaded [here](https://github.com/DAFoam/pvOptGUI_tutorials/archive/refs/heads/main.zip).

Then click the green apply button on the left, below the ParaView pipeline window. You can also set up the 'auto-apply' feature by navigating to *edit* in the upper toolbar, then selecting *settings*. Auto-apply is the second setting under the general tab.


You should now see the pvOptUMesh interface in the panel on the left, below the pipeline, as shown in the following figure.

![pvOptUMesh](/images/tutorials/GUI_pvOptUMesh_full.PNG)

A message box should appear indicating whether a working Docker version was successfully found on your system, click *OK*.

---

### Generate the mesh

**NOTE:** This step requires Docker. If Docker is not found when loading the plugin, the generation files will be created without actually generating the mesh.

First, confirm the output folder is selected. Then click the *Select Tri-Surface Mesh Files* button to select the .STL files. A file dialog should now appear, select all .STL files that you would like to generate the mesh for. **The stl files should be in meters.**


After importing the stl files, the bounds for the background mesh block should be filled in with the minimum values to contain your tri-surface mesh files.
These values can be increased, but you may get a warning if you try and decrease the size from minimum.

After setting the background mesh bounds, the bounding box can be visualized around the .STL assembly by clicking *Visualize Background Mesh*.

![pvOptUMesh_backgroundVisualization](/images/tutorials/GUI_pvOptUMesh_backgroundVisualization.PNG)


Now, prescribe the boundary type for each face of the background mesh block
- The options are patch, wall, and symmetry plane


Input the total number of cells in the background mesh
- If the input value does not allow for an aspect ratio of 1, the value will be modified
- If no nearby values are acceptable you may be asked to change the bounds of the background mesh


Input the line level
- Must be an integer
- If advanced setting are enabled, the line level can be set for each .STL file individually


Surface Level
- If advanced settings are enabled, the surface level can be set for each .STL file individually


Prism Level
- Must be an integer


A few other parameters can be adjusted by enabling advanced settings:


The Mesh Location
- Default is to generate an external mesh, but an internal mesh can also be generated


Cells Between Levels
- Number of cells generated between each prism level
- Default is 3


Final Layer Thickness
- Thickness of the final mesh layer at the tri-surface mesh boundary
- Default is 0.5


Max Non-Orthogonality Angle
- Default is 60 degrees


Max Skewness
- Default is 4


Finally, select the *Generate Mesh* button to start mesh generation. After completion, a message box should appear indicating success or failure.

**NOTE:** To load a generated mesh to the viewing area in ParaView, navigate to your paraview.foam file in the pipeline, and click refresh and apply in the menu below (you may need to scroll)

## Airfoil Aerodynamic Optimization

pvOptAirfoil is the first in a series of graphical user interface (GUI) plugins that we are developing to streamline the DaFoam optimization process. PvOptAirfoil is designed to make airfoil aerodynamic shape optimization setup more visual throughout the entire process. It can be used for mesh generation and transformation via the DaFOAM Docker image, run-script setup for local optimization using Docker or later exporting to HPC, as well as visualizing optimization results. This GUI is currently in the beta version.

### Load the case and plugin

To run a GUI-based optimization case, first download the [pvOptGUI tutorial](https://github.com/DAFoam/pvOptGUI_tutorials/archive/refs/heads/main.zip) and extract it.

Then, open ParaView following the instructions mentioned on [this page](mydoc_gui_overview.html). 

Then open the pvOptAirfoil source by first clicking the sources tab in the toolbar at the top of the screen. Then hover over pvOptGUI and select pvOptAirfoil. Open a paraview.foam dummy file inside the new source's file select option, an example of this file is found in pvOptGUI_tutorials.

Then click the green apply button on the left, below the ParaView pipeline window. You can also set up the 'auto-apply' feature by navigating to *edit* in the upper toolbar, then selecting settings. Auto-apply is the second setting under the *general* tab.

A message box should appear indicating whether a working Docker version was successfully found on your system, click *OK*

You should now see the pvOptAirfoil interface in the panel on the left, below the pipeline, as shown in the following figure.

![pvOptAirfoil](/images/tutorials/GUI_pvOptAirfoil_full.png) 

---

### Generate the mesh

**NOTE:** This step requires Docker, if Docker is not found when loading the plugin, the generation files will be created without generating the mesh

![MeshGeneration](/images/tutorials/GUI_pvOptAirfoil_meshGen.png)

First, confirm the optimization folder is selected, then choose the upper and lower profiles for your airfoil by clicking the *Select Upper Surface Profile* and *Select Lower Surface Profile* buttons and selecting the files from the dialog. An example of the upper and lower surface profiles can be found pvOptGUI_tutorials/NACA0012/profiles

Next you can set the approximate number of mesh cells, the boundary layer thickness and the number of cells between the surface and the far field

Experienced users may choose to select the *Toggle Advanced Mesh Settings* to refine their mesh further, in which case the total mesh cells is calculated from these inputs

Finally, select the *Generate Mesh* button to start mesh generation, a few seconds later a message box should appear indicating success or failure and the airfoil's calculated chord length

**NOTE:** To load a generated mesh to the viewing area in ParaView, navigate to your paraview.foam file in the pipeline, and click refresh and apply in the menu below (you may need to scroll)  

---

### Write the run script

![Runscript](/images/tutorials/GUI_pvOptAirfoil_runScript.png)

To write the run-script, a number of parameters need to be set

First, select the solver from the dropdown list of supported solvers
- DASimpleFOAM is recommended for mach number below 0.1, incompressible steady-state flow solver for Navier-Stokes equations
- DARhoSimpleFOAM is recommended for mach numbers between 0.1 and 0.6, compressible steady-state flow solver for Navier-Stokes equations (subsonic)
- DARhoSimpleCFOAM is recommended for mach numbers between 0.6 and 1.0, compressible steady-state flow solver for Navier-Stokes equations (transonic)  


Select the optimizer from the dropdown list
- ipopt is the default and is recommended

	**NOTE:** Optimizing with SNOPT requires a license and is not supported for local optimization, more info [here](https://mdolab-pyoptsparse.readthedocs-hosted.com/en/latest/optimizers/SNOPT.html)  


Input the mach number
- You will receive a warning if the input mach number does not match the solver  


Input the Reynolds number, a message box will appear asking if you would like to scale the mesh or viscosity, after selection the message box re-appears with the new scaled value

**NOTE:** Scaling geometry is disabled without Docker and viscosity is scaled automatically  


Far Field Pressure
- Not required for DASimpleFOAM solver  


Normalization Density
- Not required for DASimpleFOAM solver  


Temperature
- Not required for DASimpleFOAM solver  


Dynamic Viscosity
- Input disabled, this value is scaled by Reynolds number  


Angle of Attack
- Input disabled during optimization setup only, this is an initial condition for the CL Solution, true angle of attack is calculated before optimization by default.
- This option is enabled for flow solution 


Select the preferred turbulence model from the dropdown list
- Spalart Allmaras
- K-Omega SST
- K-Epsilon  


Experienced users may want to change the turbulence variables. To edit, select the *Toggle Advanced Turbulence Settings* button
- Eddy Viscosity Ratio
- Turbulent Intensity

**NOTE:** Some of these variables are not required and are disabled for certain turbulence models  


Set target lift coefficient
- This value is used to solve for the angle of attack during the first segment of the optimization  


Set number of free form deformation (FFD) points
- These points are distributed outside the airfoil surface and deformed for shape optimization  


Set maximum optimization (adjoint) iterations
- The optimization will end if converged before maximum iterations reached  


Set maximum (minor) flow iterations
- This limits the number of iterations within each major flow iteration, the individual major iteration will also end if flow converges before maximum iterations reached  


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


Finally, you can now click the *Generate Runscript* button to create the rest of the files required for optimization including the DaFOAM runscript.py, these are created in the optimization folder

**NOTE:** If values are changed after generating the run-script, simply click the button again to regenerate the files

![Write](/images/tutorials/GUI_pvOptAirfoil_write.png)

A message box should appear where one can see the full runscript in a small editing window by clicking the *Show Details* button, accept by clicking *OK* or run the optimization locally with one core (this requires Docker)  

---

### Optimize

After clicking the *Write Runscript* button at the bottom of the GUI, one should see a message box as described previously. Clicking optimize will run the optimization locally with one core
- If you wish to abort the optimization open the terminal that is currently running paraview (and the optimization) and enter 

<pre>
ctrl+\
</pre>  


Optimization results are output to the file logOpt.txt in your earlier selected optimization folder

A few seconds after starting the optimization, a python GUI will appear showing the optimization results in real time, we recommend making this window full screen  

---

### Python GUI for post-processing

![pyGUI](/images/tutorials/GUI_pyGUI_post.png)

The python script for the post-processing GUI is written to the optimization folder as soon as the folder is selected, this GUI can view optimization results in real time

The python GUI is launched when the optimization starts, but the user can also load the GUI by clicking the *View Optimization Data* button, located at the bottom of the ParaView interface next to the *Write Runscript* button. Clicking the *View Optimization Data* button will automatically load the python GUI with prior data if there is an output logOpt.txt file in the optimization folder. If an optimization is running and the gui has been closed, you can resume viewing optimization results by clicking the *View Optimization Data* button.

To select a different log file you can click the *Open File* button on the right hand side of the python GUI

The dropdown box labeled *Case History* allows one to select the case segment that is being viewed, there are currently two implemented choices that may be contained in your log file
- CL Solution, angle of attack is solved for the target coefficient of lift
- Optimization, selected objective function is optimized  


After selecting the portion of the case you wish to view, one can select an adjoint or flow major iteration number

For every adjoint iteration in the optimization there can be several flow iterations
- Loading a flow iteration will load the corresponding adjoint iteration
- Loading an adjoint iteration will load the *last* corresponding flow iteration

The python GUI also implements the standard Matplotlib toolbar to manipulate plots and export data

Full Docker installation guide is located [here](https://docs.docker.com/engine/install/ubuntu/)


PvOptPostProcessing and PvOptView are Paraview based graphical user interfaces included in the PvOptGUI plugin to aid users in post processing their data. PvOptPostProcessing can be used to view the iterations from a DAFoam log file, while PvOptView can be used to view results from any .hst file. PvOptView provides a ParaView interface to open OptView, a post-processing utlity from [pyOptSparse](https://github.com/mdolab/pyoptsparse). These GUI's are currently in the beta version.

---

To post process data, first open ParaView with PvOptGUI following the instructions mentioned on [this page](mydoc_gui_overview.html).

### PvOptPostProcessing

Open the PvOptPostProcessing source by first clicking the sources tab in the toolbar at the top of the screen. Then hover over PvOptGUI and select PvOptPostProcessing.

Once the source is loaded, simply click *select log file* and choose the DAFoam log file you wish to post process.

Finally, click the *Post Process* button to open the GUI

![pvOptPostProcessing](/images/tutorials/GUI_pyGUI_post.png)

### PvOptView

One can open the PvOptView source by first clicking the sources tab in the toolbar at the top of the screen. Then hover over PvOptGUI and select PvOptView.

Once the source is loaded, simply click *select history file* and choose the .hst file you wish to post process.

Finally, click the *Post Process* button to open the GUI

![pvOptView](/images/tutorials/GUI_optView.png)

[OptView](https://github.com/mdolab/pyoptsparse/blob/main/pyoptsparse/postprocessing/OptView.py) is an open-source post-processing utlity from pyOptSparse



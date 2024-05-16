---
title: Overview
keywords: gui, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_overview.html
folder: mydoc
---

To facilitate the DAFoam optimization, we developed a suite of Paraview-based Graphical User Interface (GUI) plugins called pvOptGUI. You can use the plugins to generate mesh, setup and run optimization, and visualize the optimization progress in Paraview. You can also use the plugins to generate the optimization configuration files, e.g., runScript.py, and then run it on an HPC. This GUI is currently in the beta version and has only one plugin (pvOptAirfoil) for airfoil aerodynamic optimization. 

The installation guide for Windows 10/11 is as follows. Linux and MacOS are no longer supported. The pvOptGUI package is essential and Docker is optional.

## pvOptGUI

### Windows 10/11 (64bit)

Download the [pvOptGUI_Windows10_64bit package](https://github.com/DAFoam/files/releases/download/pvOptGUI/pvOptGUI_Windows10_64bit.zip) and extract it to a desired location
- You may need [7Zip](https://www.7-zip.org/) or other similar software
- To avoid file duplication warnings, move the compressed folder to the desired location and *extract here* to decompress the file.

To load ParaView, open the shortcut *paraview.exe* located in the bin folder of your installation

To load one of the sources contained in the pvOptGUI plugin, click the source tab at the top of the toolbar, then select one of the choices listed in the *PvOptGUI* tab.

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.

## Docker (optional)

Docker is not required to generate the DAFoam run script. However, Docker is needed if you want to do mesh generation, transformation, and running the aerodynamic optimization through the GUI. 

### Windows 10/11

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

Full Docker installation guide is located [here](https://docs.docker.com/engine/install/ubuntu/)



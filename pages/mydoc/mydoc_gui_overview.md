---
title: Overview
keywords: gui, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_overview.html
folder: mydoc
---

To facilitate the DAFoam optimization, we developed a suite of Paraview-based Graphical User Interface (GUI) plugins called pvOptGUI. You can use the plugins to generate mesh, setup and run optimization, and visualize the optimization progress in Paraview. You can also use the plugins to generate the optimization configuration files, e.g., runScript.py, and then run it on an HPC. This GUI is currently in the beta version and has only one plugin (pvOptAirfoil) for airfoil aerodynamic optimization.

## Installation

### pvOptGUI

#### Ubuntu 18.04/20.04

First, download the pre-compiled pvOptGUI package for your version of Ubuntu: [pvOptGUI_Ubuntu](https://github.com/DAFoam/files/releases/tag/pvOptGUI) and the airfoil aerodynamic optimization plugin [pvOptAirfoil_Ubuntu_latest.so](https://github.com/DAFoam/files/releases/tag/pvOptGUI)

Then run the following command in the terminal to extract the pvOptGUI package to your home directory, change 1804 to the installed Ubuntu version.

<pre>
tar -xvf pvOptGUI_Ubuntu1804.tar.gz $HOME/pvOptGUI
</pre>

*Every time* before running, the environmental variables for Miniconda3 and Paraview-v5.8.1 need to be set. Confirm the pvOptGui package was decompressed in your home directory. Simply run the shell script loadOptGUI in your terminal with the command below to set the required environmental variables:

<pre>
. $HOME/pvOptGUI/loadOptGUI.sh
</pre>

**NOTE:** If a different location is preferred or the directories are renamed, edit the file paths in loadOptGUI.sh, then execute the shell script.

Finally, open Paraview by running:

<pre>
./$ParaView_DIR/bin/paraview
</pre>

pvOptGUI supports multiple GUI plugins, the current version supports only airfoil aerodynamic optimization, i.e., pvOptAirfoil.

To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click 
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.so and load the shared image

The plugin acts as a filter, so open a paraview.foam file from the file explorer at the top left of the Paraview interface to begin. Then click the green apply button on the left, below the Paraview pipeline window. Finally, load the plugin from the "Filters" menu in the upper toolbar.

You should now see the pvOptAirfoil interface in the panel on the left, below the pipeline

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.

#### Windows 10 (64bit)

First download the pre-compiled pvOptGUI packages: [pvOptGUI_Windows10_64bit/Paraview-v5.8.1_Windows10_64bit](https://github.com/DAFoam/files/releases/tag/pvOptGUI) and the airfoil aerodynamic optimization plugin [pvOptAirfoil_Windows10_64bit_latest.dll](https://github.com/DAFoam/files/releases/tag/pvOptGUI)
You may need [7Zip](https://www.7-zip.org/) or other similar software to extract pvOptGUI, WinZip encounters long file path errors.
**Note:** You may recieve a warning along the lines of "File is not commonly downloaded and may be dangerous." Continue the download by selecting *keep* file.

Extract the pvOptGui package to your Desktop

Execute the batch file loadOptGUI.bat in the extracted folder by double clicking the file, a console window should appear with the Miniconda *base* environment loaded

In the console window, launch Paraview by executing the command:

<pre>
%ParaView_DIR%\bin\Debug\paraview.exe
</pre>

pvOptGUI supports multiple GUI plugins, the current version supports only airfoil aerodynamic optimization, i.e., pvOptAirfoil.

To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click 
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.dll and load the shared library

The plugin acts as a filter, so open a paraview.foam file from the file explorer at the top left of the Paraview interface to begin. Then click the green apply button on the left, below the Paraview pipeline window. Finally, load the plugin from the "Filters" menu in the upper toolbar.

You should now see the pvOptAirfoil interface in the panel on the left, below the pipeline

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.


### Docker (optional)

Docker is not required to generate the DAFoam run script. However, Docker is needed if you want to do mesh generation, transformation, and running the aerodynamic optimization through the GUI. 
	
#### Ubuntu	

To install Docker, open your terminal, copy and run the following command. This will uninstall any previous docker versions and install the latest version:

<pre>
sudo apt-get remove docker docker-engine docker.io containerd runc && sudo apt-get update && sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent   software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https:// download. docker.com/linux/ubuntu $(lsb_release -cs) stable" && sudo apt-get update && sudo apt-get install docker docker.io -y
</pre>

Next, add your user name to the docker group:

<pre>
sudo usermod -aG docker $USER
</pre>

Log out and log back in to your user account for the command to take effect. Then, verify docker installation by running:

<pre>
docker -v
</pre>

The major version should be a minimum of 19 to run pvOptGUI docker commands with pvOptAirfoil. Once the Docker is installed and verified, run this command from the terminal to download the DAFoam image:

<pre>
docker pull dafoam/opt-packages:v2.2.7
</pre>

If the docker image is not pulled, it will be pulled automatically when the first docker command is attempted.

Full Docker installation guide is located [here](https://docs.docker.com/engine/install/ubuntu/)

#### Windows 10

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


---
title: Overview
keywords: gui, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_overview.html
folder: mydoc
---

To facilitate the pre-processing, running, and post-processing DAFoam optimization, we developed a Paraview-based Graphical User Interface (GUI) plugin called pvOptGUI. This GUI is currently in the beta version and supports only airfoil aerodynamic optimization on Ubuntu systems.

## Installation

### pvOptGUI

First download the pre-compiled pvOptGUI: [pvOptGUI_Ubuntu1804](https://github.com/DAFoam/files/releases/tag/pvOptGUI) and the plugin [pvOptGUI_Ubuntu1804_latest.so](https://github.com/DAFoam/files/releases/tag/pvOptGUI)

Then run the following command in the terminal to extract the pvOptGUI package to your home directory

<pre>
tar -xvf pvOptGUI_Ubuntu1804.tar.gz $HOME/pvOptGUI
</pre>

Before running, the environmental variables for Miniconda3 and Paraview-v5.8.1 need to be set. Confirm the pvOptGui package was decompressed in your home directory. Simply run the shell script loadOptGUI in your terminal with the command below to set the required environmental variables:

<pre>
. $HOME/pvOptGUI/loadOptGUI.sh
</pre>

**NOTE:** If a different location is preferred edit the file paths in loadOptGUI.sh, then execute the shell script

Finally, open Paraview by running:

<pre>
./$ParaView_DIR/bin/paraview
</pre>

pvOptGUI supports multiple GUI plugin, the current version supports only airfoil aerodynamic optimization, i.e., pvOptAirfoil.

To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click 
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.so and load the shared image


The plugin acts as a filter, so open a paraview.foam file from the file explorer at the top right of the interface to begin. Then click the green apply button on the left, below the Paraview pipeline window. Finally, load the plugin from the "Filters" menu in the upper toolbar.

You should now see the pvOptAirfoil menu in the panel on the left, underneath the pipeline

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.


### Docker (optional)

Docker is not required to generate the DAFoam run script. However, Docker is needed if you want to do mesh generation, transformation, and running the aerodynamic optimization through the GUI. 
	
To install Docker, open your terminal, copy and run the following command. This will uninstall any previous docker versions and install the latest version:

<pre>
sudo apt-get remove docker docker-engine docker.io containerd runc && sudo apt-get update && sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent   software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https:// download. docker.com/linux/ubuntu $(lsb_release -cs) stable" && sudo apt-get update && sudo apt-get install docker docker.io -y
</pre>

Next, add your user name to the docker group:

<pre>
sudo usermod -aG docker $USER
</pre>

Logout and log back in to your account for the command to take effect. Then, verify docker installation by running:

<pre>
docker --version
</pre>

The major version should be a minimum of 19 to run pvOptGUI docker commands. Once the Docker is installed and verified, run this command from the terminal to download the DAFoam image:

<pre>
docker pull dafoam/opt-packages:v2.2.6
</pre>

If the docker image is not pulled, it will be pulled automatically when docker commands are attempted.

Full Docker installation guide is [here](https://docs.docker.com/engine/install/ubuntu/)


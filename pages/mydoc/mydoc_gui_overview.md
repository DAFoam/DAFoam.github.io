---
title: Overview
keywords: gui, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_overview.html
folder: mydoc
---

# pvOptAirfoil Installation

### Installing Docker

Docker is used for mesh generation, transformation, and running the aerodynamic optimization. 
- Docker is not required to generate the DaFOAM run script.
	
Open your terminal, copy and run the following command. This will uninstall any previous docker versions and install the latest version:

	sudo apt-get remove docker docker-engine docker.io containerd runc && sudo apt-get update && sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent   software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https:// download. docker.com/linux/ubuntu $(lsb_release -cs) stable" && sudo apt-get update && sudo apt-get install docker docker.io -y

Next, add your user name to the docker group:

	sudo usermod -aG docker $USER


- Logout and log back in to your account for the command to take effect.
	
Then, verify docker installation by running:

	docker --version

- The major version should be a minimum of 19 to run pvOptAirfoil docker commands.

Once the Docker is installed and verified, run this command from the terminal to download the DAFoam image:

	docker pull dafoam/opt-packages:v2.2.5

- If the docker image is not pulled, it will be pulled automatically when docker commands are attempted.

Full Docker installation guide is	[here](https://docs.docker.com/engine/install/ubuntu/)



#
### Installing and Running pvOptAirfoil

First install the prerequisites: [pvOptGUI_Ubuntu1804](https://github.com/DAFoam/files/releases/tag/pvOptGUI) and [pvOptGUI_Ubuntu1804_latest.so](https://github.com/DAFoam/files/releases/tag/pvOptGUI)

Go to installation location then run the following command in the terminal to extract the pvOptGUI package to your home directory

	tar -xvf pvOptGUI_Ubuntu1804.tar.gz $HOME/pvOptGUI

#

Before running, the environmental variables for Miniconda3 and Paraview-v5.8.1 need to be set 
	
Confirm the pvOptGui package was decompressed in your home directory

Simply run the shell script loadOptGUI in your terminal with the command below to set the required environmental variables:

	. $HOME/pvOptGUI/loadOptGUI.sh
- If a different location is preferred edit the file paths in loadOptGUI.sh, then execute the shell script

Finally, open Paraview by running:

	/.$ParaView_DIR/bin/paraview

To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.so and load the shared image


The plugin acts as a filter, so open a paraview.foam file from the file explorer at the top right of the interface to begin
Then click the green apply button on the left, below the Paraview pipeline window
Finally, load the plugin from the "Filters" menu in the upper toolbar.
- You should now see the pvOptAirfoil menu in the panel on the left, underneath the pipeline

---
title: Overview
keywords: gui, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_overview.html
folder: mydoc
---

To facilitate the DAFoam optimization, we developed a suite of Paraview-based Graphical User Interface (GUI) plugins called pvOptGUI. You can use the plugins to generate mesh, setup and run optimization, and visualize the optimization progress in Paraview. You can also use the plugins to generate the optimization configuration files, e.g., runScript.py, and then run it on an HPC. This GUI is currently in the beta version and has only one plugin (pvOptAirfoil) for airfoil aerodynamic optimization. 

The installation guide for Windows, MacOS, and Linux is as follows. The pvOptGUI package is essential and Docker is optional.

## pvOptGUI

### Windows 10 (64bit)

First download the [pvOptGUI_Windows10_64bit package](https://github.com/DAFoam/files/releases/download/pvOptGUI/pvOptGUI_Windows10_64bit.zip) and extract it to a desired location
- You may need [7Zip](https://www.7-zip.org/) or other similar software
- To avoid file duplication warnings, move the compressed folder to the desired location and *extract here* to decompress the file.

Then download the official release of [ParaView 5.9.1](https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.9&type=binary&os=Windows&downloadFile=ParaView-5.9.1-Windows-Python3.8-msvc2017-64bit.zip)
- Extract the zip file inside the previously downloaded pvOptGUI folder.

Download the [Miniconda 3](https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Windows-x86_64.exe) installer. Run the installer, select all default options during the process.
- When asked where you want to install miniconda3, select *browse* and *make a new folder* titled miniconda3 inside the pvOptGUI folder you previously downloaded.
- After the Miniconda3 installation completes, open the pvOptGUI folder containing the new miniconda3 directory and double click minicondaSetup.bat to install the required packages.
- After the script finishes, a list of packages should appear in the console. Verify matplotlib version is 3.4.2, numpy is 1.20.2, and tk is 8.6.10; afterward you may close the console.

Finally download the airfoil aerodynamic optimization plugin [pvOptAirfoil_Windows10_64bit_latest.zip](https://github.com/DAFoam/files/releases/download/pvOptGUI/pvOptAirfoil_Windows10_64bit_latest.zip) and extract it
- pvOptGUI supports multiple GUI plugins, the current version supports only airfoil aerodynamic optimization, i.e., pvOptAirfoil.


To load Paraview, execute the batch file loadOptGUI.bat in your pvOptGUI folder by double clicking the file. A console window should appear briefly, then ParaView should open a few seconds later.

**NOTE:** You may need to adjust file paths if you renamed/relocated the Miniconda3 or Paraview folders


To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click 
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.dll in the file dialog and load the shared library

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.

### MacOS 10.15 and above

First, download the [ParaView-5.9.1.dmg](https://github.com/DAFoam/files/releases/download/pvOptGUI/ParaView-5.9.1-OSX10.15-Python3.8-64bit.dmg) installer. Double click to install. When asked, drag ParaView-5.9.1.app to your "/Applications" folder.

Then, download [pvOptGUI_MacOS_10.15.zip](https://github.com/DAFoam/files/releases/download/pvOptGUI/pvOptGUI_MacOS_10.15.zip) and [Miniconda3-py38_4.10.3-MacOSX-x86_64.sh](https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-MacOSX-x86_64.sh). Put these two files in your $HOME directory.

Now, open a terminal, copy the following block of commands and paste it to the terminal and hit enter:

<pre>
cd $HOME && \
unzip pvOptGUI_MacOS_10.15.zip && \
cd pvOptGUI_MacOS_10.15 && \
chmod 755 $HOME/Miniconda3-py38_4.10.3-MacOSX-x86_64.sh && \
$HOME/Miniconda3-py38_4.10.3-MacOSX-x86_64.sh -b -p $HOME/pvOptGUI_MacOS_10.15/miniconda3 && \
export PATH=$HOME/pvOptGUI_MacOS_10.15/miniconda3/bin:$PATH && \
export LD_LIBRARY_PATH=$HOME/pvOptGUI_MacOS_10.15/miniconda3/lib:$LD_LIBRARY_PATH && \
export PYTHONUSERBASE=no-local-libs && \
pip install --upgrade pip && \
pip install numpy==1.20.2 && \
pip install matplotlib==3.4.2 && \
conda install tk==8.6.10 && \
conda list
</pre>

The pvOptGUI installation will be automatically done. After the commands finish, a list of packages should appear in the console. Verify matplotlib version is 3.4.2, numpy is 1.20.2, and tk is 8.6.10.

To open ParaView, run `source ./loadOptGUI.sh` on a terminal from the pvOptGUI_MacOS_10.15 folder. Running this script is necessary because it will setup related environmental variables for optimization.

Finally, we need to activate the pvOptAirfoil plugin in Paraview, locate the toolbar at the top of ParaView, then click 
- Tools>>Manage Plugins...
- Then navigate to the bottom of the pop-up window, select "pvOptAirfoil", and then click "Load Selected".
- You may also want to check the "auto-load" such that you don't have to manually activate the pvOptAirfoil plugin again 

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.


### Linux

First, download [pvOptGUI_Linux](https://github.com/DAFoam/files/releases/tag/pvOptGUI/pvOptGUI_Linux.tar.gz) and the airfoil aerodynamic optimization plugin [pvOptAirfoil_Linux_Latest.tar.gz](https://github.com/DAFoam/files/releases/tag/pvOptGUI/pvOptAirfoil_Linux_Latest.tar.gz)

Decompress both files to a convenient location. Then install the official release of [Paraview v5.9.0](https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.9&type=binary&os=Linux&downloadFile=ParaView-5.9.0-MPI-Linux-Python3.8-64bit.tar.gz) and untar it inside of the pvOptGUI folder you previously extracted.

Also download [Miniconda](https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh), run the .sh file using the default settings. When prompted for the install location, create a directory titled *miniconda3* inside the pvOptGUI folder. 

After Miniconda has been installed, traverse to the pvOptGUI directory and run *minicondaSetup.sh* using the below command to obtain the required packages. When prompted for installation permissions, enter yes.

<pre>
./minicondaSetup.sh
</pre>

**NOTE:** If a different location is preferred or the directories are renamed, editing file paths in the script may be necessary.

Finally, open Paraview by traversing to the pvOptGUI directory and running:

<pre>
./loadOptGUI.sh
</pre>

A console window should appear briefly, then ParaView should open a few seconds later.

**NOTE:** You may need to adjust file paths if you renamed/relocated the Miniconda3 or Paraview folders

To load pvOptAirfoil into Paraview, locate the toolbar at the top of the screen, then click 
- Tools>>Manage Plugins...>>load new...>>
- Then navigate to your copy of pvOptAirfoil.so and load the shared image

Refer to [this page](mydoc_gui_pvoptairfoil.html) for detailed instructions on how to use the pvOptAirfoil plugin.

## Docker (optional)

Docker is not required to generate the DAFoam run script. However, Docker is needed if you want to do mesh generation, transformation, and running the aerodynamic optimization through the GUI. 
	
### Ubuntu	

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

### Windows 10

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

### MacOS

Download [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-mac) for MacOS

Follow the same installation steps as Windows 10.


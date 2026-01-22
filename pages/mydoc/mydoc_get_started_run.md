---
title: Run optimization
keywords: run, tutorial, optimization
summary: "We first run preProcessing.sh for pre-processing and then run runScript.py for optimization."
sidebar: mydoc_sidebar
permalink: get-started-run.html
folder: mydoc
---

The following is an aerodynamic shape optimization case for the NACA0012 airfoil at low speed:

<pre>
Case: Airfoil aerodynamic optimization 
Geometry: NACA0012
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.5
Design variables: 20 free-form deformation (FFD) points moving in the y direction, one angle of attack
Constraints: Symmetry, volume, thickness, and lift constraints (total number: 34)
Mach number: 0.02941 (10 m/s)
Reynolds number: 0.6667 million
Mesh cells: ~4,000
Solver: DASimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/NACA0012_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the NACA0012 airfoil

|

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar/extract it. Open a **Terminal** (Linux/MacOS) or **Command Prompt** (Windows) and go to a tutorial folder. For example, if you download and extract the tutorial files to the Downloads folder and want to run the NACA0012 airfoil case with incompressible flow conditions, use this command:

<pre>
cd Downloads/tutorials-main/NACA0012_Airfoil/incompressible
</pre>

Once you are in a tutorial case folder, use the following command to start the pre-compiled DAFoam Docker container (a light-weight virtual machine).

<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Win10</button>
<button class="tab-button">Win11</button>
<button class="tab-button">MacOS/Linux</button>
</div>
<div class="tab-content">
<pre><code>docker run -it --rm -u dafoamuser --mount "type=bind,src=%cd%,target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash</code></pre>
</div>
<div class="tab-content">
<pre><code>docker run -it --rm -u dafoamuser --mount "type=bind,src=.,target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash</code></pre>
</div>
<div class="tab-content">
<pre><code>docker run -it --rm -u dafoamuser --mount "type=bind,src=$(pwd),target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash</code></pre>
</div>
</div>

The above command will start a Docker container, mount the **current directory** on your local OS (tutorials-main/NACA0012_Airfoil/incompressible) to the container's **mount** directory, log in to the container's mount directory as dafoamuser, and set the relevant DAFoam environmental variables. You may see something like this on your terminal: `dafoamuser@00fb6ceac4da:~/mount$`. 

**Now you are on the DAFoam Docker container**, run the preProcessing.sh script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The optimization progress will be printed to the screen and also written to logOpt.txt (we will elaborate on logOpt.txt later on [this page](get-started-runscript.html)). This case ran for 18 optimization iterations and took about 15 minutes with an Intel 3.0 GHz CPU.

A few notes:

- For MacOS and Windows, make sure you open the Docker Desktop app before running Docker commands.

- Treat the Docker container as disposable, i.e., start one container for one optimization run. If the optimization is running and you want to kill it, press `ctr+c` or `ctr+\`. After the optimization is done, type `exit` to exit the Docker container and free up the occupied memory.

- Before re-running a case, run `./Allclean.sh` to clean up the previous optimization results.

- dafoamuser has the sudo privilege and its password is: dafoamuser.

Check [this page](get-started-post-processing.html) for interpreting and post processing the optimization results.

{% include links.html %}

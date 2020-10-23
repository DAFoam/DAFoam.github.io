---
title: Command to start the DAFoam Docker image on Windows
keywords: run, tutorial, windows
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_get_started_start_docker_windows.html
folder: mydoc
---

First, verify if the Docker Desktop app is open and if it says "Docker Desktop is running". Then, open the **Prompt Command** terminal and go to a tutorial folder. For example, if you download and extract the tutorial files to the Downloads folder and want to run the NACA0012 airfoil case with incompressible flow conditions, use this command:

<pre>
cd Downloads/tutorials-master/NACA0012_Airfoil/incompressible
</pre>

Now run the following command in the terminal and check the output to make sure you are in the right directory:

<pre>
cd
</pre>

Once you are in a tutorial folder, use the following command to start the DAFoam Docker image.

<pre>
docker run -it --rm -u dafoamuser --mount "type=bind,src=%cd%,target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:{{ site.latest_version }} bash
</pre>

{% include links.html %}

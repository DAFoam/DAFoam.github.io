---
title: Build a new Docker image
keywords: dafoam, installation, docker
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_docker.html
folder: mydoc
---

The following is an example of how to update the DAFoam repo in Docker and save it as a new Docker image. First, create a file called **Dockerfile**, copy and paste the following commands into Dockerfile, and run `docker build -t my_new_dafoam_image_name .`. Here "dafoam/opt-packages:latest" can be any existing Docker image. 

<pre>
FROM dafoam/opt-packages:latest

# Swith to dafoamuser
USER dafoamuser

# compile
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    git clone https://github.com/mdolab/dafoam && \
    cd dafoam && \
    export export COMPILE_DAFOAM_ADF=1 && \
    ./Allmake
</pre>

{% include links.html %}

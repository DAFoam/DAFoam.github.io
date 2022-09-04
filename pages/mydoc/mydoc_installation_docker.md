---
title: Build a new Docker image
keywords: dafoam, installation, docker
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_docker.html
folder: mydoc
---

The following is an example of how to update the DAFoam repo in Docker and save it as a new Docker image. First, create a file called **Dockerfile**, copy and paste the following commands into Dockerfile, and run `docker build -t my_new_dafoam_image .`. Here "dafoam/opt-packages:latest" can be any existing Docker image. 

<pre>
FROM dafoam/opt-packages:latest

# Swith to dafoamuser
USER dafoamuser

# Here we need to load all the variables defined in loadDAFoam.sh
# DAFoam root path
ENV DAFOAM_ROOT_PATH=$HOME/dafoam
# OpenFOAM-v1812
ENV LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH
# Miniconda3
ENV PATH=$DAFOAM_ROOT_PATH/packages/miniconda3/bin:$PATH
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAFOAM_ROOT_PATH/packages/miniconda3/lib
# OpenMPI
ENV MPI_INSTALL_DIR=$DAFOAM_ROOT_PATH/packages/openmpi-3.1.6/opt-gfortran
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
ENV PATH=$MPI_INSTALL_DIR/bin:$PATH
# Petsc
ENV PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.14.6
ENV PETSC_ARCH=real-opt
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib
ENV PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib
# CGNS
ENV CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-4.1.2/opt-gfortran
ENV PATH=$PATH:$CGNS_HOME/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib
# Ipopt
ENV IPOPT_DIR=$DAFOAM_ROOT_PATH/packages/Ipopt
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$IPOPT_DIR/lib

# create a new repo directory
RUN mkdir -p $DAFOAM_ROOT_PATH/repos

# Update the DAFoam repo to the latest, we need to compile both original
# and AD version of DAFoam libs
RUN cd $DAFOAM_ROOT_PATH/repos && \
    git clone https://github.com/mdolab/dafoam && \
    cd dafoam && \
    . $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
    ./Allmake && \
    . $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADR/etc/bashrc && \
    ./Allclean && \
    ./Allmake && \
    . $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADF/etc/bashrc && \
    ./Allclean && \
    ./Allmake && \
    pip install .

RUN rm -rf $DAFOAM_ROOT_PATH/repos
</pre>

{% include links.html %}

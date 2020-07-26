---
title: Build Docker image
keywords: dafoam, installation, docker
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_docker.html
folder: mydoc
---

Create a file called **Dockerfile**, copy and paste the following commands into the Dockerfile and run `docker build -t my_dafoam_image .`

Refer to the [docker](https://github.com/dafoam/docker) repo. Here `dafoam/prerequisites:latest` is a docker image that contains prerequisites such as OpenFOAM, Petsc, OpenMPI, etc.

<pre>
FROM dafoam/prerequisites:latest

# Swith to dafoamuser
USER dafoamuser

ENV HOME=/home/dafoamuser

# f2py
ENV PATH=$PATH:$HOME/.local/bin
# OpenMPI-1.10.7
ENV MPI_INSTALL_DIR=$HOME/packages/openmpi-1.10.7/opt-gfortran
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
ENV PATH=$MPI_INSTALL_DIR/bin:$PATH
# Petsc-3.11.4
ENV PETSC_DIR=$HOME/packages/petsc-3.11.4
ENV PETSC_ARCH=real-opt
ENV PATH=$PETSC_DIR/$PETSC_ARCH/bin:$PATH
ENV PATH=$PETSC_DIR/$PETSC_ARCH/include:$PATH
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib
ENV PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib
# CGNS-3.3.0
ENV CGNS_HOME=$HOME/packages/CGNS-3.3.0/opt-gfortran
ENV PATH=$PATH:$CGNS_HOME/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

# MACH framework
RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/baseclasses && \
    cd baseclasses && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/pyspline && \
    cd pyspline && \
    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/pygeo && \
    cd pygeo && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/multipoint && \
    cd multipoint && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/pyhyp && \
    cd pyhyp && \
    cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/cgnsutilities && \
    cd cgnsutilities && \
    cp config.mk.info config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/idwarp && \
    cd idwarp && \
    cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/pyoptsparse && \
    cd pyoptsparse && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/adflow && \
    cd adflow && \
    cp -r config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/pyofm && \
    cd pyofm && \
    . $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    git clone https://github.com/mdolab/dafoam && \
    cd dafoam && \
    . $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
    ./Allmake && \
    pip install .

RUN cd $HOME && \
    rm -rf repos
</pre>

{% include links.html %}

---
title: Build Docker image
keywords: dafoam, installation, docker
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_docker.html
folder: mydoc
---

Create a file called **Dockerfile**, copy and paste the following commands into the Dockerfile and run `docker build -t my_dafoam_image .`

<pre>
FROM dafoam/prerequisites:v2.0

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
    wget https://github.com/mdolab/baseclasses/archive/v1.2.0.tar.gz -O baseclasses.tar.gz && \
    tar -xvf baseclasses.tar.gz && \
    cd baseclasses-1.2.0 && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/pyspline/archive/v1.2.0.tar.gz -O pyspline.tar.gz && \
    tar -xvf pyspline.tar.gz && \
    cd pyspline-1.2.0 && \
    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/pygeo/archive/v1.2.0.tar.gz -O pygeo.tar.gz && \
    tar -xvf pygeo.tar.gz && \
    cd pygeo-1.2.0 && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/multipoint/archive/v1.2.0.tar.gz -O multipoint.tar.gz && \
    tar -xvf multipoint.tar.gz && \
    cd multipoint-1.2.0 && \
    pip install .


RUN cd $HOME/repos && \
    wget https://github.com/mdolab/pyhyp/archive/v2.2.0.tar.gz -O pyhyp.tar.gz && \
    tar -xvf pyhyp.tar.gz && \
    cd pyhyp-2.2.0 && \
    cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/cgnsutilities/archive/v2.2.0.tar.gz -O cgnsutilities.tar.gz && \
    tar -xvf cgnsutilities.tar.gz && \
    cd cgnsutilities-2.2.0 && \
    cp config.mk.info config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/idwarp/archive/v2.2.0.tar.gz -O idwarp.tar.gz && \
    tar -xvf idwarp.tar.gz && \
    cd idwarp-2.2.0 && \
    cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/pyoptsparse/archive/v2.1.3.tar.gz -O pyoptsparse.tar.gz && \
    tar -xvf pyoptsparse.tar.gz && \
    cd pyoptsparse-2.1.3 && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/adflow/archive/v2.2.0.tar.gz -O adflow.tar.gz && \
    tar -xvf adflow.tar.gz && \
    cd adflow-2.2.0 && \
    cp -r config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/pyofm/archive/v1.2.0.tar.gz -O pyofm.tar.gz && \
    tar -xvf pyofm.tar.gz && \
    cd pyofm-1.2.0 && \
    . $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
    make && \
    pip install .

RUN cd $HOME/repos && \
    wget https://github.com/mdolab/dafoam/archive/v2.0.0.tar.gz -O dafoam.tar.gz && \
    tar -xvf dafoam.tar.gz && \
    cd dafoam-2.0.0 && \
    . $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
    ./Allmake && \
    pip install .

RUN cd $HOME && \
    rm -rf repos
</pre>

{% include links.html %}

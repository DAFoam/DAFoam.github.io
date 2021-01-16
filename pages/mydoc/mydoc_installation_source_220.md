---
title: Installation guide for DAFoam v2.2.0 and before
keywords: dafoam, installation, compile
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_source_220.html
folder: mydoc
---

{% include note.html content="This section assumes you want to compile the DAFoam optimization package (v2.0) from the source on a Linux system. If you use the Docker image, there is no need to compile anything and you can skip this section." %}

The DAFoam package can be compiled with various dependency versions. Here we elaborate on how to compile it on Ubuntu 18.04 using the dependencies shown in the following table. 


Ubuntu | Compiler | OpenMPI | mpi4py | PETSc  | petsc4py | CGNS  | Python | Numpy  | Scipy | Cython
| :------------------------------------------------------------------------------------------------ | 
18.04  | gcc/7.5  | 1.10.7  | 3.0.2  | 3.11.4 | 3.11.0   | 3.3.0 | 3.6.5  | 1.14.3 | 1.1.0 | 0.29.21

To compile, you can just copy the code blocks in the following steps and run them on the terminal. 

{% include note.html content="If a code block contains multiple lines, copy all the lines and run them on the terminal. Make sure each step run successfully before going to the next one. The entire compilation may take a few hours, the most time-consuming part is to compile OpenFOAM." %}


## **Prerequisites**

Run this on terminal to install prerequisites:

<pre>
sudo apt-get update && \
sudo apt-get install -y build-essential flex bison cmake zlib1g-dev libboost-system-dev libboost-thread-dev libreadline-dev libncurses-dev libxt-dev qt5-default libqt5x11extras5-dev libqt5help5 qtdeclarative5-dev qttools5-dev libqtwebkit-dev freeglut3-dev libqt5opengl5-dev texinfo  libscotch-dev libcgal-dev gfortran swig wget git vim cmake-curses-gui libfl-dev apt-utils libibverbs-dev --no-install-recommends
</pre>

After this, create a "packages" in your home directory:

<pre>
mkdir -p $HOME/packages
</pre>

## **Python**

Install Anaconda3-5.2.0 by running this command:

<pre>
cd $HOME/packages && \
wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh && \
chmod 755 Anaconda3-5.2.0-Linux-x86_64.sh && \
./Anaconda3-5.2.0-Linux-x86_64.sh -b -p $HOME/packages/anaconda3 && \
echo '# Anaconda3' >> $HOME/.bashrc && \
echo 'export PATH=$HOME/packages/anaconda3/bin:$PATH' >> $HOME/.bashrc && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/packages/anaconda3/lib' >> $HOME/.bashrc && \
. $HOME/.bashrc
</pre>

Then upgrade the pip utility:

<pre>
pip install --upgrade pip
</pre>

## **OpenMPI**

First append relevant environmental variables by running:

<pre>
echo '# OpenMPI-1.10.7' >> $HOME/.bashrc && \
echo 'export MPI_INSTALL_DIR=$HOME/packages/openmpi-1.10.7/opt-gfortran' >> $HOME/.bashrc && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib' >> $HOME/.bashrc && \
echo 'export PATH=$MPI_INSTALL_DIR/bin:$PATH' >> $HOME/.bashrc && \
. $HOME/.bashrc
</pre>

Then, configure and build OpenMPI:

<pre>
cd $HOME/packages && \
wget https://download.open-mpi.org/release/open-mpi/v1.10/openmpi-1.10.7.tar.gz  && \
tar -xvf openmpi-1.10.7.tar.gz && \
cd openmpi-1.10.7 && \
./configure --prefix=$MPI_INSTALL_DIR && \
make all install
</pre>

To verify the installation, run:

<pre>
mpicc -v
</pre>

You should see the version of the compiled OpenMPI.

Finally, install mpi4py-3.0.2:

<pre>
pip install mpi4py==3.0.2
</pre>

## **Petsc**

First append relevant environmental variables by running:

<pre>   
echo '# Petsc-3.11.4' >> $HOME/.bashrc && \
echo 'export PETSC_DIR=$HOME/packages/petsc-3.11.4' >> $HOME/.bashrc && \
echo 'export PETSC_ARCH=real-opt' >> $HOME/.bashrc && \
echo 'export PATH=$PETSC_DIR/$PETSC_ARCH/bin:$PATH' >> $HOME/.bashrc && \
echo 'export PATH=$PETSC_DIR/$PETSC_ARCH/include:$PATH' >> $HOME/.bashrc && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib' >> $HOME/.bashrc && \
echo 'export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib' >> $HOME/.bashrc
. $HOME/.bashrc
</pre>

Then, configure and compile:

<pre>
cd $HOME/packages && \
wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.11.4.tar.gz  && \
tar -xvf petsc-3.11.4.tar.gz && \
cd petsc-3.11.4 && \
./configure --PETSC_ARCH=real-opt --with-scalar-type=real --with-debugging=0 --with-mpi-dir=$MPI_INSTALL_DIR --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes --download-fblaslapack=yes --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11 && \
make PETSC_DIR=$HOME/packages/petsc-3.11.4 PETSC_ARCH=real-opt all
</pre>

Finally, install petsc4py-3.11.0:

<pre>
pip install petsc4py==3.11.0
</pre>

## **CGNS**

First append relevant environmental variables by running:

<pre>  
echo '# CGNS-3.3.0' >> $HOME/.bashrc && \
echo 'export CGNS_HOME=$HOME/packages/CGNS-3.3.0/opt-gfortran' >> $HOME/.bashrc && \
echo 'export PATH=$PATH:$CGNS_HOME/bin' >> $HOME/.bashrc && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib' >> $HOME/.bashrc && \
. $HOME/.bashrc
</pre>

Then, configure and compile:

<pre>
cd $HOME/packages && \
wget https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz  && \
tar -xvaf v3.3.0.tar.gz && \
cd CGNS-3.3.0 && \
mkdir -p build && \
cd build && \
cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME -DCGNS_BUILD_CGNSTOOLS=0 && \
make all install
</pre>

## **MACH-Aero framework**

The supported repo versions in the MACH-Aero framework for DAFoam-{{ site.latest_version }} is as follows

baseclasses | pySpline | pyGeo  | multipoint | pyHyp  | cgnsUtilities | IDWarp  | pyOptSparse | pyOFM  | DAFoam
| :----------------------------------------------------------------------------------------------------------- | 
v1.2.0      | v1.2.0   | v1.2.0 | v1.2.0     | v2.2.0 | v2.2.0        | v2.2.1  | v2.1.3      | v1.2.0 | {{ site.latest_version }}



To install all the repos in MACH-Aero, first create a "repos" folder in the $HOME directory:

<pre>
mkdir -p $HOME/repos
</pre>

Now run this command to install all the repos for MACH-Aero:

<pre>
cd $HOME/repos && \
wget https://github.com/mdolab/baseclasses/archive/v1.2.0.tar.gz -O baseclasses.tar.gz && \
tar -xvf baseclasses.tar.gz && cd baseclasses-1.2.0 && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/pyspline/archive/v1.2.0.tar.gz -O pyspline.tar.gz && \
tar -xvf pyspline.tar.gz && cd pyspline-1.2.0 && \
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
make && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/pygeo/archive/v1.2.0.tar.gz -O pygeo.tar.gz && \
tar -xvf pygeo.tar.gz && cd pygeo-1.2.0 && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/multipoint/archive/v1.2.0.tar.gz -O multipoint.tar.gz && \
tar -xvf multipoint.tar.gz && cd multipoint-1.2.0 && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/pyhyp/archive/v2.2.0.tar.gz -O pyhyp.tar.gz && \
tar -xvf pyhyp.tar.gz && cd pyhyp-2.2.0 && \
cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
make && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/cgnsutilities/archive/v2.2.0.tar.gz -O cgnsutilities.tar.gz && \
tar -xvf cgnsutilities.tar.gz && cd cgnsutilities-2.2.0 && \
cp config.mk.info config.mk && \
make && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/idwarp/archive/v2.2.1.tar.gz -O idwarp.tar.gz && \
tar -xvf idwarp.tar.gz && cd idwarp-2.2.1 && \
cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
make && pip install . && \
cd $HOME/repos && \
wget https://github.com/mdolab/pyoptsparse/archive/v2.1.3.tar.gz -O pyoptsparse.tar.gz && \
tar -xvf pyoptsparse.tar.gz && cd pyoptsparse-2.1.3 && \
pip install .
</pre>

## **OpenFOAM**

Compile OpenFOAM-v1812 by running:

<pre>
mkdir -p $HOME/OpenFOAM && \
cd $HOME/OpenFOAM && \
wget https://sourceforge.net/projects/openfoamplus/files/v1812/OpenFOAM-v1812.tgz/download -O OpenFOAM-v1812.tgz && \
wget https://sourceforge.net/projects/openfoamplus/files/v1812/ThirdParty-v1812.tgz/download -O ThirdParty-v1812.tgz && \
tar -xvf OpenFOAM-v1812.tgz && \
tar -xvf ThirdParty-v1812.tgz && \
cd $HOME/OpenFOAM/OpenFOAM-v1812 && \
wget https://github.com/DAFoam/files/releases/download/v1.0.0/UPstream.C && \
mv UPstream.C src/Pstream/mpi/UPstream.C && \
. etc/bashrc && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

{% include note.html content="In the above command, we replaced the OpenFOAM-v1812's built-in UPstream.C file with a customized one because we need to prevent OpenFOAM from calling the MPI_Finialize function when wrapping OpenFOAM functions using Cython." %}

{% include note.html content="NOTE: The above command will compile OpenFOAM using 4 CPU cores. If you want to compile OpenFOAM using more cores, change the ``WM_NCOMPPROCS`` parameter before running ``./Allwmake``" %}

Finally, verify the installation by running:

<pre>
simpleFoam -help
</pre>

It should see some basic information of OpenFOAM

## **pyOFM**

First install Cython:

<pre>
pip install cython==0.29.21
</pre>

Then, compile pyOFM by running:

<pre>
cd $HOME/repos && \
wget https://github.com/mdolab/pyofm/archive/v1.2.0.tar.gz -O pyofm.tar.gz && \
tar -xvf pyofm.tar.gz && cd pyofm-1.2.0 && \
. $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
make && pip install .
</pre>

## **DAFoam**

Compile DAFoam by running:

<pre>
cd $HOME/repos && \
wget https://github.com/mdolab/dafoam/archive/{{ site.latest_version }}.tar.gz -O dafoam.tar.gz && \
tar -xvf dafoam.tar.gz && cd dafoam-* && \
. $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc && \
./Allmake && pip install .
</pre>

Once DAFoam is compiled, run the regression test:

<pre>
cd $HOME/repos/dafoam/tests && ./Allrun
</pre>

The regression tests should take less than 30 minutes. The test progress will be printed to screen. Make sure you see this at the end:

<pre>   
************************************************************
**************** All DAFoam tests passed! ******************
************************************************************
</pre>

{% include note.html content="Load the OpenFOAM environments: `source $HOME/OpenFOAM/OpenFOAM-v1812/etc/bashrc` before running any jobs!" %}

|

In summary, here is the folder structures for all the installed packages:

<pre>   
$HOME
  - OpenFOAM
    - OpenFOAM-v1812
    - ThirdParty-v1812
  - packages
    - anaconda3
    - CGNS-3.3.0
    - mpi4py-3.0.2
    - petsc-3.11.4
    - petsc4py-3.11.0
  - repos
    - baseclasses
    - cgnsutilities
    - dafoam
    - idwarp
    - multipoint
    - pygeo
    - pyhyp
    - pyofm
    - pyoptsparse
    - pyspline
</pre>

Here is the DAFoam related environmental variable setup that should appear in your bashrc file:

<pre>
# OpenMPI-1.10.7
export MPI_INSTALL_DIR=$HOME/packages/openmpi-1.10.7/opt-gfortran
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$MPI_INSTALL_DIR/lib
export PATH=$MPI_INSTALL_DIR/bin:$PATH
# PETSC
export PETSC_DIR=$HOME/packages/petsc-3.11.4
export PETSC_ARCH=real-opt
export PATH=$PETSC_DIR/$PETSC_ARCH/bin:$PATH
export PATH=$PETSC_DIR/$PETSC_ARCH/include:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib
export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib
# CGNS-3.3.0
export CGNS_HOME=$HOME/packages/CGNS-3.3.0/opt-gfortran
export PATH=$PATH:$CGNS_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib
</pre>

{% include links.html %}

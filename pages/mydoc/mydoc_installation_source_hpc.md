---
title: Compile from source (HPC)
keywords: dafoam, installation, compile
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_source_hpc.html
folder: mydoc
---

{% include note.html content="This section provides instructions on compiling the DAFoam optimization package on an HPC system (Stampede 2) with Intel compilers. Installation on other intel-based clusters may differ, but follows the same general procedure" %}

The required modules on Stampede are:


TACC  | git    | intel  | libfabric | impi   | boost | petsc       | python3
| :------------------------------------------------------------------------ | 
N / A | 2.24.1 | 18.0.2 | 1.7.0     | 18.0.2 | 1.68  | 3.11-nohdf5 | 3.7.0

All DAFoam installation files should be stored within `$WORK/DAFoam_Codes`.
The directory structure of the completed installation should be the following:

<pre>
DAFoam/
└───DAFOAM_VENV/
│
└───OpenFOAM/
│   └───OpenFOAM-v1812/
│   └───OpenFOAM-v1812-ADF/
│   └───OpenFOAM-v1812-ADR/
│   └───sharedBins/
│   └───sharedLibs/
│   └───ThirdParty-v1812/
│
└───packages/
│   └───CGNS-3.3.0/
│
└───repos/
│   └───baseclasses/
│   └───cgnsutilities/
│   └───dafoam/
│   └───idwarp/
│   └───mphys/
│   └───multipoint/
│   └───pygeo/
│   └───pyhyp/
│   └───pyofm/
│   └───pyoptsparse/
│   └───pyspline/
│ 
└───ENV_DAFOAM.sh/
</pre>

Create this directory structure by navigating to the `$WORK` directory and running:

<pre>
mkdir DAFoam
cd DAFoam
mkdir OpenFOAM packages repos
</pre>

## **Setup Environment Loader**

Enter `$WORK/DAFoam` and create the file: `ENV_DAFOAM.sh`. Add the following to `ENV_DAFOAM.sh`:

<pre>
#!/bin/bash

echo "=================== Initializing DAFoam Environment ==================="
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Modules
echo "Loading Modules"
module purge
module load TACC
module load git/2.24.1
module load intel/18.0.2
module load libfabric/1.7.0
module load impi/18.0.2
module load boost/1.68
module load petsc/3.11-nohdf5
module load python3/3.7.0

# DAFoam
echo "Initializing DAFoam"
export DAFOAM_ROOT_PATH=$DIR

# CGNS
echo "Initializing CGNS"
export CGNS_HOME=$DIR/packages/CGNS-3.3.0/opt-gfortran
export PATH=$PATH:$CGNS_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib

# OpenFOAM
echo "Initializing OpenFOAM"
source $DIR/OpenFOAM/OpenFOAM-v1812/etc/bashrc
export LD_LIBRARY_PATH=$DIR/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH
PATH=$DIR/OpenFOAM/sharedBins:$PATH

# Python Virtual Environment
echo "Initializing Python Virtual Environment"
source $DIR/DAFOAM_VENV/bin/activate

echo "================= Done Initializing DAFOAM Environment ================"
</pre>

This file will be responsible for loading the DAFoam environment once everything is installed. A command to source the file can be added to your `bashrc`, or you can call the file by navigating to its directory and running (run this command now):

<pre>
. ENV_DAFOAM.sh
</pre>

## **Create Python Virtual Environment**
Create a Python virtual environment using `venv`:

<pre>
python3 -m venv DAFOAM_VENV
</pre>

Re-source the environment initialization script to activate the virtual environment:

<pre>
. ENV_DAFOAM.sh
</pre>

Install the python dependencies:

<pre>
pip3 install --upgrade pip
pip3 install numpy==1.21.2
pip3 install scipy==1.7.1
pip3 install cython==0.29.21
pip3 install numpy-stl==2.16.0
pip3 install petsc4py==3.11.0
</pre>


## **Install OpenFOAM**

Download OpenFOAM and untar its files into working directory:

<pre>
cd OpenFOAM
wget https://sourceforge.net/projects/openfoamplus/files/v1812/OpenFOAM-v1812.tgz/download -O OpenFOAM-v1812.tgz
wget https://sourceforge.net/projects/openfoamplus/files/v1812/ThirdParty-v1812.tgz/download -O ThirdParty-v1812.tgz
tar -xvf OpenFOAM-v1812.tgz
tar -xvf ThirdParty-v1812.tgz
</pre>

Enter the `OpenFOAM-v1812` directory:

<pre>
cd OpenFOAM-v1812
</pre>

Replace the built-in UPstream.C file with a customized version:

<pre>
wget https://github.com/DAFoam/files/releases/download/v1.0.0/UPstream.C
mv UPstream.C src/Pstream/mpi/UPstream.C
</pre>

Edit `OpenFOAM-v1812/etc/bashrc`:

<pre>
projectDir="$HOME/OpenFOAM/OpenFoam-$WM_PROJECT_VERSION"
->
projectDir="$DAFOAM_ROOT_PATH/OpenFOAM/OpenFoam-$WM_PROJECT_VERSION"
-------------------------------------------------
export WM_COMPILER=Gcc
->
export WM_COMPILER=Icc
-------------------------------------------------
export WM_MPLIB=SYSTEMOPENMPI
->
export WM_MPLIB=INTELMPI
-------------------------------------------------
foamOldDirs="$WM_PROJECT_DIR $WM_THIRD_PARTY_DIR \
    $HOME/$WM_PROJECT/$USER $FOAM_USER_APPBIN $FOAM_USER_LIBBIN \
    $WM_PROJECT_SITE $FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN"
->
foamOldDirs="$WM_PROJECT_DIR $WM_THIRD_PARTY_DIR \
    $DAFOAM_ROOT_PATH/$WM_PROJECT/$USER $FOAM_USER_APPBIN $FOAM_USER_LIBBIN \
    $WM_PROJECT_SITE $FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN"
-------------------------------------------------
export WM_PROJECT_USER_DIR=$HOME/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
->
export WM_PROJECT_USER_DIR=$DAFOAM_ROOT_PATH/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
</pre>

Edit `OpenFOAM-v1812/etc/config.sh/CGAL`:

<pre>
boost_version=boost_1_64_0
-> 
boost_version=boost-system
-------------------------------------------------
export BOOST_ARCH_PATH=$WM_THIRD_PARTY_DIR/platforms/$WM_ARCH$WM_COMPILER/$boost_version
->
export BOOST_ARCH_PATH=$TACC_BOOST_DIR
</pre>

Edit `OpenFOAM-v1812/etc/config.sh/settings`:

<pre>
export WM_CC="gcc"
export WM_CXX="g++"
export WM_CFLAGS="-fPIC"
export WM_CXXFLAGS="-fPIC -std=c++11"
->
export WM_CC="mpicc"
export WM_CXX="mpicxx"
export WM_CFLAGS="-O3 -fPIC"
export WM_CXXFLAGS="-O3 -fPIC -std=c++11"
-------------------------------------------------
64)
    WM_ARCH=linux64
    export WM_COMPILER_LIB_ARCH=64
    export WM_CFLAGS="$WM_CFLAGS -m64"
    export WM_CXXFLAGS="$WM_CXXFLAGS -m64"
    export WM_LDFLAGS="-m64"
->
64)
    WM_ARCH=linux64
    export WM_COMPILER_LIB_ARCH=64
    export WM_CFLAGS="$WM_CFLAGS"
    export WM_CXXFLAGS="$WM_CXXFLAGS"
    export WM_LDFLAGS="-O3"
</pre>

Edit `OpenFOAM-v1812/wmake/rules/linux64Icc/c`:

<pre>
cc          = icc
->
cc          = mpicc
</pre>

Edit `OpenFOAM-v1812/wmake/rules/linux64Icc/c++`:

<pre>
CC          = icpc -std=c++11 -fp-trap=common -fp-model precise
->
CC          = mpicxx -std=c++11 -fp-trap=common -fp-model precise
</pre>


Copy `mplibINTELMPI` in `OpenFOAM-v1812/wmake/rules/linux64Icc/mplibINTELMPI` to `OpenFOAM-v1812/wmake/rules/General/mplibINTELMPI`


Edit `ThirdParty-v1812/makeCGAL`:

<pre>
  : ${BOOST_ARCH_PATH:=$installBASE/$boostPACKAGE}    # Fallback
->
  : ${BOOST_ARCH_PATH:=$TACC_BOOST_DIR}    # Fallback
</pre>

Source the OpenFOAM bashrc file:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc
</pre>

Make CGAL:

<pre>
cd $WM_THIRD_PARTY_DIR and ./makeCGAL > log.mkcgal 2>&1
</pre>

Make OpenFOAM:

<pre>
cd $WM_PROJECT_DIR and ./Allwmake > log.make 2>&1
</pre>

## **Install OpenFOAM AD**

Download the AD version of OpenFOAM:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM
wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v1.2.9.tar.gz -O OpenFOAM-v1812-AD.tgz
</pre>

### **Reverse Mode**

Unzip the code, move the AD version of OpenFOAM to mark it as reverse-mode, and enter the code directory:

<pre>
tar -xvf OpenFOAM-v1812-AD.tgz
mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADR
cd OpenFOAM-v1812-ADR
</pre>

Edit `OpenFOAM-v1812-ADR/etc/bashrc`:

<pre>
export WM_PROJECT_VERSION=v1812-AD
->
export WM_PROJECT_VERSION=v1812-ADR
-------------------------------------------------
projectDir="$HOME/OpenFOAM/OpenFoam-$WM_PROJECT_VERSION"
->
projectDir="$DAFOAM_ROOT_PATH/OpenFOAM/OpenFoam-$WM_PROJECT_VERSION"
-------------------------------------------------
export WM_COMPILER=Gcc
->
export WM_COMPILER=Icc
-------------------------------------------------
export WM_MPLIB=SYSTEMOPENMPI
->
export WM_MPLIB=INTELMPI
-------------------------------------------------
export WM_CODI_AD_MODE=CODI_AD_FORWARD
->
export WM_CODI_AD_MODE=CODI_AD_REVERSE
-------------------------------------------------
foamOldDirs="$WM_PROJECT_DIR $WM_THIRD_PARTY_DIR \
    $HOME/$WM_PROJECT/$USER $FOAM_USER_APPBIN $FOAM_USER_LIBBIN \
    $WM_PROJECT_SITE $FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN"
->
foamOldDirs="$WM_PROJECT_DIR $WM_THIRD_PARTY_DIR \
    $DAFOAM_ROOT_PATH/$WM_PROJECT/$USER $FOAM_USER_APPBIN $FOAM_USER_LIBBIN \
    $WM_PROJECT_SITE $FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN"
-------------------------------------------------
export WM_PROJECT_USER_DIR=$HOME/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
->
export WM_PROJECT_USER_DIR=$DAFOAM_ROOT_PATH/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
</pre>

Edit `OpenFOAM-v1812-ADR/etc/config.sh/CGAL`:

<pre>
boost_version=boost_1_64_0
-> 
boost_version=boost-system
-------------------------------------------------
export BOOST_ARCH_PATH=$WM_THIRD_PARTY_DIR/platforms/$WM_ARCH$WM_COMPILER/$boost_version
->
export BOOST_ARCH_PATH=$TACC_BOOST_DIR
</pre>

Edit `OpenFOAM-v1812-ADR/etc/config.sh/settings`:

<pre>
export WM_CC="gcc"
export WM_CXX="g++"
export WM_CFLAGS="-fPIC"
export WM_CXXFLAGS="-fPIC -std=c++11"
->
export WM_CC="mpicc"
export WM_CXX="mpicxx"
export WM_CFLAGS="-O3 -fPIC"
export WM_CXXFLAGS="-O3 -fPIC -std=c++11"
-------------------------------------------------
64)
    WM_ARCH=linux64
    export WM_COMPILER_LIB_ARCH=64
    export WM_CFLAGS="$WM_CFLAGS -m64"
    export WM_CXXFLAGS="$WM_CXXFLAGS -m64"
    export WM_LDFLAGS="-m64"
->
64)
    WM_ARCH=linux64
    export WM_COMPILER_LIB_ARCH=64
    export WM_CFLAGS="$WM_CFLAGS"
    export WM_CXXFLAGS="$WM_CXXFLAGS"
    export WM_LDFLAGS="-O3"
</pre>

Edit `OpenFOAM-v1812-ADR/wmake/rules/linux64Icc/c`:

<pre>
cc          = icc
->
cc          = mpicc
</pre>

Edit `OpenFOAM-v1812-ADR/wmake/rules/linux64Icc/c++`:

<pre>
CC          = icpc -std=c++11 -fp-trap=common -fp-model precise
->
CC          = mpicxx -std=c++11 -fp-trap=common -fp-model precise
</pre>


Copy `mplibINTELMPI` in `OpenFOAM-v1812-ADR/wmake/rules/linux64Icc/mplibINTELMPI` to `OpenFOAM-v1812-ADR/wmake/rules/General/mplibINTELMPI`


Source the OpenFOAM reverse-mode bashrc file:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADR/etc/bashrc
</pre>

Make OpenFOAM reverse-mode:


<pre>
cd $WM_PROJECT_DIR and ./Allwmake > log.make 2>&1
</pre>

Link reverse-mode mode code to OpenFOAM:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib
ln -s ../../../../OpenFOAM-v1812-ADR/platforms/*/lib/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/dummy/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/mpi
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/mpi/*.so .
</pre>

### **Forward Mode**

Unzip the code, move the AD version of OpenFOAM to mark it as forward-mode, and enter the code directory:

<pre>
tar -xvf OpenFOAM-v1812-AD.tgz
mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADF
cd OpenFOAM-v1812-ADF
</pre>

Edit `OpenFOAM-v1812-ADF/etc/bashrc`:

<pre>
export WM_PROJECT_VERSION=v1812-AD
->
export WM_PROJECT_VERSION=v1812-ADF
-------------------------------------------------
projectDir="$HOME/OpenFOAM/OpenFoam-$WM_PROJECT_VERSION"
->
projectDir="$DAFOAM_ROOT_PATH/OpenFOAM/OpenFoam-$WM_PROJECT_VERSION"
-------------------------------------------------
export WM_COMPILER=Gcc
->
export WM_COMPILER=Icc
-------------------------------------------------
export WM_MPLIB=SYSTEMOPENMPI
->
export WM_MPLIB=INTELMPI
-------------------------------------------------
foamOldDirs="$WM_PROJECT_DIR $WM_THIRD_PARTY_DIR \
    $HOME/$WM_PROJECT/$USER $FOAM_USER_APPBIN $FOAM_USER_LIBBIN \
    $WM_PROJECT_SITE $FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN"
->
foamOldDirs="$WM_PROJECT_DIR $WM_THIRD_PARTY_DIR \
    $DAFOAM_ROOT_PATH/$WM_PROJECT/$USER $FOAM_USER_APPBIN $FOAM_USER_LIBBIN \
    $WM_PROJECT_SITE $FOAM_SITE_APPBIN $FOAM_SITE_LIBBIN"
-------------------------------------------------
export WM_PROJECT_USER_DIR=$HOME/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
->
export WM_PROJECT_USER_DIR=$DAFOAM_ROOT_PATH/$WM_PROJECT/$USER-$WM_PROJECT_VERSION
</pre>

Edit `OpenFOAM-v1812-ADF/etc/config.sh/CGAL`:

<pre>
boost_version=boost_1_64_0
-> 
boost_version=boost-system
-------------------------------------------------
export BOOST_ARCH_PATH=$WM_THIRD_PARTY_DIR/platforms/$WM_ARCH$WM_COMPILER/$boost_version
->
export BOOST_ARCH_PATH=$TACC_BOOST_DIR
</pre>

Edit `OpenFOAM-v1812-ADF/etc/config.sh/settings`:

<pre>
export WM_CC="gcc"
export WM_CXX="g++"
export WM_CFLAGS="-fPIC"
export WM_CXXFLAGS="-fPIC -std=c++11"
->
export WM_CC="mpicc"
export WM_CXX="mpicxx"
export WM_CFLAGS="-O3 -fPIC"
export WM_CXXFLAGS="-O3 -fPIC -std=c++11"
-------------------------------------------------
64)
    WM_ARCH=linux64
    export WM_COMPILER_LIB_ARCH=64
    export WM_CFLAGS="$WM_CFLAGS -m64"
    export WM_CXXFLAGS="$WM_CXXFLAGS -m64"
    export WM_LDFLAGS="-m64"
->
64)
    WM_ARCH=linux64
    export WM_COMPILER_LIB_ARCH=64
    export WM_CFLAGS="$WM_CFLAGS"
    export WM_CXXFLAGS="$WM_CXXFLAGS"
    export WM_LDFLAGS="-O3"
</pre>

Edit `OpenFOAM-v1812-ADF/wmake/rules/linux64Icc/c`:

<pre>
cc          = icc
->
cc          = mpicc
</pre>

Edit `OpenFOAM-v1812-ADF/wmake/rules/linux64Icc/c++`:

<pre>
CC          = icpc -std=c++11 -fp-trap=common -fp-model precise
->
CC          = mpicxx -std=c++11 -fp-trap=common -fp-model precise
</pre>


Copy `mplibINTELMPI` in `OpenFOAM-v1812-ADF/wmake/rules/linux64Icc/mplibINTELMPI` to `OpenFOAM-v1812-ADF/wmake/rules/General/mplibINTELMPI`


Source the OpenFOAM forward-mode bashrc file:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADF/etc/bashrc
</pre>

Make OpenFOAM forward-mode:

<pre>
cd $WM_PROJECT_DIR and ./Allwmake > log.make 2>&1
</pre>

Link forward-mode code to OpenFOAM:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib
ln -s ../../../../OpenFOAM-v1812-ADF/platforms/*/lib/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM-v1812/platforms/*/lib/dummy
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/dummy/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM-v1812/platforms/*/lib/mpi
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/mpi/*.so .
</pre>


## **Install CGNS**

Enter the packages directory, download CGNS, untar the code files, and enter the CGNS directory:

<pre>
cd $DAFOAM_ROOT_PATH/packages/
wget https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz
tar -xvaf v3.3.0.tar.gz
cd CGNS-3.3.0
</pre>

Configure the CGNS build:

<pre>
cmake -D CGNS_ENABLE_FORTRAN=ON -D CMAKE_INSTALL_PREFIX=$CGNS_HOME -D CGNS_ENABLE_64BIT=OFF -D CGNS_BUILD_CGNSTOOLS=OFF -D CMAKE_C_COMPILER=$(which icc) -D CMAKE_Fortran_COMPILER=$(which ifort) .
</pre>

Make and install CGNS:

<pre>
make all install
</pre>

## **Install MACH-Aero**

Move to the `repos` directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

**NOTE:** This installation assumes you have already set up an SSH key to GitHub and clone the codes directly from the MDO Lab repositories. The same process can be carried out using forks instead, however the code versions should match.

For simplicity, the repos will be installed in-place.

### **baseClasses**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/baseclasses.git
cd baseclasses
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **pySpline**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/pyspline.git
cd pyspline
</pre>

Copy the configuration file:

<pre>
cp config/defaults/config.LINUX_INTEL.mk config/config.mk
</pre>

Compile the code:

<pre>
make
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **pyGeo**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/pygeo.git
cd pygeo
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **multipoint**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/multipoint.git
cd multipoint
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **pyHyp**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/pyhyp.git
cd pyhyp
</pre>

Copy the configuration file:

<pre>
cp config/defaults/config.LINUX_INTEL_OPENMPI.mk config/config.mk
</pre>

Compile the code:

<pre>
make
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **cgnsUtilities**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/cgnsutilities.git
cd cgnsutilities
</pre>

Copy the configuration file:

<pre>
cp config/defaults/config.LINUX_INTEL.mk config/config.mk
</pre>

Compile the code:

<pre>
make
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **IDWarp**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/idwarp.git
</pre>

Copy the configuration file:

<pre>
cp config/defaults/config.LINUX_INTEL_OPENMPI.mk config/config.mk
</pre>

Compile the code:

<pre>
make
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

### **pyOptSparse**

**NOTE:** pyOptSparse can be modified before installing to include additional optimizers. Refer to the pyOptSparse documentation for more information

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/pyoptsparse.git
cd pyoptsparse
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

## **Install pyOFM**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/pyofm.git
cd pyofm
</pre>

pyOFM requires a newer version of `mpi4py` than is available on STAMPEDE natively. To avoid installing a second `mpi4py`, edit the `setup.py` script within the `pyofm/` root directory:

<pre>
install_requires=[
    'numpy>=1.16.4',
    'mpi4py>=3.0.2',
],
->
install_requires=[
    'numpy>=1.16.4',
    'mpi4py>=3.0.0',
],
</pre>

Make the package:

<pre>
make
</pre>

* Install the package:

<pre>
pip3 install -e .
</pre>

Return to the repos directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

## **Install DAFoam**

Clone the repository and enter the directory:

<pre>
git clone git@github.com:mdolab/dafoam.git
cd dafoam
</pre>

DAFoam requires a newer version of `mpi4py` than is available on STAMPEDE natively. To avoid installing a second `mpi4py`, edit the `setup.py` script within the `dafoam/` root directory:

<pre>
install_requires=[
    "numpy>=1.16.4",
    "mpi4py>=3.0.2",
    "petsc4py>=3.11.0",
    "cython>=0.29.21",
],
->
install_requires=[
    "numpy>=1.16.4",
    "mpi4py>=3.0.0",
    "petsc4py>=3.11.0",
    "cython>=0.29.21",
],
</pre>

Build DAFoam original:

<pre>
. $DAFOAM_ROOT_PATH/ENV_DAFOAM.sh
./Allmake 2> errorLog.txt
</pre>

Build DAFoam reverse-mode:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADR/etc/bashrc
./Allclean && ./Allmake 2> errorLog.txt
</pre>

Build DAFoam forward-mode:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADF/etc/bashrc
./Allclean && ./Allmake 2> errorLog.txt
</pre>

Install the package:

<pre>
pip3 install -e .
</pre>

Unset the AD environment:

<pre>
unset WM_CODI_AD_MODE\
. $DAFOAM_ROOT_PATH/ENV_DAFOAM.sh
</pre>


{% include links.html %}

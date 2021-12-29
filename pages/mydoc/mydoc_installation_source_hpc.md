---
title: Compile from source (HPC)
keywords: dafoam, installation, compile
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_source_hpc.html
folder: mydoc
---

{% include note.html content="This section provides instructions on compiling the DAFoam optimization package on an HPC system (Stampede 2) with Intel compilers. Installation on other intel-based clusters may differ, but follows the same general procedure" %}

The DAFoam package can be compiled with various dependency versions. For this installation, we will use the following modules already installed on Stampede 2:


TACC  | git    | intel  | libfabric | impi   | boost | petsc       | python3
| :------------------------------------------------------------------------ | 
N / A | 2.24.1 | 18.0.2 | 1.7.0     | 18.0.2 | 1.68  | 3.11-nohdf5 | 3.7.0

For this installtion, we will store all of the DAFoam installation files within `$WORK/DAFoam`. Follow this guide line-by-line, reproducing each command on your terminal. Ensure that each command exits successfully before moving to the next one. Once the installation is complete, the directory structure of the installation should be the following:

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

Begin by navigating to the `$WORK` directory and generating the DAFoam code directory and its subdirectory structure:

<pre>
mkdir DAFoam
cd DAFoam
mkdir OpenFOAM packages repos
</pre>

## **Setup Environment Loader**
To simplify the process of initializing the DAFoam environment when logging into Stampede, we will create a bash script that automates the steps required to load the required modules, export the required environment variables, and source the Python virtual environment. To generate this script, enter `$WORK/DAFoam` and create the file: `ENV_DAFOAM.sh`. Add the following to `ENV_DAFOAM.sh`:

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

This file will be responsible for loading the DAFoam environment once everything is installed. A command to source the file can be added to your `bashrc`, or you can call the file by navigating to its directory and running the following command (run this command now):

<pre>
. ENV_DAFOAM.sh
</pre>

This command will output information stating that the DAFoam environment is being initialized. Since DAFoam and the assorted environment components are not yet installed, the script will output some errors.

## **Create Python Virtual Environment**
To modularize the DAFoam environment, we will use a Python virtual environment. Create a Python virtual environment using the package `venv`:

<pre>
python3 -m venv DAFOAM_VENV
</pre>

Re-source the environment initialization script to activate the virtual environment:

<pre>
. ENV_DAFOAM.sh
</pre>

After re-sourcing the environment initialization script your terminal prompt should include the label `(ENV_DAFOAM)`. Install the Python dependencies in the virtual environment:

<pre>
pip3 install --upgrade pip
pip3 install numpy==1.21.2
pip3 install scipy==1.7.1
pip3 install cython==0.29.21
pip3 install numpy-stl==2.16.0
pip3 install petsc4py==3.11.0
</pre>

## **Install OpenFOAM**

We will begin by install OpenFOAM-v1812. **There are three versions of OpenFOAM to compile: original, reverse-mode AD (ADR), and forward-mode AD (ADF).** The reverse-mode AD enables the JacobianFree adjoint option, and the forward-mode AD enables the brute-force AD for verifying the adjoint accuracy. These packages should be installed in the `OpenFoam/` directory.

**Build Original**

Begin by downloading OpenFOAM-v1812 and the associated third-party libraries, and unzip the tarballs:

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

We will make several modifications to the configuration files within OpenFOAM. The following steps show which files need to be changed and what changes are required.

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


Copy `mplibINTELMPI`:

<pre>
cp OpenFOAM-v1812/wmake/rules/linux64Icc/mplibINTELMPI OpenFOAM-v1812/wmake/rules/General/mplibINTELMPI
</pre>

Edit `ThirdParty-v1812/makeCGAL`:

<pre>
  : ${BOOST_ARCH_PATH:=$installBASE/$boostPACKAGE}    # Fallback
->
  : ${BOOST_ARCH_PATH:=$TACC_BOOST_DIR}    # Fallback
</pre>

Once the configuration file modifications are complete, source the OpenFOAM bashrc file:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc
</pre>

We will begin the installation by making CGAL. To do this, run the following command:

<pre>
cd $WM_THIRD_PARTY_DIR and ./makeCGAL > log.mkcgal 2>&1
</pre>

Once the CGAL installation is complete, we will install OpenFOAM using the following command:

<pre>
cd $WM_PROJECT_DIR and ./Allwmake > log.make 2>&1
</pre>

Once the original version of OpenFOAM is installed, we will install the AD versions of the code. These packages should be in the `OpenFOAM/` directory. Download the AD version of OpenFOAM using the following command:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM
wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v1.2.9.tar.gz -O OpenFOAM-v1812-AD.tgz
</pre>

**Reverse Mode**

Unzip the  downloaded AD code, move the AD version of OpenFOAM to mark it as reverse-mode, and enter its code directory:

<pre>
tar -xvf OpenFOAM-v1812-AD.tgz
mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADR
cd OpenFOAM-v1812-ADR
</pre>

As with the original version of OpenFOAM, we need to make several modifications to the configuration files within the reverse-mode AD version of OpenFOAM. The following steps show which files need to be changed and what changes are required.

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


Copy `mplibINTELMPI`:

<pre>
cp OpenFOAM-v1812-ADR/wmake/rules/linux64Icc/mplibINTELMPI OpenFOAM-v1812-ADR/wmake/rules/General/mplibINTELMPI
</pre>

Once the configuration file modifications are complete, source the OpenFOAM reverse-mode bashrc file:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADR/etc/bashrc
</pre>

Install OpenFOAM reverse-mode AD using the following command:

<pre>
cd $WM_PROJECT_DIR and ./Allwmake > log.make 2>&1
</pre>

Once the reverse-mode AD version of the code is build, we need to link it to the original version. To do this, run the following commands to create soft links:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib
ln -s ../../../../OpenFOAM-v1812-ADR/platforms/*/lib/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/dummy/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/mpi
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/mpi/*.so .
</pre>

**Forward Mode**

Again unzip the AD code, move the AD version of OpenFOAM to mark it as forward-mode, and enter its code directory:

<pre>
tar -xvf OpenFOAM-v1812-AD.tgz
mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADF
cd OpenFOAM-v1812-ADF
</pre>

As with the original and reverse-mode versions of OpenFOAM, we need to make several modifications to the configuration files within the forward-mode AD version of OpenFOAM. The following steps show which files need to be changed and what changes are required.

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

Copy `mplibINTELMPI`:

<pre>
cp OpenFOAM-v1812-ADF/wmake/rules/linux64Icc/mplibINTELMPI OpenFOAM-v1812-ADF/wmake/rules/General/mplibINTELMPI
</pre>

Once the configuration file modifications are complete, source the OpenFOAM forward-mode bashrc file:

<pre>
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADF/etc/bashrc
</pre>

Install OpenFOAM forward-mode AD using the following command:

<pre>
cd $WM_PROJECT_DIR and ./Allwmake > log.make 2>&1
</pre>

As with the reverse-mode AD code, we need to link the built forward-mode AD code to the original version. To do this, run the following commands to create soft links:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib
ln -s ../../../../OpenFOAM-v1812-ADF/platforms/*/lib/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM-v1812/platforms/*/lib/dummy
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/dummy/*.so .
cd $DAFOAM_ROOT_PATH/OpenFOAM-v1812/platforms/*/lib/mpi
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/mpi/*.so .
</pre>


## **Install CGNS**

CGNS is a required dependency for DAFoam that should be installed within the ``packages/`` subdirectory of the DAFoam directory. Enter the packages directory, download CGNS, untar the code files, and enter the CGNS directory:

<pre>
cd $DAFOAM_ROOT_PATH/packages/
wget https://github.com/CGNS/CGNS/archive/v3.3.0.tar.gz
tar -xvaf v3.3.0.tar.gz
cd CGNS-3.3.0
</pre>

We will configure the CGNS build with several options. We will enable Fortran bindings, set the installation location, disable 64bit architecture, and specify the paths for the required Fortran and C compilers. Run this configuration step using the following command:

<pre>
cmake -D CGNS_ENABLE_FORTRAN=ON -D CMAKE_INSTALL_PREFIX=$CGNS_HOME -D CGNS_ENABLE_64BIT=OFF -D CGNS_BUILD_CGNSTOOLS=OFF -D CMAKE_C_COMPILER=$(which icc) -D CMAKE_Fortran_COMPILER=$(which ifort) .
</pre>

Once the configuration process is complete, make and install CGNS using the following command:

<pre>
make all install
</pre>

## **Install MACH-Aero**

The supported repo versions in the MACH-Aero framework for DAFoam-{{ site.latest_version }} is as follows

baseclasses | pySpline | pyGeo  | multipoint | pyHyp  | cgnsUtilities | IDWarp  | pyOptSparse | pyOFM  | DAFoam
| :----------------------------------------------------------------------------------------------------------- | 
v1.2.0      | v1.2.0   | v1.5.0 | v1.2.0     | v2.2.0 | v2.5.0        | v2.2.1  | v2.3.0      | v1.2.1 | {{ site.latest_version }}

The MACH-Aero packages are considered part of the DAFoam ecosystem and should be installed in the `repos/` subdirectory of the `DAFoam/` directory. Move to the `repos` directory:

<pre>
cd $DAFOAM_ROOT_PATH/repos/
</pre>

The following steps go through the process of installing the MACH-Aero codes one at a time, downloading, unpacking, building, and installing each package. For simplicity, the packages will be installed in-place.

### **baseClasses**

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/baseclasses/archive/v1.2.0.tar.gz -O baseclasses.tar.gz
tar -xvf baseclasses.tar.gz
cd baseclasses-1.2.0
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/pyspline/archive/v1.2.0.tar.gz -O pyspline.tar.gz
tar -xvf pyspline.tar.gz
cd pyspline-1.2.0
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/pygeo/archive/v1.5.0.tar.gz -O pygeo.tar.gz
tar -xvf pygeo.tar.gz
cd pygeo-1.5.0
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/multipoint/archive/v1.2.0.tar.gz -O multipoint.tar.gz
tar -xvf multipoint.tar.gz
cd multipoint-1.2.0
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/pyhyp/archive/v2.2.0.tar.gz -O pyhyp.tar.gz
tar -xvf pyhyp.tar.gz
cd pyhyp-2.2.0
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/cgnsutilities/archive/v2.5.0.tar.gz -O cgnsutilities.tar.gz
tar -xvf cgnsutilities.tar.gz
cd cgnsutilities-2.5.0
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/idwarp/archive/v2.2.1.tar.gz -O idwarp.tar.gz
tar -xvf idwarp.tar.gz
cd idwarp-2.2.1
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

Download the repository and enter the directory:

<pre>
wget https://github.com/mdolab/pyoptsparse/archive/v2.3.0.tar.gz -O pyoptsparse.tar.gz
tar -xvf pyoptsparse.tar.gz
cd pyoptsparse-2.3.0
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

In addition to installing the main components of MACH-Aero, we will install pyOFM to interface with OpenFOAM meshes. Download the repository and enter its code directory:

<pre>
wget https://github.com/mdolab/pyofm/archive/v1.2.1.tar.gz -O pyofm.tar.gz
tar -xvf pyofm.tar.gz
cd pyofm-1.2.1
</pre>

Make the package:

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

## **Install DAFoam**

Once OpenFOAM, CGNS, and the MACH-Aero packages are installed, we can install DAFoam. Similar to OpenFOAM, we need to compile three versions of DAFoam: original, reverse-mode AD (ADR), and forward-mode AD (ADF). Download the repository and enter its code directory:

<pre>
wget https://github.com/mdolab/dafoam/archive/v2.2.9.tar.gz -O dafoam.tar.gz
tar -xvf dafoam.tar.gz
cd dafoam-2.2.9
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

Once the installtion is complete, unset the AD environment and re-source the environment loading script. **This step is needed every time you compile an AD version of DAFoam!**

<pre>
unset WM_CODI_AD_MODE\
. $DAFOAM_ROOT_PATH/ENV_DAFOAM.sh
</pre>

## **Regression Tests**

Once DAFoam and all of its dependencies are installed, you can run the regression tests located in the `DAFoam/repos/dafoam/tests` directory. To run the cases, use the command:

<pre>
cd $HOME/dafoam/repos/dafoam/tests && ./Allrun
</pre>

If successful, the test will output the following message:

<pre>
************************************************************
**************** All DAFoam tests passed! ******************
************************************************************
</pre>

If for any reason the tests fail, check the output message to understand if the issue is due to numerical precision errors caused by differing hardware / compiler versions or if there is an issue with the installation.
## **Compile SNOPT for pyOptSparse (optional)**

This step is needed if you want to use the SNOPT optimizer. Detailed instructions are available from [pyOptSparse Documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com).

SNOPT is a commercial package, and you can purchase it from [here](http://www.sbsi-sol-optimize.com/asp/sol_snopt.htm). Once you obtain the SNOPT source code, copy all the source files (except for snopth.f) to the "$HOME/dafoam/repos/pyoptsparse-2.3.0/pyoptsparse/pySNOPT/source" folder. Then, run this command to compile pyOptSparse with SNOPT.

<pre>
cd $HOME/dafoam/repos/pyoptsparse-2.3.0 && \
pip install .
</pre>

{% include links.html %}

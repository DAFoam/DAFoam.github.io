---
title: Compile from source
keywords: dafoam, installation, compile
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_source.html
folder: mydoc
---

{% include note.html content="This section assumes you want to compile the latest DAFoam optimization package from the source on a Linux system. If you use the Docker image, there is no need to compile anything and you can skip this section. For DAFoam older versions, refer to [v2.2.0-](mydoc_installation_source_220.html) and [v1.0.0](mydoc_installation_source_100.html)." %}

The DAFoam package can be compiled with various dependency versions. Here we elaborate on how to compile it on **Ubuntu 18.04** using the dependencies shown in the following table. If you use **Ubuntu 20.04**, you can follow the same steps except that you need to change Miniconda3-4.5.4-Linux-x86_64.sh to Miniconda3-py37_4.8.3-Linux-x86_64.sh in the **Python** section.


Ubuntu | Compiler | OpenMPI | mpi4py | PETSc  | petsc4py | CGNS  | Python | Numpy  | Scipy | Cython
| :------------------------------------------------------------------------------------------------ | 
18.04  | gcc/7.5  | 1.10.4  | 3.0.2  | 3.11.4 | 3.11.0   | 3.3.0 | 3.6.5  | 1.14.3 | 1.1.0 | 0.29.21

To compile, you can just copy the code blocks in the following steps and run them on the terminal. If a code block contains multiple lines, copy all the lines and run them on the terminal. Make sure each step run successfully before going to the next one. The entire compilation may take a few hours, the most time-consuming part is to compile OpenFOAM.

## **Prerequisites**

Run this on terminal to install prerequisites:

<pre>
sudo apt-get update && \
sudo apt-get install -y build-essential flex bison cmake zlib1g-dev libboost-system-dev libboost-thread-dev libreadline-dev libncurses-dev libxt-dev freeglut3-dev texinfo libscotch-dev libcgal-dev gfortran swig wget git vim cmake-curses-gui libfl-dev apt-utils libibverbs-dev ca-certificates pkg-config --no-install-recommends
</pre>

## **Root folder**

First create a "dafoam" folder in your home directory. Then create a "loadDAFoam.sh" bash script and set up the root path $DAFOAM_ROOT_PATH. Finally, we will create the "packages", "OpenFOAM", and "repos" folders. We will compile and install everything in $DAFOAM_ROOT_PATH.

<pre>
mkdir -p $HOME/dafoam && \
mkdir -p $HOME/dafoam/packages $HOME/dafoam/OpenFOAM $HOME/dafoam/repos && \
echo '#!/bin/bash' > $HOME/dafoam/loadDAFoam.sh && \
echo '# DAFoam root path' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export DAFOAM_ROOT_PATH=$HOME/dafoam' >> $HOME/dafoam/loadDAFoam.sh && \
chmod 755 $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

## **OpenFOAM**

We need to first compile OpenFOAM-v1812 because it contains OpenMPI-1.10.4 which will be used for other packages.

<pre>
cd $HOME/dafoam/OpenFOAM && \
wget https://sourceforge.net/projects/openfoamplus/files/v1812/OpenFOAM-v1812.tgz/download -O OpenFOAM-v1812.tgz && \
wget https://sourceforge.net/projects/openfoamplus/files/v1812/ThirdParty-v1812.tgz/download -O ThirdParty-v1812.tgz && \
tar -xvf OpenFOAM-v1812.tgz && \
tar -xvf ThirdParty-v1812.tgz && \
sed -i 's/$HOME/$DAFOAM_ROOT_PATH/g' OpenFOAM-v1812/etc/bashrc && \
sed -i 's/WM_MPLIB=SYSTEMOPENMPI/WM_MPLIB=OPENMPI/g' OpenFOAM-v1812/etc/bashrc && \
sed -i 's/--enable-mpi-fortran=none/--enable-mpi-fortran=yes/g' ThirdParty-v1812/makeOPENMPI && \
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812 && \
wget https://github.com/DAFoam/files/releases/download/v1.0.0/UPstream.C && \
mv UPstream.C src/Pstream/mpi/UPstream.C && \
echo '# OpenFOAM-v1812' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedBins:$PATH' >> $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

{% include note.html content="In the above command, we replaced the OpenFOAM-v1812's built-in UPstream.C file with a customized one because we need to prevent OpenFOAM from calling the MPI_Finialize function when wrapping OpenFOAM functions using Cython." %}

{% include note.html content="The above command will compile OpenFOAM using 4 CPU cores. If you want to compile OpenFOAM using more cores, change the ``WM_NCOMPPROCS`` parameter before running ``./Allwmake``" %}

Finally, verify the installation by running:

<pre>
simpleFoam -help
</pre>

It should see some basic information of OpenFOAM

## **Python**

Install Miniconda3-4.5.4 by running this command:

<pre>
cd $HOME/dafoam/packages && \
wget https://repo.anaconda.com/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh && \
chmod 755 Miniconda3-4.5.4-Linux-x86_64.sh && \
./Miniconda3-4.5.4-Linux-x86_64.sh -b -p $HOME/dafoam/packages/miniconda3 && \
echo '# Miniconda3' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PATH=$DAFOAM_ROOT_PATH/packages/miniconda3/bin:$PATH' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAFOAM_ROOT_PATH/packages/miniconda3/lib' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PYTHONUSERBASE=no-local-libs' >> $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

In the above, we use "export PYTHONUSERBASE=no-local-libs" to bypass the site-packages in user's .local directory because they may conflict with the DAFoam packages. Then we can upgrade the pip utility:

<pre>
pip install --upgrade pip && \
pip install numpy==1.14.3 && \
pip install scipy==1.1.0 && \
pip install cython==0.29.21 && \
pip install numpy-stl==2.16.0
</pre>

## **Petsc**

First append relevant environmental variables by running:

<pre>
echo '# Petsc-3.11.4' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.11.4' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PETSC_ARCH=real-opt' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib' >> $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

Then, configure and compile:

<pre>
cd $HOME/dafoam/packages && \
wget http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/petsc-3.11.4.tar.gz  && \
tar -xvf petsc-3.11.4.tar.gz && \
cd petsc-3.11.4 && \
./configure --PETSC_ARCH=real-opt --with-scalar-type=real --with-debugging=0 --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes --download-fblaslapack=yes --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11 && \
make PETSC_DIR=$HOME/dafoam/packages/petsc-3.11.4 PETSC_ARCH=real-opt all
</pre>

Finally, install mpi4py-3.0.2 and petsc4py-3.11.0:

<pre>
cd $HOME/dafoam/packages && \
wget https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-3.0.2.tar.gz && \
tar -xvf mpi4py-3.0.2.tar.gz && cd mpi4py-3.0.2 && \
python setup.py install && \
cd $HOME/dafoam/packages && \
wget https://bitbucket.org/petsc/petsc4py/downloads/petsc4py-3.11.0.tar.gz && \
tar -xvf petsc4py-3.11.0.tar.gz && cd petsc4py-3.11.0 && \
python setup.py install
</pre>

## **CGNS**

First append relevant environmental variables by running:

<pre>
echo '# CGNS-3.3.0' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-3.3.0/opt-gfortran' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export PATH=$PATH:$CGNS_HOME/bin' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib' >> $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

Then, configure and compile:

<pre>
cd $HOME/dafoam/packages && \
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
v1.2.0      | v1.2.0   | v1.5.0 | v1.2.0     | v2.2.0 | v2.2.0        | v2.2.1  | v2.3.0      | v1.2.1 | {{ site.latest_version }}

Now run this command to install all the repos for MACH-Aero:

<pre>
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/baseclasses/archive/v1.2.0.tar.gz -O baseclasses.tar.gz && \
tar -xvf baseclasses.tar.gz && cd baseclasses-1.2.0 && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/pyspline/archive/v1.2.0.tar.gz -O pyspline.tar.gz && \
tar -xvf pyspline.tar.gz && cd pyspline-1.2.0 && \
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
make && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/pygeo/archive/v1.5.0.tar.gz -O pygeo.tar.gz && \
tar -xvf pygeo.tar.gz && cd pygeo-1.5.0 && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/multipoint/archive/v1.2.0.tar.gz -O multipoint.tar.gz && \
tar -xvf multipoint.tar.gz && cd multipoint-1.2.0 && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/pyhyp/archive/v2.2.0.tar.gz -O pyhyp.tar.gz && \
tar -xvf pyhyp.tar.gz && cd pyhyp-2.2.0 && \
cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
make && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/cgnsutilities/archive/v2.2.0.tar.gz -O cgnsutilities.tar.gz && \
tar -xvf cgnsutilities.tar.gz && cd cgnsutilities-2.2.0 && \
cp config.mk.info config.mk && \
make && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/idwarp/archive/v2.2.1.tar.gz -O idwarp.tar.gz && \
tar -xvf idwarp.tar.gz && cd idwarp-2.2.1 && \
cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
make && pip install . && \
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/pyoptsparse/archive/v2.3.0.tar.gz -O pyoptsparse.tar.gz && \
tar -xvf pyoptsparse.tar.gz && cd pyoptsparse-2.3.0 && \
pip install .
</pre>

## **pyOFM**

Compile pyOFM by running:

<pre>
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/pyofm/archive/v1.2.1.tar.gz -O pyofm.tar.gz && \
tar -xvf pyofm.tar.gz && cd pyofm-1.2.1 && \
. $HOME/dafoam/loadDAFoam.sh && \
make && pip install .
</pre>

## **DAFoam**

Compile DAFoam by running:

<pre>
cd $HOME/dafoam/repos && \
wget https://github.com/mdolab/dafoam/archive/{{ site.latest_version }}.tar.gz -O dafoam.tar.gz && \
tar -xvf dafoam.tar.gz && cd dafoam-* && \
. $HOME/dafoam/loadDAFoam.sh && \
./Allmake && pip install .
</pre>

Once DAFoam is compiled, run the regression test:

<pre>
cd $HOME/dafoam/repos/dafoam/tests && ./Allrun
</pre>

The regression tests should take less than 30 minutes. The test progress will be printed to screen. Make sure you see this at the end:

<pre>   
************************************************************
**************** All DAFoam tests passed! ******************
************************************************************
</pre>

{% include note.html content="Before running any jobs, source the loadDAFoam.sh file to load DAFoam environment!" %}

|

In summary, here is the folder structures for all the installed packages:

<pre>   
$HOME/dafoam
  loadDAFoam.sh
  - OpenFOAM
    - OpenFOAM-v1812
    - ThirdParty-v1812
  - packages
    - miniconda3
    - CGNS-3.3.0
    - petsc-3.11.4
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

The loadDAFoam.sh file should look like this:

<pre>
#!/bin/bash
# DAFoam root path
export DAFOAM_ROOT_PATH=$HOME/dafoam
# Miniconda3
export PATH=$DAFOAM_ROOT_PATH/packages/miniconda3/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAFOAM_ROOT_PATH/packages/miniconda3/lib
export PYTHONUSERBASE=no-local-libs
# PETSC
export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.11.4
export PETSC_ARCH=real-opt
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib
export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib
# CGNS-3.3.0
export CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-3.3.0/opt-gfortran
export PATH=$PATH:$CGNS_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib
# OpenFOAM-v1812
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc
export LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH
export PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedBins:$PATH
</pre>

## **Compile DAFoam with automatic differentiation (optional)**

**Build Reverse Mode AD**

This step is only needed if you want to use the Jacobian free adjoint feature (e.g., adjJacobianOption=JacobianFree) in DAFoam. If you skip this step, you have to use the default finite-difference Jacobian adjoint, i.e., adjJacobianOption=JacobianFD. Check the detail of the adjJacobianOption key on [this page](https://dafoam.github.io/doxygen/html/classdafoam_1_1pyDAFoam_1_1DAOPTION.html). Note that some derivatives, e.g., the betaSA and alphaPorosity, are only avaiable with adjJacobianOption=JacobianFree.

We need to first compile the reverse mode AD version of OpenFOAM:

<pre>
cd $HOME/dafoam/OpenFOAM && \
wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v1.2.8.tar.gz -O OpenFOAM-v1812-AD.tgz && \
tar -xvf OpenFOAM-v1812-AD.tgz && mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADR && \
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812-ADR && \
sed -i 's/WM_PROJECT_VERSION=v1812-AD/WM_PROJECT_VERSION=v1812-ADR/g' etc/bashrc && \
sed -i 's/$HOME/$DAFOAM_ROOT_PATH/g' etc/bashrc && \
sed -i 's/export WM_CODI_AD_MODE=CODI_AD_FORWARD/export WM_CODI_AD_MODE=CODI_AD_REVERSE/g' etc/bashrc && \
sed -i 's/WM_MPLIB=SYSTEMOPENMPI/WM_MPLIB=OPENMPI/g' etc/bashrc && \
source etc/bashrc && \
export WM_NCOMPPROCS=4 && \
./Allwmake 2> warningLog.txt
</pre>

Then, verify the installation by running:

<pre>
DASimpleFoamReverseAD -help
</pre>

It should see some basic information of DASimpleFoamReverseAD.

{% include note.html content="We use CodiPack to differentiate the OpenFOAM libraries. During the compliation, it will generate a lot of warning messages, which are saved to the warningLog.txt file. After the compilation is done, remember to delete this warning file, which can be larger than 1 GB." %}

After OpenFOAM-v1812-ADR is compiled and verified, we need to link all the compiled AD libraries to the original OpenFOAM-v1812 folder. Note that we need to link the relative path because we want this to be portable.

<pre>
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812/platforms/*/lib
ln -s ../../../../OpenFOAM-v1812-ADR/platforms/*/lib/*.so .
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/dummy/*.so .
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/openmpi-1.10.4
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/openmpi-1.10.4/*.so .
</pre>

Now, compile the AD version of DAFoam:

<pre>
cd $HOME/dafoam/repos/dafoam && \
./Allclean && ./Allmake 2> warningLog.txt && pip install .
</pre>

Finally, reset the AD environment, and re-source the original OpenFOAM-v1812.

<pre>
unset WM_CODI_AD_MODE && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

You are ready to use the adjJacobianOption=JacobianFree option in DAFoam.

**Build Foward Mode AD**

This step is only needed if you want to run the forward mode AD to verify adjoint sensitivity. This build is NOT needed in optimization. 

We need to first compile the forward mode AD version of OpenFOAM:

<pre>
cd $HOME/dafoam/OpenFOAM && \
wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v1.2.8.tar.gz -O OpenFOAM-v1812-AD.tgz && \
tar -xvf OpenFOAM-v1812-AD.tgz && mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADF && \
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812-ADF && \
sed -i 's/WM_PROJECT_VERSION=v1812-AD/WM_PROJECT_VERSION=v1812-ADF/g' etc/bashrc && \
sed -i 's/$HOME/$DAFOAM_ROOT_PATH/g' etc/bashrc && \
sed -i 's/WM_MPLIB=SYSTEMOPENMPI/WM_MPLIB=OPENMPI/g' etc/bashrc && \
source etc/bashrc && \
export WM_NCOMPPROCS=4 && \
./Allwmake 2> warningLog.txt
</pre>

After OpenFOAM-v1812-ADF is compiled and verified, we need to link all the compiled AD libraries to the original OpenFOAM-v1812 folder. Note that we need to link the relative path because we want this to be portable.

<pre>
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812/platforms/*/lib
ln -s ../../../../OpenFOAM-v1812-ADF/platforms/*/lib/*.so .
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/dummy/*.so .
cd $HOME/dafoam/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/openmpi-1.10.4
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/openmpi-1.10.4/*.so .
</pre>

Now, compile the AD version of DAFoam:

<pre>
cd $HOME/dafoam/repos/dafoam && \
./Allclean && ./Allmake 2> warningLog.txt && pip install .
</pre>

Finally, reset the AD environment, and re-source the original OpenFOAM-v1812.

<pre>
unset WM_CODI_AD_MODE && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

You are ready to use the forward mode AD in DAFoam.


## **Compile SNOPT and IPOPT for pyOptSparse (optional)**

This step is needed if you want to use SNOPT and IPOPT optimizers. Detailed instructions are available from [pyOptSparse Documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com).

**IPOPT**

Download Ipopt-3.13.2 and set up the relevant environmental variables to loadDAFoam.sh by runing:

<pre>
echo '# Ipopt' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export IPOPT_DIR=$DAFOAM_ROOT_PATH/packages/Ipopt' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$IPOPT_DIR/lib' >> $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

Next, compiles the ThirdParty dependencies Metis and Mumps by running:

<pre>
cd $HOME/dafoam/packages && \
git clone -b stable/3.13 https://github.com/coin-or/Ipopt.git && \
cd $IPOPT_DIR && \
git clone -b stable/2.0 https://github.com/coin-or-tools/ThirdParty-Metis.git && \
cd ThirdParty-Metis && \
./get.Metis && \
CFLAGS='-Wno-implicit-function-declaration' ./configure --prefix=$IPOPT_DIR && \
make && \
make install && \
cd $IPOPT_DIR && \
git clone -b stable/1.4 https://github.com/coin-or-tools/ThirdParty-Blas.git && \
cd ThirdParty-Blas && \
./get.Blas && \
./configure --prefix=$IPOPT_DIR && \
make && \
make install && \
cd $IPOPT_DIR && \
git clone -b stable/1.6 https://github.com/coin-or-tools/ThirdParty-Lapack.git && \
cd ThirdParty-Lapack && \
./get.Lapack && \
./configure --prefix=$IPOPT_DIR && \
make && \
make install && \
cd $IPOPT_DIR && \
git clone -b stable/2.1 https://github.com/coin-or-tools/ThirdParty-Mumps.git && \
cd ThirdParty-Mumps && \
./get.Mumps && \
./configure --prefix=$IPOPT_DIR --with-metis --with-metis-lflags="-L${PREFIX}/lib -lcoinmetis" --with-metis-cflags="-I${PREFIX}/include -I${PREFIX}/include/coin-or -I${PREFIX}/include/coin-or/metis" CFLAGS="-I${PREFIX}/include -I${PREFIX}/include/coin-or -I${PREFIX}/include/coin-or/metis" FCFLAGS="-I${PREFIX}/include -I${PREFIX}/include/coin-or -I${PREFIX}/include/coin-or/metis" --with-lapack --with-lapack-lflags="-L${IPOPT_DIR}/lib -lcoinlapack" && \
make && \
make install
</pre>

Finally, compile Ipopt and pyoptsparse by running:

<pre>
cd $IPOPT_DIR && \
mkdir build && \
cd build && \
../configure --prefix=${IPOPT_DIR} --disable-java --with-mumps --with-mumps-lflags="-L${IPOPT_DIR}/lib -lcoinmumps" --with-mumps-cflags="-I${IPOPT_DIR}/include/coin-or/mumps" --with-lapack --with-lapack-lflags="-L${IPOPT_DIR}/lib -lcoinlapack" && \
make && \
make install && \
cd $IPOPT_DIR/lib && \
ln -s libcoinlapack.so liblapack.so && \
ln -s libcoinblas.so libblas.so && \
cd $HOME/dafoam/repos/pyoptsparse-2.3.0 && pip install .
</pre>

**SNOPT**

SNOPT is a commercial package, and you can purchase it from [here](http://www.sbsi-sol-optimize.com/asp/sol_snopt.htm). Once you obtain the SNOPT source code, copy all the source files (except for snopth.f) to the "$HOME/dafoam/repos/pyoptsparse-2.3.0/pyoptsparse/pySNOPT/source" folder. Then, run this command to compile pyOptSparse with SNOPT.

<pre>
cd $HOME/dafoam/repos/pyoptsparse-2.3.0 && \
pip install .
</pre>

## **Make the DAFoam package portable (optional)**

This step is only needed if you want to change the root path of your installation, e.g., copy your compiled DAFoam packages to another directory.

The only thing you need to do is to modify the interpreter lines "#!" for files in $HOME/dafoam/packages/miniconda3/. This is because Miniconda hard codes the Python path, so we need to chagne it to "#!/usr/bin/env python"

First find an example of the hard-coded interpreter line from $HOME/dafoam/packages/miniconda3/bin/conda. Run this command

<pre>
head -1 $HOME/dafoam/packages/miniconda3/bin/conda
</pre>

You may see an output like this:

<pre>
#!/home/replace_this_with_your_username/dafoam/packages/miniconda3/bin/python
</pre>

Then run this command to replace all the hard-coded interpreter lines:

<pre>
sed -i 's,^#\!/home/replace_this_with_your_username/dafoam/packages/miniconda3/bin/python,#!/usr/bin/env python,g' $HOME/dafoam/packages/miniconda3/*/*
</pre>

Finally, you can change the DAFOAM_ROOT_PATH value (in loadDAFoam.sh) to your new directory, source the "loadDAFoam.sh" script again, and run DAFoam without compiling everything again.

{% include links.html %}

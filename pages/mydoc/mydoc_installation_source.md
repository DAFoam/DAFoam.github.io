---
title: Compile from source (Ubuntu)
keywords: dafoam, installation, compile
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_source.html
folder: mydoc
---

{% include note.html content="This section assumes you want to compile the latest DAFoam optimization package from the source on a Linux system. If you use the Docker image, there is no need to compile anything and you can skip this section. For DAFoam older versions, refer to [v3](https://dafoam.github.io/v3-pages/mydoc_installation_source.html), [v2.2.10-](mydoc_installation_source_2210.html), [v2.2.0-](mydoc_installation_source_220.html), and [v1.0.0](mydoc_installation_source_100.html)." %}

The DAFoam package can be compiled with various dependency versions. Here we elaborate on how to compile it on **Ubuntu 22.04** using the dependencies shown in the following table.


Ubuntu | Compiler | OpenMPI | mpi4py | PETSc  | petsc4py | CGNS  | Python | Numpy  | Scipy | Cython
| :------------------------------------------------------------------------------------------------ | 
22.04.2 | gcc/11.4  | 4.1.2   | 3.1.5  | 3.15.5 | 3.15.5   | 4.5.0 | 3.9    | 1.23.5 | 1.13.1 | 0.29.21

To compile, you can just copy the code blocks in the following steps and run them on the terminal. If a code block contains multiple lines, copy all the lines and run them on the terminal. Make sure each step run successfully before going to the next one. The entire compilation may take a few hours, the most time-consuming part is to compile OpenFOAM.

## **Prerequisites**

Run this on terminal to install prerequisites:

<pre>
sudo apt-get update && \
sudo apt-get install -y build-essential flex bison cmake zlib1g-dev libboost-system-dev libboost-thread-dev libreadline-dev libncurses-dev libxt-dev freeglut3-dev texinfo libscotch-dev libcgal-dev gfortran swig wget git vim cmake-curses-gui libfl-dev apt-utils libibverbs-dev ca-certificates pkg-config liblapack-dev libmetis-dev libopenmpi-dev openmpi-bin --no-install-recommends
</pre>

## **Root folder**

First, we need to create a "dafoam" folder in your home directory. Then create a "loadDAFoam.sh" bash script to set up the root path $DAFOAM_ROOT_PATH, and load loadDAFoam.sh the script:

<pre>
mkdir -p $HOME/dafoam && \
echo '#!/bin/bash' > $HOME/dafoam/loadDAFoam.sh && \
echo '# DAFoam root path' >> $HOME/dafoam/loadDAFoam.sh && \
echo 'export DAFOAM_ROOT_PATH=$HOME/dafoam' >> $HOME/dafoam/loadDAFoam.sh && \
chmod 755 $HOME/dafoam/loadDAFoam.sh && \
. $HOME/dafoam/loadDAFoam.sh
</pre>

{% include note.html content="You need to complete the following steps on the same terminal session. If you start a new terminal session, you need to load the loadDAFoam.sh script before installing DAFoam packages!" %}

Next, we will create the "packages", "OpenFOAM", and "repos" folders in $DAFOAM_ROOT_PATH.

<pre>
mkdir -p $DAFOAM_ROOT_PATH/packages $DAFOAM_ROOT_PATH/OpenFOAM $DAFOAM_ROOT_PATH/OpenFOAM/sharedBins $DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs $DAFOAM_ROOT_PATH/repos
</pre>

## **Python**

Install Miniconda3 by running this command:

<pre>
cd $DAFOAM_ROOT_PATH/packages && \
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh && \
chmod 755 Miniconda3-py39_4.12.0-Linux-x86_64.sh && \
./Miniconda3-py39_4.12.0-Linux-x86_64.sh -b -p $DAFOAM_ROOT_PATH/packages/miniconda3 && \
echo '# Miniconda3' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PATH=$DAFOAM_ROOT_PATH/packages/miniconda3/bin:$PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAFOAM_ROOT_PATH/packages/miniconda3/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PYTHONUSERBASE=no-local-libs' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

In the above, we use "export PYTHONUSERBASE=no-local-libs" to bypass the site-packages in user's .local directory because they may conflict with the DAFoam packages. 

The miniconda's built-in libstdc++ and libtinfo libs may conflict with the Ubuntu's system libs. Also, the new miniconda's compiler_compat ld may conflict with the system ld. So we need to rename the miniconda's libs and exes by running:

<pre>
mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libstdc++.so.6 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libstdc++.so.6.backup && \
mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libtinfo.so.6 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libtinfo.so.6.backup && \
mv $DAFOAM_ROOT_PATH/packages/miniconda3/compiler_compat/ld $DAFOAM_ROOT_PATH/packages/miniconda3/compiler_compat/ld.backup
</pre>

Next, we need to upgrade the pip utility and install python packages:

<pre>
pip install --upgrade pip && \
pip install numpy==1.23.5 && \
pip install scipy==1.13.1 && \
pip install mpi4py==3.1.5 && \
pip install cython==0.29.21 && \
pip install numpy-stl==2.16.0 && \
pip install pynastran==1.3.3 && \
pip install nptyping==1.4.4 && \
pip install tensorflow-cpu==2.12
</pre>

## **Petsc**

First append relevant environmental variables by running:

<pre>
echo '# Petsc' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.15.5' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PETSC_ARCH=real-opt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

Then, configure and compile:

<pre>
cd $DAFOAM_ROOT_PATH/packages && \
wget https://www.mcs.anl.gov/petsc/mirror/release-snapshots/petsc-3.15.5.tar.gz  && \
tar -xvf petsc-3.15.5.tar.gz && \
cd petsc-3.15.5 && \
./configure --PETSC_ARCH=real-opt --with-scalar-type=real --with-debugging=0 --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes --download-fblaslapack=yes --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11 && \
make PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.15.5 PETSC_ARCH=real-opt all
</pre>

Finally, install petsc4py-3.15:

<pre>
cd $PETSC_DIR/src/binding/petsc4py && \
pip install .
</pre>

## **CGNS**

First append relevant environmental variables by running:

<pre>
echo '# CGNS' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-4.5.0/opt-gfortran' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PATH=$PATH:$CGNS_HOME/bin' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

Then, configure and compile:

<pre>
cd $DAFOAM_ROOT_PATH/packages && \
wget https://github.com/CGNS/CGNS/archive/v4.5.0.tar.gz  && \
tar -xvaf v4.5.0.tar.gz && \
cd CGNS-4.5.0 && \
mkdir -p build && \
cd build && \
cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME -DCGNS_BUILD_CGNSTOOLS=0 -DCGNS_ENABLE_HDF5=OFF -DCGNS_ENABLE_64BIT=OFF -DCMAKE_C_FLAGS="-fPIC" -DCMAKE_Fortran_FLAGS="-fPIC"
&& \
make all install
</pre>

## **IPOPT**

Download Ipopt-3.13.2 and set up the relevant environmental variables to loadDAFoam.sh by running:

<pre>
echo '# Ipopt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export IPOPT_DIR=$DAFOAM_ROOT_PATH/packages/Ipopt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$IPOPT_DIR/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

Next, compiles the ThirdParty dependencies Metis and Mumps by running:

<pre>
cd $DAFOAM_ROOT_PATH/packages && \
git clone -b stable/3.13 https://github.com/coin-or/Ipopt.git && \
cd $IPOPT_DIR && \
git clone -b stable/2.1 https://github.com/coin-or-tools/ThirdParty-Mumps.git && \
cd ThirdParty-Mumps && \
./get.Mumps && \
./configure --prefix=$IPOPT_DIR && \
make && \
make install
</pre>

Finally, compile Ipopt by running:

<pre>
cd $IPOPT_DIR && \
mkdir build && \
cd build && \
../configure --prefix=${IPOPT_DIR} --disable-java --with-mumps --with-mumps-lflags="-L${IPOPT_DIR}/lib -lcoinmumps" --with-mumps-cflags="-I${IPOPT_DIR}/include/coin-or/mumps" && \
make && \
make install
</pre>

## **MACH-Aero framework**

The supported repo versions in the MACH-Aero framework for DAFoam-{{ site.latest_version }} is as follows

baseclasses | pySpline |  pyGeo  | multipoint | pyHyp  | cgnsUtilities | IDWarp  | pyOptSparse | pyOFM  | DAFoam
| :----------------------------------------------------------------------------------------------------------- | 
v1.6.1      | v1.5.2   | v1.13.0 | v1.4.0     | v2.6.1 | v2.6.0        | v2.6.2  | v2.10.1      | v1.2.2 | {{ site.latest_version }}

Now run this command to install all the repos for MACH-Aero:

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/baseclasses/archive/v1.6.1.tar.gz -O baseclasses.tar.gz && \
tar -xvf baseclasses.tar.gz && cd baseclasses-1.6.1 && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyspline/archive/v1.5.2.tar.gz -O pyspline.tar.gz && \
tar -xvf pyspline.tar.gz && cd pyspline-1.5.2 && \
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pygeo/archive/v1.13.0.tar.gz -O pygeo.tar.gz && \
tar -xvf pygeo.tar.gz && cd pygeo-1.13.0 && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/multipoint/archive/v1.4.0.tar.gz -O multipoint.tar.gz && \
tar -xvf multipoint.tar.gz && cd multipoint-1.4.0 && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/cgnsutilities/archive/v2.6.0.tar.gz -O cgnsutilities.tar.gz && \
tar -xvf cgnsutilities.tar.gz && cd cgnsutilities-2.6.0 && \
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyhyp/archive/v2.6.1.tar.gz -O pyhyp.tar.gz && \
tar -xvf pyhyp.tar.gz && cd pyhyp-2.6.1 && \
cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
sed -i "s/mpifort/mpif90/g" config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/idwarp/archive/v2.6.2.tar.gz -O idwarp.tar.gz && \
tar -xvf idwarp.tar.gz && cd idwarp-2.6.2 && \
cp -r config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
sed -i "s/mpifort/mpif90/g" config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyoptsparse/archive/v2.10.1.tar.gz -O pyoptsparse.tar.gz && \
tar -xvf pyoptsparse.tar.gz && cd pyoptsparse-2.10.1 && \
pip install .
</pre>


## **OpenFOAM**

**There are three versions of OpenFOAM to compile: original, reverse-mode AD (ADR), and forward-mode AD (ADF).** The reverse-mode AD enables the JacobianFree adjoint option, and the forward-mode AD enables the brute-force AD for verifying the adjoint accuracy.

**Build Original**

Run the following:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
wget https://sourceforge.net/projects/openfoam/files/v1812/OpenFOAM-v1812.tgz/download -O OpenFOAM-v1812.tgz && \
wget https://sourceforge.net/projects/openfoam/files/v1812/ThirdParty-v1812.tgz/download -O ThirdParty-v1812.tgz && \
tar -xvf OpenFOAM-v1812.tgz && \
tar -xvf ThirdParty-v1812.tgz && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812 && \
wget https://github.com/DAFoam/files/releases/download/v1.0.0/OpenFOAM-v1812-patch-files.tar.gz && \
tar -xvf OpenFOAM-v1812-patch-files.tar.gz && \
cd OpenFOAM-v1812-patch-files && \
./runPatch.sh && \
cd .. && \
echo '# OpenFOAM-v1812' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedBins:$PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

{% include note.html content="In the above command, we replaced some custome source files to enable Python wrapping for OpenFOAM. These patch files also make OpenFOAM-v1812 compatible with newer Gcc compilers, like Gcc 13." %}

{% include note.html content="The above command will compile OpenFOAM using 4 CPU cores. If you want to compile OpenFOAM using more cores, change the ``WM_NCOMPPROCS`` parameter before running ``./Allwmake``" %}

Finally, verify the installation by running:

<pre>
simpleFoam -help
</pre>

It should see some basic information of OpenFOAM


**Build Reverse Mode AD**

Run the following:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v1.3.2.tar.gz -O OpenFOAM-v1812-AD.tgz && \
tar -xvf OpenFOAM-v1812-AD.tgz && mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADR && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADR && \
sed -i 's/WM_PROJECT_VERSION=v1812-AD/WM_PROJECT_VERSION=v1812-ADR/g' etc/bashrc && \
sed -i 's/export WM_CODI_AD_LIB_POSTFIX=ADF/export WM_CODI_AD_LIB_POSTFIX=ADR/g' etc/bashrc && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
source etc/bashrc && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

Then, verify the installation by running:

<pre>
DASimpleFoamReverseAD -help
</pre>

It should see some basic information of DASimpleFoamReverseAD.

{% include note.html content="We use CodiPack to differentiate the OpenFOAM libraries." %}

After OpenFOAM-v1812-ADR is compiled and verified, we need to link all the compiled AD libraries to the original OpenFOAM-v1812 folder. Note that we need to link the relative path because we want this to be portable.

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib && \
ln -s ../../../../OpenFOAM-v1812-ADR/platforms/*/lib/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy && \
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/dummy/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/openmpi-system && \
ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/openmpi-system/*.so .
</pre>

**Build Forward Mode AD (Optional)**

Run the following:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v1.3.2.tar.gz -O OpenFOAM-v1812-AD.tgz && \
tar -xvf OpenFOAM-v1812-AD.tgz && mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADF && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADF && \
sed -i 's/WM_PROJECT_VERSION=v1812-AD/WM_PROJECT_VERSION=v1812-ADF/g' etc/bashrc && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
source etc/bashrc && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

After OpenFOAM-v1812-ADF is compiled and verified, we need to link all the compiled AD libraries to the original OpenFOAM-v1812 folder. Note that we need to link the relative path because we want this to be portable.

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib && \
ln -s ../../../../OpenFOAM-v1812-ADF/platforms/*/lib/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy && \
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/dummy/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/openmpi-system && \
ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/openmpi-system/*.so .
</pre>

Once done, we need to re-source the original OpenFOAM-v1812.

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

## **pyOFM**

Compile pyOFM by running:

<pre>
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyofm/archive/refs/tags/v1.2.3.tar.gz -O pyofm.tar.gz && \
tar -xvf pyofm.tar.gz && cd pyofm-* && \
make && pip install .
</pre>

## **DAFoam**

Similar to OpenFOAM, we need to compile three versions of DAFoam: original, reverse-mode AD (ADR), and forward-mode AD (ADF). It can be done by running the following commands:

<pre>
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/dafoam/archive/{{ site.latest_version }}.tar.gz -O dafoam.tar.gz && \
tar -xvf dafoam.tar.gz && cd dafoam-* && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
./Allmake
</pre>

The above command will compile the original and ADR versions of DAFoam. If you need to compile the ADF version run:

<pre>
export COMPILE_DAFOAM_ADF=1 && \
./Allmake
</pre>


{% include note.html content="Before running any jobs, source the loadDAFoam.sh file to load DAFoam environment!" %}

## **MDO packages**

To perform multidisplinary deisgn optimization, we need to install the following packages:

[OpenMDAO](https://openmdao.org) is an open-source multidisciplinary optimization framework. 

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
pip install openmdao==3.26
</pre>

[Mphys](https://github.com/OpenMDAO/mphys) is an interface that faciliate the interation between low- and high-fidelity tools within OpenMDAO.

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/OpenMDAO/mphys/archive/b6db107d05937d95a46b392b6f5759677a93e46d.tar.gz -O mphys.tar.gz && \
tar -xvf mphys.tar.gz && mv mphys-* mphys && \
cd mphys && pip install .
</pre>

[FUNtoFEM](https://github.com/smdogroup/funtofem) is a generic aeroelastic analysis and adjoint-based gradient evaluation tools.

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/smdogroup/funtofem/archive/refs/tags/v0.3.tar.gz -O funtofem.tar.gz && \
tar -xvf funtofem.tar.gz && mv funtofem-* funtofem && \
cd funtofem && cp Makefile.in.info Makefile.in && \
sed -i "s/F2F_DIR=.*/F2F_DIR=\$\{DAFOAM_ROOT_PATH\}\/repos\/funtofem/g" Makefile.in && \
make && pip install -e .
</pre>

[TACS](https://github.com/smdogroup/tacs) is a finite-element library for analysis and adjoint-based gradient evaluation

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/smdogroup/tacs/archive/refs/tags/v3.4.0.tar.gz -O tacs.tar.gz && \
tar -xvf tacs.tar.gz && mv tacs-* tacs && \
cd tacs/extern && \
wget https://github.com/DAFoam/files/releases/download/TACS_Extern/TACS_extern.tar.gz && tar -xzf TACS_extern.tar.gz && \
rm -rf metis-4.0.3* && \
wget https://github.com/DAFoam/files/releases/download/TACS_Extern/metis-5.1.0.tar.gz && \
tar -czvf TACS_extern.tar.gz metis*.tar.gz UFconfig*.tar.gz  AMD*.tar.gz &&\
tar -xzf metis*.tar.gz && \
cd metis-5.1.0 && make config prefix=$DAFOAM_ROOT_PATH/repos/tacs/extern/metis/ CFLAGS="-fPIC" && make install && \
cd ../../ && \
cp Makefile.in.info Makefile.in && \
ls && \
sed -i "s/TACS_DIR\ =.*/TACS_DIR=\$\{DAFOAM_ROOT_PATH\}\/repos\/tacs/g" Makefile.in && \
make && pip install -e . && \
cd extern/f5tovtk && make && cp f5tovtk $DAFOAM_ROOT_PATH/OpenFOAM/sharedBins
</pre>

## **DAFoam regression tests**

To verify the DAFoam installation, you can run the regression tests:

<pre>
cd $DAFOAM_ROOT_PATH/repos/dafoam-*/tests && ./Allrun
</pre>

The regression tests should take less than 30 minutes. The test progress will be printed to screen. Make sure you see this at the end:

<pre>   
*** All Tests Passed! ***
</pre>

|

In summary, here is the folder structures for all the installed packages:

<pre>
$HOME/dafoam
  loadDAFoam.sh
  - OpenFOAM
    - OpenFOAM-v1812
    - OpenFOAM-v1812-ADF
    - OpenFOAM-v1812-ADR
    - ThirdParty-v1812
    - sharedBins
    - sharedLibs
  - packages
    - Ipopt
    - miniconda3
    - CGNS-4.5.0
    - petsc-3.15.5
  - repos
    - baseclasses
    - cgnsutilities
    - dafoam
    - funtofem
    - idwarp
    - multipoint
    - mphys
    - pygeo
    - pyhyp
    - pyofm
    - pyoptsparse
    - pyspline
    - tacs
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
export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.15.5
export PETSC_ARCH=real-opt
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib
export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib
# CGNS
export CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-4.5.0/opt-gfortran
export PATH=$PATH:$CGNS_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib
# Ipopt
export IPOPT_DIR=$DAFOAM_ROOT_PATH/packages/Ipopt
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$IPOPT_DIR/lib
# OpenFOAM-v1812
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/etc/bashrc
export LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH
export PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedBins:$PATH
</pre>

## **Compile Hisa4DAFoam (optional)**

DAFoam integrates a density-based, high-speed aerodynamic CFD solver [Hisa](https://hisa.gitlab.io/index.html). We have adopted the original Hisa solver into a DAFoam compatible lib called Hisa4DAFoam. Run the following command to install the Hisa4DAFoam dependency: 

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
wget https://github.com/DAFoam/Hisa4DAFoam/archive/refs/tags/v1.0.tar.gz -O Hisa4DAFoam.tar.gz && \
tar -xvf Hisa4DAFoam.tar.gz && \
mv Hisa4DAFoam-* Hisa4DAFoam && \
cd Hisa4DAFoam && \
./Allmake
</pre>

You should see "Build Successful!" at the end of the compilation. Once Hisa4DAFoam is compiled, you need to recompile the DAFoam repo in repos/dafoam to make sure everything is up-to-date.

***NOTE: The solver is called DAHisaFoam and is in a beta state.*** It is not supported by v4.0.2. Instead, you need to use the latest version of the DAFoam repo. We currently have two tutorials: supersonic, Euler flow optimization for a [cone](https://github.com/DAFoam/tutorials/tree/main/Cone_Supersonic) and a transonic, RANS flow optimization for [RAE2822 airfoil](https://github.com/DAFoam/tutorials/tree/main/RAE2822_Airfoil). Only the JST flux scheme is supported. Other schemes, such as AUSMPlusUp, may have adjoint convergence issues.

## **Compile SNOPT for pyOptSparse (optional)**

This step is needed if you want to use the SNOPT optimizer. Detailed instructions are available from [pyOptSparse Documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com).

SNOPT is a commercial package, and you can purchase it from [here](http://www.sbsi-sol-optimize.com/asp/sol_snopt.htm). Once you obtain the SNOPT source code, copy all the source files (except for snopth.f) to the "$DAFOAM_ROOT_PATH/repos/pyoptsparse-2.10.1/pyoptsparse/pySNOPT/source" folder. Then, run this command to compile pyOptSparse with SNOPT.

<pre>
cd $DAFOAM_ROOT_PATH/repos/pyoptsparse-2.10.1 && \
pip install .
</pre>


## **Make the DAFoam package portable (optional)**

This step is only needed if you want to change the root path of your installation, e.g., copy your compiled DAFoam packages to another directory.

The only thing you need to do is to modify the interpreter lines "#!" for files in $DAFOAM_ROOT_PATH/packages/miniconda3/. This is because Miniconda hard codes the Python path, so we need to chagne it to "#!/usr/bin/env python"

First find an example of the hard-coded interpreter line from $DAFOAM_ROOT_PATH/packages/miniconda3/bin/conda. Run this command

<pre>
head -1 $DAFOAM_ROOT_PATH/packages/miniconda3/bin/conda
</pre>

You may see an output like this:

<pre>
#!/home/replace_this_with_your_username/dafoam/packages/miniconda3/bin/python
</pre>

Then run this command to replace all the hard-coded interpreter lines:

<pre>
sed -i 's,^#\!/home/replace_this_with_your_username/dafoam/packages/miniconda3/bin/python,#!/usr/bin/env python,g' $DAFOAM_ROOT_PATH/packages/miniconda3/*/*
</pre>

Finally, you can change the DAFOAM_ROOT_PATH value (in loadDAFoam.sh) to your new directory, source the "loadDAFoam.sh" script again, and run DAFoam without compiling everything again.

{% include links.html %}

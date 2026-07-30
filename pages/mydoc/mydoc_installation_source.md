---
title: Compile from source (Gcc)
keywords: dafoam, installation, compile
summary: 
sidebar: mydoc_sidebar
permalink: installation-source.html
folder: mydoc
---

{% include note.html content="This section assumes you want to compile the latest DAFoam optimization package from the source on a Linux system. If you use the Docker image, there is no need to compile anything and you can skip this section. For DAFoam older versions, refer to [v4](https://dafoam.github.io/v4-pages/mydoc_installation_source.html), [v3](https://dafoam.github.io/v3-pages/mydoc_installation_source.html), [v2.2.10-](installation-source-2210.html), [v2.2.0-](installation-source-220.html), and [v1.0.0](installation-source-100.html)." %}

The DAFoam package can be compiled with various versions of its dependencies. Here we elaborate on how to compile it on a workstation with Ubuntu 24.04 and two different HPC clusters.

**Workstation** uses the Ubuntu 24.04 system with the following compiler versions.

Compiler | OpenMPI | Cmake |
| :------------------------| 
gcc/13.3 | 4.1.6   | 3.28  |

**TACC-Stampede3 HPC** uses the Rocky Linux 9.5 system with the following compiler versions.

Compiler | OpenMPI | Cmake |
| :------------------------| 
gcc/13.2 | 5.0.8   |  3.28 |

**ISU Nova HPC** uses the RedHat Linux 9.4 system with the following compiler versions.

Compiler | OpenMPI | Cmake |
| :------------------------| 
gcc/12.2 | 4.1.5   |  3.26 |

To compile, you can just copy the code blocks in the following steps and run them on the terminal. If a code block contains multiple lines, copy all the lines and run them on the terminal. Make sure each step run successfully before going to the next one. The entire compilation may take a few hours; the most time-consuming part is compiling OpenFOAM.

## **Prerequisites (Ubuntu only)**

If you use Ubuntu, run this on the terminal to install prerequisites. If you install DAFoam on an HPC, skip this step.

<pre>
sudo apt-get update && \
sudo apt-get install -y --no-install-recommends build-essential ca-certificates cmake flex bison libfl-dev libcgal-dev libopenmpi-dev openmpi-bin libscotch-dev libreadline-dev libncurses-dev sudo wget vim git lcov patchelf pkg-config swig gfortran libxrender1 libxml2-dev libegl1 curl
</pre>

The following installation steps should work for both Ubuntu 24.04 and the HPC clusters.

## **Root folder**

Run the following commands to create a root folder and a few subfolders where DAFoam's modules will be installed into. The default is \$HOME/dafoam, and you can change to a different path by modifying the first line. We suggest you reserve at least 5 Gb hard disk space for the DAFoam installation. Here "loadDAFoam.sh" is a bash script to load the DAFoam environment, and we will add more modules into loadDAFoam.sh later. 

<pre>
export DAFOAM_ROOT_PATH=$HOME/dafoam
mkdir -p "$DAFOAM_ROOT_PATH" && \
cd "$DAFOAM_ROOT_PATH" && \
echo '#!/bin/bash' > loadDAFoam.sh && \
echo '# DAFoam root path' >> loadDAFoam.sh && \
echo "export DAFOAM_ROOT_PATH=$DAFOAM_ROOT_PATH" >> loadDAFoam.sh && \
chmod 755 loadDAFoam.sh && \
. ./loadDAFoam.sh && \
mkdir -p $DAFOAM_ROOT_PATH/packages $DAFOAM_ROOT_PATH/OpenFOAM $DAFOAM_ROOT_PATH/OpenFOAM/sharedBins $DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs $DAFOAM_ROOT_PATH/repos
</pre>

{% include note.html content="You need to complete the following steps on the same terminal session. If you start a new terminal session, you need to load the loadDAFoam.sh script before installing DAFoam packages!" %}

## **Python**

Install Miniconda3 by running this command:

<pre>
cd $DAFOAM_ROOT_PATH/packages && \
wget https://repo.anaconda.com/miniconda/Miniconda3-py312_26.1.1-1-Linux-x86_64.sh && \
chmod 755 Miniconda3-py312_26.1.1-1-Linux-x86_64.sh && \
bash ./Miniconda3-py312_26.1.1-1-Linux-x86_64.sh -b -p $DAFOAM_ROOT_PATH/packages/miniconda3 && \
echo '# Miniconda3' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PATH=$DAFOAM_ROOT_PATH/packages/miniconda3/bin:$PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAFOAM_ROOT_PATH/packages/miniconda3/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PYTHONUSERBASE=no-local-libs' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

In the above, we use "export PYTHONUSERBASE=no-local-libs" to bypass the site-packages in your `.local` directory, as they may conflict with the DAFoam packages. 

The miniconda's built-in libstdc++ and libtinfo libs may conflict with the system libs. Also, the new miniconda's compiler_compat ld may conflict with the system ld. So we need to rename the miniconda's libs and exes by running:

<pre>
mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libstdc++.so.6 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libstdc++.so.6.backup && \
mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libtinfo.so.6 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libtinfo.so.6.backup && \
mv $DAFOAM_ROOT_PATH/packages/miniconda3/compiler_compat/ld $DAFOAM_ROOT_PATH/packages/miniconda3/compiler_compat/ld.backup && \
mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libgcc_s.so.1 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libgcc_s.so.1.backup && \
mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libquadmath.so.0 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libquadmath.so.0.backup
</pre>

Next, we need to upgrade the pip utility and install Python packages:

<pre>
pip install --upgrade pip && \
pip install numpy==2.3.5 scipy==1.17.1 mpi4py==4.1.1 cython==3.0.5 numpy-stl==2.16.0 imageio==2.37.4 nptyping==1.4.4 tensorflow-cpu==2.21 coverage==7.11.0 fastmcp==2.13.2 vtk==9.5.2 trame==3.12.0 trame-vuetify==3.2.0 trame-vtk==2.10.0
</pre>

## **Petsc**

First, append relevant environmental variables by running:

<pre>
echo '# Petsc' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.21.6' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PETSC_ARCH=real-opt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

Then, configure and compile:

<pre>
cd $DAFOAM_ROOT_PATH/packages && \
wget https://web.cels.anl.gov/projects/petsc/download/release-snapshots/petsc-3.21.6.tar.gz  && \
tar -xvf petsc-3.21.6.tar.gz && \
cd petsc-3.21.6 && \
./configure --PETSC_ARCH=real-opt --with-scalar-type=real --with-debugging=0 --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes --download-fblaslapack=yes --download-f2cblaslapack=yes --with-shared-libraries=yes --with-fortran-bindings=1 --with-cxx-dialect=C++11 && \
make PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.21.6 PETSC_ARCH=real-opt all
</pre>

Finally, install petsc4py:

<pre>
cd $PETSC_DIR/src/binding/petsc4py && \
pip install . --no-build-isolation
</pre>

## **CGNS**

First, append relevant environmental variables by running:

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
cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME -DCGNS_BUILD_CGNSTOOLS=0 -DCGNS_ENABLE_HDF5=OFF -DCGNS_ENABLE_64BIT=OFF -DCMAKE_C_FLAGS="-fPIC" -DCMAKE_Fortran_FLAGS="-fPIC" && \
make all install
</pre>

## **MACH-Aero framework**

The supported repo versions in the MACH-Aero framework for DAFoam-{{ site.latest_version }} is as follows

baseclasses | pySpline |  pyGeo  | multipoint | pyHyp  | cgnsUtilities | IDWarp  | pyOptSparse | pyOFM  | DAFoam
| :----------------------------------------------------------------------------------------------------------- | 
v1.9.0      | v1.5.4   | v1.17.0 | v1.4.2     | v2.6.3 | v2.9.0        | v2.6.4  | v2.16.0      | v1.2.3 | {{ site.latest_version }}

Now run this command to install all the repos for MACH-Aero:

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/baseclasses/archive/v1.9.0.tar.gz -O baseclasses.tar.gz && \
tar -xvf baseclasses.tar.gz && cd baseclasses-1.9.0 && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyspline/archive/v1.5.4.tar.gz -O pyspline.tar.gz && \
tar -xvf pyspline.tar.gz && cd pyspline-1.5.4 && \
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pygeo/archive/v1.17.0.tar.gz -O pygeo.tar.gz && \
tar -xvf pygeo.tar.gz && cd pygeo-1.17.0 && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/multipoint/archive/v1.4.2.tar.gz -O multipoint.tar.gz && \
tar -xvf multipoint.tar.gz && cd multipoint-1.4.2 && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/cgnsutilities/archive/v2.9.0.tar.gz -O cgnsutilities.tar.gz && \
tar -xvf cgnsutilities.tar.gz && cd cgnsutilities-2.9.0 && \
cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyhyp/archive/v2.6.3.tar.gz -O pyhyp.tar.gz && \
tar -xvf pyhyp.tar.gz && cd pyhyp-2.6.3 && \
cp -r config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
sed -i "s/mpifort/mpif90/g" config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/idwarp/archive/v2.6.4.tar.gz -O idwarp.tar.gz && \
tar -xvf idwarp.tar.gz && cd idwarp-2.6.4 && \
cp -r config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
sed -i "s/mpifort/mpif90/g" config/config.mk && \
make && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/prefoil/archive/v2.0.1.tar.gz -O prefoil.tar.gz && \
tar -xvf prefoil.tar.gz && cd prefoil-2.0.1 && \
pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/mdolab/pyoptsparse/archive/v2.16.0.tar.gz -O pyoptsparse.tar.gz && \
tar -xvf pyoptsparse.tar.gz && cd pyoptsparse-2.16.0 && \
pip install .
</pre>

## **Surrogate Modeling Toolbox (SMT)**

Install SMT for surrogate-based optimization:

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/SMTorg/smt/archive/refs/tags/v2.10.1.tar.gz && \
tar -xvf v2.10.1.tar.gz && \
cd smt-2.10.1 && \
pip install .
</pre>

## **Uno and Egor optimizers**

Uno and Egor are open-source optimizers for gradient-based and gradient-free optimization. To install them, run:

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
pip install egobox==0.37.6 && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/LSDOlab/modopt/archive/refs/tags/v0.3.0.tar.gz -O modopt.tar.gz && \
tar -xvf modopt.tar.gz && mv modopt-* modopt && rm -rf modopt.tar.gz && \
cd modopt && pip install . && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/cvanaret/Uno/archive/7481abe47cec45e0e91ac73ccc2461c17e68f84c.tar.gz -O Uno.tar.gz && \
tar -xvf Uno.tar.gz && mv Uno-* Uno && rm -rf Uno.tar.gz && cd Uno && \
sed -i '175i\      Logger::flush();' uno/tools/Statistics.cpp && \
sed -i '159i\      Logger::flush();' uno/tools/Statistics.cpp && \
sed -i '143i\      Logger::flush();' uno/tools/Statistics.cpp && \
./dependencies/scripts/download_dependencies.sh && \
pip install --force-reinstall --no-deps -v .
</pre>

The current Uno version writes the optimization log file only after the optimization finishes. The `sed` commands above insert `Logger::flush()` calls so Uno writes the optimization log to disk immediately.

## **OpenVSP**

This step is needed if you want to use OpenVSP for geometry parameterization. Here we build the OpenVSP without GUI, only the vspscript and its Python API. Use the following commands.

**IMPORTANT**: (1) The Python API depends on swig. So, if you build it on the HPC, you may need to load the swig module. (2) there is a bug in the recent version of OpenVSP that will cause seg fault when perturbing a small step (e.g., 1e-6) for parameter such as camber for the surface geometry. Version 3.42.3 is the latest working version. (3) there is a bug in the fitCST API for 3.42.3, which has been fixed in the later version of OpenVSP. Here, we have applied the bug fix through the `sed` line. (4) OpenVSP does not compile with Gcc 11 or 12.

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/packages && \
mkdir OpenVSP && cd OpenVSP && \
mkdir build buildlibs && \
wget https://github.com/OpenVSP/OpenVSP/archive/refs/tags/OpenVSP_3.42.3.tar.gz && \
tar -xvf OpenVSP_3.42.3.tar.gz && mv OpenVSP-* repo && rm -rf OpenVSP_3.42.3.tar.gz && \
sed -i '5352,5357s/ ||$/ \&\&/;6452,6457s/ ||$/ \&\&/' repo/src/geom_api/VSP_Geom_API.cpp && \
cd buildlibs && \
cmake -DVSP_NO_GRAPHICS=ON -DVSP_USE_SYSTEM_ADEPT2=false -DVSP_USE_SYSTEM_CLIPPER2=false -DVSP_USE_SYSTEM_CMINPACK=false -DVSP_USE_SYSTEM_CODEELI=false -DVSP_USE_SYSTEM_CPPTEST=false -DVSP_USE_SYSTEM_DELABELLA=false -DVSP_USE_SYSTEM_EIGEN=false -DVSP_USE_SYSTEM_EXPRPARSE=false -DVSP_USE_SYSTEM_FLTK=false -DVSP_USE_SYSTEM_GLEW=false -DVSP_USE_SYSTEM_GLM=false -DVSP_USE_SYSTEM_LIBIGES=false -DVSP_USE_SYSTEM_LIBXML2=true -DVSP_USE_SYSTEM_OPENABF=false -DVSP_USE_SYSTEM_PINOCCHIO=false -DVSP_USE_SYSTEM_STEPCODE=false -DVSP_USE_SYSTEM_TRIANGLE=false ../repo/Libraries -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx && \
make -j4 && \
cd ../build && \
cmake ../repo/src/ -DVSP_LIBRARY_PATH=$DAFOAM_ROOT_PATH/packages/OpenVSP/buildlibs -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DVSP_NO_GRAPHICS=ON && \
make -j4 && \
cd python_pseudo && pip install ./utilities ./degen_geom ./openvsp_config ./openvsp && \
echo '# OpenVSP' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PATH=$PATH:$DAFOAM_ROOT_PATH/packages/OpenVSP/build/vsp' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh
</pre>

## **OpenFOAM**

**There are three versions of OpenFOAM to compile: original, reverse-mode AD (ADR), and forward-mode AD (ADF).** The reverse-mode AD enables the JacobianFree adjoint option, and the forward-mode AD enables the brute-force AD for verifying the adjoint accuracy.

**Build Original**

Run the following:

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
wget https://sourceforge.net/projects/openfoam/files/v2506/OpenFOAM-v2506.tgz/download -O OpenFOAM-v2506.tgz && \
wget https://sourceforge.net/projects/openfoam/files/v2506/ThirdParty-v2506.tgz/download -O ThirdParty-v2506.tgz && \
tar -xvf OpenFOAM-v2506.tgz && \
tar -xvf ThirdParty-v2506.tgz && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506 && \
wget https://github.com/DAFoam/files/releases/download/v1.0.0/UPstream_OF2506_Patch.C && \
mv UPstream_OF2506_Patch.C src/Pstream/mpi && \
echo '# OpenFOAM-v2506' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/etc/bashrc' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
echo 'export PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedBins:$PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
export WM_QUIET=true && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

{% include note.html content="The above command will compile OpenFOAM using 4 CPU cores. If you want to compile OpenFOAM using more cores, change the ``WM_NCOMPPROCS`` parameter before running ``./Allwmake``" %}

Finally, verify the installation by running:

<pre>
simpleFoam -help
</pre>

It should see some basic information about OpenFOAM


**Build Reverse Mode AD**

Run the following:

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
wget https://github.com/DAFoam/OpenFOAM-AD/archive/refs/heads/v2506-ad.tar.gz -O OpenFOAM-AD.tgz && \
tar -xvf OpenFOAM-AD.tgz && mv OpenFOAM-AD-* OpenFOAM-AD && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-AD && \
sed -i 's/export WM_AD_MODE=.*/export WM_AD_MODE=ADR/g' etc/bashrc && \
source etc/bashrc && \
export WM_QUIET=true && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

Then, verify the installation by running:

<pre>
simpleFoamADR -help
</pre>

It should see some basic information about simpleFoamADR.

{% include note.html content="We use CodiPack to differentiate the OpenFOAM libraries." %}

After the ADR is compiled and verified, we need to link all the compiled AD libraries to the original OpenFOAM-v2506 folder. Note that we need to link the relative path so that this is portable.

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM-AD && \
./renameAD.sh platforms/linux*ADR --ADR --commit && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/platforms/*/lib && \
ln -s ../../../../OpenFOAM-AD/platforms/linux*ADR/lib/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/platforms/*/lib/dummy && \
ln -s ../../../../../OpenFOAM-AD/platforms/linux*ADR/lib/dummy/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/platforms/*/lib/$FOAM_MPI && \
ln -s ../../../../../OpenFOAM-AD/platforms/linux*ADR/lib/$FOAM_MPI/*.so .
</pre>

**Build Forward Mode AD (Optional)**

This is needed only if you want to compare the adjoint derivatives with forward AD. We must compile the ADR version first! After that, run the following:

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-AD && \
sed -i 's/export WM_AD_MODE=.*/export WM_AD_MODE=ADF/g' etc/bashrc && \
source etc/bashrc && \
export WM_QUIET=true && \
export WM_NCOMPPROCS=4 && \
./Allwmake
</pre>

After DF is compiled and verified, we need to link all the compiled AD libraries to the original OpenFOAM-v2506 folder. Note that we need to link the relative path so that this is portable.

<pre>
cd $DAFOAM_ROOT_PATH/OpenFOAM-AD && \
./renameAD.sh platforms/linux*ADF --ADF --commit && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/platforms/*/lib && \
ln -s ../../../../OpenFOAM-AD/platforms/linux*ADF/lib/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/platforms/*/lib/dummy && \
ln -s ../../../../../OpenFOAM-AD/platforms/linux*ADF/lib/dummy/*.so . && \
cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/platforms/*/lib/$FOAM_MPI && \
ln -s ../../../../../OpenFOAM-AD/platforms/linux*ADF/lib/$FOAM_MPI/*.so .
</pre>

Once done, we need to re-source the original OpenFOAM-v2506.

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

## **Hisa4DAFoam**

DAFoam integrates a density-based, high-speed aerodynamic CFD solver [Hisa](https://hisa.gitlab.io/index.html). We have adopted the original Hisa solver into a DAFoam-compatible lib called Hisa4DAFoam. Run the following command to install the Hisa4DAFoam dependency: 

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/OpenFOAM && \
git clone https://github.com/DAFoam/Hisa4DAFoam && \
cd Hisa4DAFoam && \
./Allmake
</pre>

You should see "Build Successful!" at the end of the compilation. ***NOTE: The solver is called DAHisaFoam and is in a beta state.***

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

To perform multidisciplinary design optimization, we need to install the following packages:

[OpenMDAO](https://openmdao.org) is an open-source multidisciplinary optimization framework. 

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
pip install openmdao==3.45
</pre>

[Mphys](https://github.com/OpenMDAO/mphys) is an interface that facilitates the interaction between low- and high-fidelity tools within OpenMDAO.

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/OpenMDAO/mphys/archive/2080c39e86eee4c7069a41898181fb0e92cd4b93.tar.gz -O mphys.tar.gz && \
tar -xvf mphys.tar.gz && mv mphys-* mphys && \
cd mphys && pip install .
</pre>

[FUNtoFEM](https://github.com/smdogroup/funtofem) is a generic aeroelastic analysis and adjoint-based gradient evaluation tool.

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/smdogroup/funtofem/archive/refs/tags/v0.3.12.tar.gz -O funtofem.tar.gz && \
tar -xvf funtofem.tar.gz && mv funtofem-* funtofem && \
cd funtofem && cp Makefile.in.info Makefile.in && \
sed -i "s/F2F_DIR=.*/F2F_DIR=\$\{DAFOAM_ROOT_PATH\}\/repos\/funtofem/g" Makefile.in && \
sed -i "s/LAPACK_LIBS\ =.*/LAPACK_LIBS=-L\$\{PETSC_LIB\}\ -lf2clapack -lf2cblas/g" Makefile.in && \
make && pip install -e . --no-build-isolation
</pre>

[TACS](https://github.com/smdogroup/tacs) is a finite-element library for analysis and adjoint-based gradient evaluation

<pre>
. $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
cd $DAFOAM_ROOT_PATH/repos && \
wget https://github.com/smdogroup/pyNastran/archive/c9b8c2ee7e6fa452622ef10b5bb218ee02595583.tar.gz -O pyNastran.tar.gz && \
tar -xvf pyNastran.tar.gz && mv pyNastran-* pyNastran && \
cd pyNastran && pip install . && cd .. && \
wget https://github.com/smdogroup/tacs/archive/refs/tags/v3.9.2.tar.gz -O tacs.tar.gz && \
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
sed -i "s/LAPACK_LIBS\ =.*/LAPACK_LIBS=-L\$\{PETSC_LIB\}\ -lf2clapack -lf2cblas -lpthread/g" Makefile.in && \
make && pip install -e . --no-build-isolation && \
cd extern/f5tovtk && make && cp f5tovtk $DAFOAM_ROOT_PATH/OpenFOAM/sharedBins
</pre>

## **DAFoam regression tests**

To verify the DAFoam installation, you can run the regression tests:

<pre>
cd $DAFOAM_ROOT_PATH/repos/dafoam-*/tests && ./Allrun
</pre>

The regression tests should take less than 30 minutes. The test progress will be printed to the screen. Make sure you see this at the end:

<pre>   
*** All Tests Passed! ***
</pre>

|

In summary, here is the folder structure for all the installed packages:

<pre>
$HOME/dafoam
  loadDAFoam.sh
  - OpenFOAM
    - OpenFOAM-v2506
    - OpenFOAM-AD
    - ThirdParty-v2506
    - sharedBins
    - sharedLibs
  - packages
    - miniconda3
    - CGNS-4.5.0
    - OpenVSP
    - petsc-3.21.6
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
export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-3.21.6
export PETSC_ARCH=real-opt
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib
export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib
# CGNS
export CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-4.5.0/opt-gfortran
export PATH=$PATH:$CGNS_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib
# OpenFOAM-v2506
source $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v2506/etc/bashrc
export LD_LIBRARY_PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs:$LD_LIBRARY_PATH
export PATH=$DAFOAM_ROOT_PATH/OpenFOAM/sharedBins:$PATH
</pre>

## **Compile other optimizers for pyOptSparse (optional)**

This step is needed if you want to use the SNOPT optimizer. Detailed instructions are available from [pyOptSparse Documentation](https://mdolab-pyoptsparse.readthedocs-hosted.com).

SNOPT is a commercial package, and you can purchase it from [here](http://www.sbsi-sol-optimize.com/asp/sol_snopt.htm). Once you obtain the SNOPT source code, copy all the source files (except for snopth.f) to the "$DAFOAM_ROOT_PATH/repos/pyoptsparse-2.16.1/pyoptsparse/pySNOPT/source" folder. Then, run this command to compile pyOptSparse with SNOPT.

<pre>
cd $DAFOAM_ROOT_PATH/repos/pyoptsparse-2.16.1 && \
pip install .
</pre>

If you are provided a precompiled library for SNOPT instead of the source codes, refer to this [post](https://github.com/mdolab/dafoam/discussions/998#discussioncomment-17390364).

If you want to compile ParOpt for pyOptSparse, refer to this [post](https://github.com/mdolab/dafoam/discussions/138#discussioncomment-17646208)

{% include links.html %}

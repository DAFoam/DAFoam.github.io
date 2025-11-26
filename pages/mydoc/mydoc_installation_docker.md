---
title: Build Docker images
keywords: dafoam, installation, docker
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_installation_docker.html
folder: mydoc
---

## Build based on existing Docker images

The following is an example of how to update the DAFoam repo from an existing Docker image and save it as a new Docker image. First, create a file called **Dockerfile**, copy and paste the following commands into Dockerfile, and run `docker build -t my_new_dafoam_image_name .`. Here "dafoam/opt-packages:latest" can be any existing Docker image. 

<pre>
FROM dafoam/opt-packages:latest

# Swith to dafoamuser
USER dafoamuser

# compile
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    rm -rf dafoam && \
    git clone https://github.com/mdolab/dafoam && \
    cd dafoam && \
    export export COMPILE_DAFOAM_ADF=1 && \
    ./Allmake
</pre>

## Build Docker images from scratch

If you want to compile DAFoam and its dependencies from scratch, use the following Dockerfile.

<pre>
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=UTC

# Tunable versions (match the DAFoam docs v4.0.3)
ARG DAFOAM_VER=4.0.3
ARG PETSC_VER=3.15.5
ARG CGNS_VER=4.5.0
ARG BASECLASSES_VER=1.6.1
ARG PY_SPLINE_VER=1.5.2
ARG PY_GEO_VER=1.13.0
ARG MULTIPOINT_VER=1.4.0
ARG PY_HYP_VER=2.6.1
ARG CGNS_UTILS_VER=2.6.0
ARG IDWARP_VER=2.6.2
ARG PYOPTSPARSE_VER=2.10.1
ARG PYOFM_VER=1.2.3
ARG PREFOIL_VER=2.0.1
ARG OPENFOAM_AD_TAG=1.3.2
ARG OPENMDAO_VER=3.26
ARG MPHYS_HASH=b6db107d05937d95a46b392b6f5759677a93e46d
ARG FUNTOFEM_VER=0.3
ARG TACS_VER=3.4.0

# Build toggles
ARG MAKE_JOBS=4
ARG BUILD_ADF=false   # set to true to also build ADF
ARG BUILD_IPOPT=true  # set to false if providing your own IPOPT
ARG BUILD_HISA=true   # set to true to build Hisa4DAFoam high-speed solver

# Use bash for RUN steps (we need `source`)
SHELL ["/bin/bash", "-lc"]

# System prerequisites (from docs - Ubuntu 22.04)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tzdata ca-certificates apt-utils \
    build-essential flex bison cmake cmake-curses-gui \
    zlib1g-dev libboost-system-dev libboost-thread-dev \
    libreadline-dev libncurses-dev libxt-dev freeglut3-dev \
    texinfo libscotch-dev libcgal-dev gfortran swig wget git vim \
    libfl-dev libibverbs-dev pkg-config liblapack-dev libmetis-dev \
    libopenmpi-dev openmpi-bin && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user with home
RUN useradd -m -s /bin/bash dafoamuser
USER dafoamuser
WORKDIR /home/dafoamuser

# Root folder + env script
RUN mkdir -p /home/dafoamuser/dafoam && \
    echo '#!/bin/bash' > /home/dafoamuser/dafoam/loadDAFoam.sh && \
    echo '# DAFoam root path' >> /home/dafoamuser/dafoam/loadDAFoam.sh && \
    echo 'export DAFOAM_ROOT_PATH=$HOME/dafoam' >> /home/dafoamuser/dafoam/loadDAFoam.sh && \
    chmod 755 /home/dafoamuser/dafoam/loadDAFoam.sh && \
    . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    mkdir -p $DAFOAM_ROOT_PATH/packages $DAFOAM_ROOT_PATH/OpenFOAM \
             $DAFOAM_ROOT_PATH/OpenFOAM/sharedBins $DAFOAM_ROOT_PATH/OpenFOAM/sharedLibs \
             $DAFOAM_ROOT_PATH/repos

# ---------------------------
# Python (Miniconda, pinned to py310 per docs)
# ---------------------------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/packages && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh && \
    chmod 755 Miniconda3-py310_22.11.1-1-Linux-x86_64.sh && \
    bash ./Miniconda3-py310_22.11.1-1-Linux-x86_64.sh -b -p $DAFOAM_ROOT_PATH/packages/miniconda3 && \
    echo '# Miniconda3' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export PATH=$DAFOAM_ROOT_PATH/packages/miniconda3/bin:$PATH' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAFOAM_ROOT_PATH/packages/miniconda3/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export PYTHONUSERBASE=no-local-libs' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    . $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    # Avoid conda lib/tool conflicts per docs
    mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libstdc++.so.6 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libstdc++.so.6.backup && \
    mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libtinfo.so.6 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libtinfo.so.6.backup && \
    mv $DAFOAM_ROOT_PATH/packages/miniconda3/compiler_compat/ld $DAFOAM_ROOT_PATH/packages/miniconda3/compiler_compat/ld.backup && \
    mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libgcc_s.so.1 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libgcc_s.so.1.backup && \
    mv $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libquadmath.so.0 $DAFOAM_ROOT_PATH/packages/miniconda3/lib/libquadmath.so.0.backup && \
    # Python pkgs (pin exact versions from docs)
    pip install --upgrade pip && \
    pip install numpy==1.23.5 scipy==1.13.1 mpi4py==3.1.5 cython==0.29.21 \
                numpy-stl==2.16.0 pynastran==1.3.3 nptyping==1.4.4 tensorflow-cpu==2.12

# -------------
# PETSc + p4py
# -------------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    echo '# Petsc' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo "export PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-${PETSC_VER}" >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export PETSC_ARCH=real-opt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PETSC_DIR/$PETSC_ARCH/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export PETSC_LIB=$PETSC_DIR/$PETSC_ARCH/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    . $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/packages && \
    wget https://www.mcs.anl.gov/petsc/mirror/release-snapshots/petsc-${PETSC_VER}.tar.gz && \
    tar -xf petsc-${PETSC_VER}.tar.gz && \
    cd petsc-${PETSC_VER} && \
    ./configure --PETSC_ARCH=real-opt --with-scalar-type=real --with-debugging=0 \
                --download-metis=yes --download-parmetis=yes --download-superlu_dist=yes \
                --download-fblaslapack=yes --download-f2cblaslapack=yes --with-shared-libraries=yes \
                --with-fortran-bindings=1 --with-cxx-dialect=C++11 && \
    make PETSC_DIR=$DAFOAM_ROOT_PATH/packages/petsc-${PETSC_VER} PETSC_ARCH=real-opt all && \
    cd $PETSC_DIR/src/binding/petsc4py && pip install . --no-build-isolation

# -----
# CGNS
# -----
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    echo '# CGNS' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo "export CGNS_HOME=$DAFOAM_ROOT_PATH/packages/CGNS-${CGNS_VER}/opt-gfortran" >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export PATH=$PATH:$CGNS_HOME/bin' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CGNS_HOME/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    . $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/packages && \
    wget https://github.com/CGNS/CGNS/archive/v${CGNS_VER}.tar.gz -O cgns.tar.gz && \
    tar -xvaf cgns.tar.gz && \
    cd CGNS-${CGNS_VER} && mkdir -p build && cd build && \
    cmake .. -DCGNS_ENABLE_FORTRAN=1 -DCMAKE_INSTALL_PREFIX=$CGNS_HOME \
             -DCGNS_BUILD_CGNSTOOLS=0 -DCGNS_ENABLE_HDF5=OFF -DCGNS_ENABLE_64BIT=OFF \
             -DCMAKE_C_FLAGS="-fPIC" -DCMAKE_Fortran_FLAGS="-fPIC" && \
    make all install -j ${MAKE_JOBS}

# ------
# IPOPT
# ------
RUN if [ "${BUILD_IPOPT}" = "true" ]; then \
      . /home/dafoamuser/dafoam/loadDAFoam.sh && \
      echo '# Ipopt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
      echo 'export IPOPT_DIR=$DAFOAM_ROOT_PATH/packages/Ipopt' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
      echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$IPOPT_DIR/lib' >> $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
      . $DAFOAM_ROOT_PATH/loadDAFoam.sh && \
      cd $DAFOAM_ROOT_PATH/packages && \
      git clone --depth 1 -b stable/3.13 https://github.com/coin-or/Ipopt.git && \
      cd $IPOPT_DIR && \
      git clone --depth 1 -b stable/1.3 https://github.com/coin-or-tools/ThirdParty-Blas.git && \
      cd ThirdParty-Blas && ./get.Blas && \
      ./configure --prefix=$IPOPT_DIR && \
      make && make install && cd .. && \
      git clone --depth 1 -b stable/1.5 https://github.com/coin-or-tools/ThirdParty-Lapack.git && \
      cd ThirdParty-Lapack && ./get.Lapack && \
      ./configure --prefix=$IPOPT_DIR --with-blas-lflags="-L${IPOPT_DIR}/lib -lcoinblas" && \
      make && make install && cd .. && \
      git clone --depth 1 -b stable/1.3 https://github.com/coin-or-tools/ThirdParty-Metis.git && \
      cd ThirdParty-Metis && ./get.Metis && \
      ./configure --prefix=$IPOPT_DIR && make && make install && cd .. && \
      git clone --depth 1 -b stable/2.1 https://github.com/coin-or-tools/ThirdParty-Mumps.git && \
      cd ThirdParty-Mumps && ./get.Mumps && \
      ./configure --prefix=$IPOPT_DIR --with-blas-lflags="-L${IPOPT_DIR}/lib -lcoinblas" \
                   --with-metis-lflags="-L${IPOPT_DIR}/lib -lcoinmetis" \
                   --with-metis-cflags="-I${IPOPT_DIR}/include/coin/ThirdParty" \
                   --with-lapack-lflags="-L${IPOPT_DIR}/lib -lcoinlapack" && \
      make && make install && \
      cd $IPOPT_DIR && mkdir -p build && cd build && \
      ../configure --prefix=${IPOPT_DIR} --disable-java --with-mumps \
                   --with-mumps-lflags="-L${IPOPT_DIR}/lib -lcoinmumps" \
                   --with-mumps-cflags="-I${IPOPT_DIR}/include/coin-or/mumps" \
                   --with-blas-lflags="-L${IPOPT_DIR}/lib -lcoinblas" \
                   --with-metis-lflags="-L${IPOPT_DIR}/lib -lcoinmetis" \
                   --with-metis-cflags="-I${IPOPT_DIR}/include/coin/ThirdParty" \
                   --with-lapack-lflags="-L${IPOPT_DIR}/lib -lcoinlapack" && \
      make && make install ; \
    fi

# ----------------------------
# MACH-Aero pinned components
# ----------------------------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/baseclasses/archive/v${BASECLASSES_VER}.tar.gz -O baseclasses.tar.gz && \
    tar -xf baseclasses.tar.gz && cd baseclasses-${BASECLASSES_VER} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/pyspline/archive/v${PY_SPLINE_VER}.tar.gz -O pyspline.tar.gz && \
    tar -xf pyspline.tar.gz && cd pyspline-${PY_SPLINE_VER} && \
    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    make -j ${MAKE_JOBS} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/pygeo/archive/v${PY_GEO_VER}.tar.gz -O pygeo.tar.gz && \
    tar -xf pygeo.tar.gz && cd pygeo-${PY_GEO_VER} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/multipoint/archive/v${MULTIPOINT_VER}.tar.gz -O multipoint.tar.gz && \
    tar -xf multipoint.tar.gz && cd multipoint-${MULTIPOINT_VER} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/cgnsutilities/archive/v${CGNS_UTILS_VER}.tar.gz -O cgnsutilities.tar.gz && \
    tar -xf cgnsutilities.tar.gz && cd cgnsutilities-${CGNS_UTILS_VER} && \
    cp config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    make -j ${MAKE_JOBS} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/pyhyp/archive/v${PY_HYP_VER}.tar.gz -O pyhyp.tar.gz && \
    tar -xf pyhyp.tar.gz && cd pyhyp-${PY_HYP_VER} && \
    cp -r config/defaults/config.LINUX_GFORTRAN_OPENMPI.mk config/config.mk && \
    sed -i "s/mpifort/mpif90/g" config/config.mk && \
    make -j ${MAKE_JOBS} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/idwarp/archive/v${IDWARP_VER}.tar.gz -O idwarp.tar.gz && \
    tar -xf idwarp.tar.gz && cd idwarp-${IDWARP_VER} && \
    cp -r config/defaults/config.LINUX_GFORTRAN.mk config/config.mk && \
    sed -i "s/mpifort/mpif90/g" config/config.mk && \
    make -j ${MAKE_JOBS} && pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/prefoil/archive/v${PREFOIL_VER}.tar.gz -O prefoil.tar.gz && \
    tar -xf prefoil.tar.gz && cd prefoil-${PREFOIL_VER} && \
    pip install . && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/pyoptsparse/archive/v${PYOPTSPARSE_VER}.tar.gz -O pyoptsparse.tar.gz && \
    tar -xf pyoptsparse.tar.gz && cd pyoptsparse-${PYOPTSPARSE_VER} && \
    pip install .

# ---------------
# OpenFOAM v1812
# ---------------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
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
    export WM_NCOMPPROCS=${MAKE_JOBS} && \
    ./Allwmake

# ------------------------
# OpenFOAM Reverse-mode AD
# ------------------------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/OpenFOAM && \
    wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v${OPENFOAM_AD_TAG}.tar.gz -O OpenFOAM-v1812-AD.tgz && \
    tar -xf OpenFOAM-v1812-AD.tgz && mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADR && \
    cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADR && \
    sed -i 's/WM_PROJECT_VERSION=v1812-AD/WM_PROJECT_VERSION=v1812-ADR/g' etc/bashrc && \
    sed -i 's/export WM_CODI_AD_LIB_POSTFIX=ADF/export WM_CODI_AD_LIB_POSTFIX=ADR/g' etc/bashrc && \
    . $DAFOAM_ROOT_PATH/loadDAFoam.sh && source etc/bashrc && \
    export WM_NCOMPPROCS=${MAKE_JOBS} && \
    ./Allwmake && \
    DASimpleFoamReverseAD -help >/dev/null && \
    # link ADR libs into original OpenFOAM-v1812 (relative symlinks for portability)
    cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib && \
    ln -s ../../../../OpenFOAM-v1812-ADR/platforms/*/lib/*.so . && \
    cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy && \
    ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/dummy/*.so . && \
    cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/openmpi-system && \
    ln -s ../../../../../OpenFOAM-v1812-ADR/platforms/*/lib/openmpi-system/*.so .

# ------------------------
# (Optional) OpenFOAM ADF
# ------------------------
RUN if [ "${BUILD_ADF}" = "true" ]; then \
      . /home/dafoamuser/dafoam/loadDAFoam.sh && \
      cd $DAFOAM_ROOT_PATH/OpenFOAM && \
      wget https://github.com/DAFoam/OpenFOAM-v1812-AD/archive/v${OPENFOAM_AD_TAG}.tar.gz -O OpenFOAM-v1812-AD.tgz && \
      tar -xf OpenFOAM-v1812-AD.tgz && mv OpenFOAM-v1812-AD-* OpenFOAM-v1812-ADF && \
      cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812-ADF && \
      sed -i 's/WM_PROJECT_VERSION=v1812-AD/WM_PROJECT_VERSION=v1812-ADF/g' etc/bashrc && \
      . $DAFOAM_ROOT_PATH/loadDAFoam.sh && source etc/bashrc && \
      export WM_NCOMPPROCS=${MAKE_JOBS} && \
      ./Allwmake && \
      cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib && \
      ln -s ../../../../OpenFOAM-v1812-ADF/platforms/*/lib/*.so . && \
      cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/dummy && \
      ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/dummy/*.so . && \
      cd $DAFOAM_ROOT_PATH/OpenFOAM/OpenFOAM-v1812/platforms/*/lib/openmpi-system && \
      ln -s ../../../../../OpenFOAM-v1812-ADF/platforms/*/lib/openmpi-system/*.so . ; \
    fi

# -----
# pyOFM
# -----
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/pyofm/archive/refs/tags/v${PYOFM_VER}.tar.gz -O pyofm.tar.gz && \
    tar -xf pyofm.tar.gz && cd pyofm-* && make -j ${MAKE_JOBS} && pip install .

# ----------------------
# Hisa4DAFoam (Optional)
# ----------------------
RUN if [ "${BUILD_HISA}" = "true" ]; then \
      . /home/dafoamuser/dafoam/loadDAFoam.sh && \
      cd $DAFOAM_ROOT_PATH/OpenFOAM && \
      git clone https://github.com/DAFoam/Hisa4DAFoam && \
      cd Hisa4DAFoam && \
      ./Allmake ; \
    fi

# -------
# DAFoam
# -------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/mdolab/dafoam/archive/v${DAFOAM_VER}.tar.gz -O dafoam.tar.gz && \
    tar -xf dafoam.tar.gz && cd dafoam-* && \
    ./Allmake && \
    echo "" && echo "DAFoam build complete."

# (Optional) Compile DAFoam ADF if BUILD_ADF is true
RUN if [ "${BUILD_ADF}" = "true" ]; then \
      . /home/dafoamuser/dafoam/loadDAFoam.sh && \
      cd $DAFOAM_ROOT_PATH/repos/dafoam-* && \
      export COMPILE_DAFOAM_ADF=1 && \
      ./Allmake ; \
    fi

# -------
# OpenMDAO
# -------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    pip install openmdao==${OPENMDAO_VER}

# -------
# MPhys
# -------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/OpenMDAO/mphys/archive/${MPHYS_HASH}.tar.gz -O mphys.tar.gz && \
    tar -xvf mphys.tar.gz && mv mphys-* mphys && \
    cd mphys && pip install .

# -------
# FUNtoFEM
# -------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/smdogroup/funtofem/archive/refs/tags/v${FUNTOFEM_VER}.tar.gz -O funtofem.tar.gz && \
    tar -xvf funtofem.tar.gz && mv funtofem-* funtofem && \
    cd funtofem && cp Makefile.in.info Makefile.in && \
    sed -i "s/F2F_DIR=.*/F2F_DIR=\$\{DAFOAM_ROOT_PATH\}\/repos\/funtofem/g" Makefile.in && \
    sed -i "s/LAPACK_LIBS\ =.*/LAPACK_LIBS=-L\$\{PETSC_LIB\}\ -lf2clapack -lf2cblas/g" Makefile.in && \
    make && pip install -e . --no-build-isolation

# -------
# TACS
# -------
RUN . /home/dafoamuser/dafoam/loadDAFoam.sh && \
    cd $DAFOAM_ROOT_PATH/repos && \
    wget https://github.com/smdogroup/tacs/archive/refs/tags/v${TACS_VER}.tar.gz -O tacs.tar.gz && \
    tar -xvf tacs.tar.gz && mv tacs-* tacs && \
    cd tacs/extern && \
    wget https://github.com/DAFoam/files/releases/download/TACS_Extern/TACS_extern.tar.gz && tar -xzf TACS_extern.tar.gz && \
    rm -rf metis-4.0.3* && \
    wget https://github.com/DAFoam/files/releases/download/TACS_Extern/metis-5.1.0.tar.gz && \
    tar -czvf TACS_extern.tar.gz metis*.tar.gz UFconfig*.tar.gz AMD*.tar.gz && \
    tar -xzf metis*.tar.gz && \
    cd metis-5.1.0 && make config prefix=$DAFOAM_ROOT_PATH/repos/tacs/extern/metis/ CFLAGS="-fPIC" && make install && \
    cd ../../ && \
    cp Makefile.in.info Makefile.in && \
    sed -i "s/TACS_DIR\ =.*/TACS_DIR=\$\{DAFOAM_ROOT_PATH\}\/repos\/tacs/g" Makefile.in && \
    sed -i "s/LAPACK_LIBS\ =.*/LAPACK_LIBS=-L\$\{PETSC_LIB\}\ -lf2clapack -lf2cblas -lpthread/g" Makefile.in && \
    make && pip install -e . --no-build-isolation && \
    cd extern/f5tovtk && make && cp f5tovtk $DAFOAM_ROOT_PATH/OpenFOAM/sharedBins

# Default env on container start
RUN echo 'echo "Loading DAFoam environment..."' >> /home/dafoamuser/.bashrc && \
    echo '. $HOME/dafoam/loadDAFoam.sh' >> /home/dafoamuser/.bashrc

# Helpful default
WORKDIR /home/dafoamuser
CMD ["/bin/bash"]

</pre>

{% include links.html %}

---
title:  "DAFoam v2.0 released with major code restructuring"
categories: jekyll update
permalink: dafoam_v2_released.html
---

DAFoam v2.0 is a major update that introduces multiple features for a more efficient interface, better performance, and more modulated code structures. 

- Rewrite the classes and member functions. Now each partial derivative is implemented in a child class of DAPartDeriv. Similarly, each objective function is implemented in DAObjFunc. The C++ classes now receive parameters directly from the Python layer through DAOption class. The primal and adjoint calls use Petsc vectors as input and output.

- All the primal and adjoint solvers are now compiled as libraries, and Cython is used to wrap all libraries such that everything happens in memory; there is no file IO interaction between the C++ and Python layers. 

- Optimize the screen output for primal and adjoint solutions. Now all the optimization process will be printed to screen, instead of separate files. Users can set `printInterval` to specify how frequently the primal and adjoint solution progress is printed. 

- Improve the performance of the file output of intermediate shapes. Facilitate the visualization of optimization results by renaming the intermediate shape and flow fields into different time folders.

- Use setup.py to enable `pip install .`.

- The `pyDAFoam.py` will no longer write configuration files for OpenFOAM. Users need to provide a working OpenFOAM configuration to start the optimization.

- Multipoint optimization no longer needs multiple folders.

{% include links.html %}

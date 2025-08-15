---
title: OpenFOAM Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openfoam.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## 1. Overview of DAFoam and OpenFOAM

### 1.1 What is DAFoam?
DAFoam (Discrete Adjoint with OpenFOAM) is a high-fidelity multidisciplinary design optimization and analysis framework. DAFoam can be used to compute derivatives for a large amount of design variables, perform gradient based optimizations, and run OpenFOAM primal solvers to generate CFD samples.

### 1.2 What is OpenFOAM?
OpenFOAM (Open-source Field Operation And Manipulation) is a free finite-volume open-source CFD solver. OpenFOAM is primarily written in C++ and comes with libraries to help facilitate numerical operations on field values. OpenFOAM also has a wide range of utilities for pre- and post- processing such as mesh generation/quality checks and paraview (for post-process visualization). There are three main branches of OpenFOAM: ESI OpenCFD, The OpenFOAM Foundation, and Extended Project. DAFoam only supports the ESI OpenCFD version.


## 2. Details of Configuration Files
Since DAFoam uses OpenFOAM as the CFD solver, the file structure of a DAFoam simulation is very similar to that of an OpenFOAM simulation. To help with clarity, below is the file structure for the [NACA 0012 incompressible tutorial case]([http://github.com/dafoam/tutorials/](https://github.com/DAFoam/tutorials/tree/main/NACA0012_Airfoil/incompressible)) 

<pre>
- 0.orig               // initial fields and boundary conditions
- FFD                  // folder that containts FFD file
- constant             // flow and turbulence property information
- profiles             // naca0012 profile coordinates for mesh generation
- system               // flow discretization, setup, time step etc.
- Allclean.sh          // script to clean up simulation results
- genAirFoilMesh.py    // mesh generation script called by preProcessing
- paraview.foam        // dummy file used by paraview to load results
- preProcessing.sh     // script to generate the mesh
- runScript.py         // main run script for optimization
</pre>

### 2.1 0.orig
The 0.orig file contains the initial field values as well as the field boundary conditions of the simulation:

<pre>
0.orig         
|-- epsilon    // turbulent kinetic energy dissipation rate
|-- k          // turbulent kinetic energy
|-- nut        // turbulent viscosity
|-- nuTilda    // modified turbulent viscosity
|-- omega      // specific dissipation rate
|-- p          // pressure
|-- U          // velocity
</pre>

The exact setup of the 0.orig file (which field values to include and what their initial values should be) depends on the case being setup. To serve as an example we can open the 0.orig/U file. The first line is the `dimensions [0 1 -1 0 0 0 0];` line. This line specifies the units used for the field value. For the NACA 0012 case the initial velocity condition is 10 m/s, hence `internalField uniform (10 0 0);` is set. The following block (`boundaryField`) is where the actual boundary conditions are defined. 

<pre>
dimensions      [0 1 -1 0 0 0 0];
  
internalField uniform (10 0 0);

boundaryField
{
    "(wing.*)"
    {
        type            fixedValue;
        value           uniform (0 0 0);
    }
  
    symmetry1
    {
        type            symmetry;
    }
  
    symmetry2
    {
        type            symmetry;
    }
  
    inout
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }
}
</pre>

In this shape optimization of the airfoil, OpenFOAM does not support pure 2D cases so the airfoil is modeled as a 3D airfoil that is only 1 mesh cell thick, hence two symmetry boundary conditions. Inout refers to the far field domain inlet condition and `"(wing.*)"` refers to all boundaries defined by the airfoil. The `value uniform (0 0 0);` for the airfoil provides a no slip boundary condition on the wall. The inout boundary condition is standard for this type of case and usually does not need to be adjusted. Similar setups follow for the other field values (p, nuTilda, k etc.). 

### 2.2 FFD
The FFD folder contains two files: a genFFD.py script and a wingFFD.xyz file. The genFFD.py script is used to generate the FFD points and export their coordinates to the plot3D format needed in the simulation. It should be noted that this script generates a clean FFD box, not body fitted FFDs (which can be done using [ICEM CFD](https://github.com/mdolab/dafoam/discussions/652) amongst other methods). The FFD points can be easily adjusted using this file in terms of number of FFD points and their locations:

<pre>
nBlocks = 1   // number of FFD boxes
nx = [5]      // number of FFD points in x-direction
ny = [2]      // number of FFD points in y-direction
nz = [2]      // number of FFD points in z-direction

corners = np.zeros([nBlocks,8,3])     // initialize corners array to store FFD box coordinates (below)
  
corners[0,0,:] = [-0.010,-.0700,0.0]  // add x, y, z coordinates of FFD box (all 8 corners needed)
corners[0,1,:] = [-0.010,-0.0700,0.1]
corners[0,2,:] = [-0.010,0.0700,0.0]
corners[0,3,:] = [-0.010,0.0700,0.1]
corners[0,4,:] = [ 1.01,-.07,0.0]
corners[0,5,:] = [ 1.01,-.07,0.10]
corners[0,6,:] = [ 1.01,0.07,0.0]
corners[0,7,:] = [ 1.01,0.07,0.1]
</pre>

By increasing or decreasing nx, ny, and/or nz you can increase or decrease the number of FFD points modeled. Additionally, adjusting the coordinates in the 'corners' array will adjust the location of the FFD box. The remainder of this file can be left unchanged. When visualizing the FFD points in paraview, the program may crash if there are too few mesh cells (this is a bug in paraview where the program struggles with small plot3D files). To overcome this, we can load the DAFoam environement and run the command `dafoam_plot3d2tecplot.py wingFFD.xyz wingFFD.dat`. This will create a .dat version of your FFD.xyz file that paraview will be able to load.

These FFD points can be generated using a custom script as well, the user just needs to be mindful of the order of the points (x coordinates on first line, y coordinates on second line, z coordinates on third line) in the .xyz file and use proper headers (first two lines below). 

<pre>
1                                     // number of FFD blocks (header)
5  2  2                               // nx ny nz             (header)
-0.010000  0.245000  0.500000 . . .   // list of x coordinates
-0.070000 -0.070000 -0.070000 . . .   // list of y coordinates
 0.000000  0.000000  0.000000 . . .   // list of z coordinates
</pre>

If generating your own FFD points using a different script then paraview is a great way to visualize the points and potentially debug the FFD script. To load the .xyz file into paraview go file -> open and select the .xyz file. Choose the `PLOT3D Reader` from the pop-up menu. On the left hand menu uncheck `Binary File` and check `Multi Grid` then hit `Apply`. You will be able to see the points in the working window. If done properly, and after setting the representation to `outline`, a clean FFD box should appear. Lastly, when generating FFD points, the points must fully contain the design surface or the simulation will abort.


### 2.3 constant
The constant folder contains the mesh files (polyMesh directory) as well as flow and turbulence property definitions:

<pre>
constant         
|-- polyMesh               // directory containing the files
  |-- boundary             // mesh boundary patch names and types
  |-- faces.gz             // mesh faces
  |-- neighbour.gz         // face neighbour info
  |-- owner.gz             // face owner info
  |-- points.gz            // baseline mesh point coordinates
|-- transportProperties    // transport model definition
|-- turbulenceProperties   // turbulence model
</pre>

As seen below, from the polyMesh/boundary file, are the same boundary names as seen in 0.orig/U. The boundary file can be lightly adjusted manually: users can change the name of boundaries (such as changing the `wing` boundary name to `airfoil` for example), the type of boundary present, and delete boundaries. However, though these values can be changed without destroying the mesh, mesh manipulation should not take place manually. Manually adjusting the other files in polyMesh/ or the other entries (nFaces, startFace, inGroups etc.) is a difficult and inefficient method of adjusting the mesh and will most likely destroy the mesh. If the mesh must be adjusted the best practice is to regenerate the mesh.

<pre>
4    // number of boundaries defined in file (modifiable)
(
    symmetry1                          // name of boundary (modifiable)
    {
        type            symmetry;      // type of boundary (modifiable)
        inGroups        1(symmetry);   // group of boundary
        nFaces          4032;          // number of faces in boundary
        startFace       7938;          // starting face of boundary
    }
  
    symmetry2
    {
        type            symmetry;
        inGroups        1(symmetry);
        nFaces          4032;
        startFace       11970;
    }
  
    wing
    {
        type            wall;
        inGroups        1(wall);
        nFaces          126;
        startFace       16002;
    }
  
    inout
    {
        type            patch;
        nFaces          126;
        startFace       16128;
    }
)
</pre>

The following two files, transportProperties and turbulenceProperties, are relatively straightforward. The transportProperties defines flow properties which may be adjusted to model a different fluid:

<pre>
transportModel Newtonian;   // transport model to use

nu 1.5e-5;                  // molecular viscosity
Pr 0.7;                     // Prandtl number
Prt 1.0;                    // turblent Prandtl number
</pre>

The turbulenceProperties file elects which turbulence model to use:

<pre>
simulationType RAS;
RAS 
{ 
    RASModel             SpalartAllmaras;   // which RAS model to use
    turbulence           on;                // model turbulence
    printCoeffs          off;               // whether or not to print turbulence model coefficients
} 
</pre>


### 2.4 system






































### 2.5 genAirFoilMesh.py    
### 2.6 preProcessing.sh     
### 2.7 runScript.py 
### 2.8 misc -> profiles, paraview.foam, Allclean.sh






































## Post-processing Results
### Installing Paraview
### Loading case into paraview
### Visualizing case in paraview



















{% include links.html %}

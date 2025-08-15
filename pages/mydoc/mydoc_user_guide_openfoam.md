---
title: OpenFOAM Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openfoam.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## 1. Overview of OpenFOAM
OpenFOAM (Open-source Field Operation And Manipulation) is a free finite-volume open-source CFD solver. OpenFOAM is primarily written in C++ and comes with libraries to help facilitate numerical operations on field values. OpenFOAM also has a wide range of utilities for pre- and post-processing, such as mesh generation/quality checks and Paraview (for post-process visualization). There are three main branches of OpenFOAM: ESI OpenCFD, The OpenFOAM Foundation, and Extended Project. DAFoam only supports the ESI OpenCFD version.


## 2. Details of Configuration Files
To help with clarity, below is the general file structure for OpenFOAM simulations. As a general overview: `0` contains boundary conditions and initial field values, `constant` handles flow properties (such as turbulence model and fluid modeling parameters), and `system` controls the numerical discretization, equation solutions, etc. In this section, we will discuss each entry below.

<pre>
- 0                    // initial fields and boundary conditions
- constant             // flow and turbulence property information
- system               // flow discretization, setup, time step etc.
- paraview.foam        // dummy file used by Paraview to load results
</pre>

### 2.1 The 0 folder
The 0 folder contains the initial field values as well as the field boundary conditions of the simulation:

<pre>
0        
|-- epsilon    // turbulent kinetic energy dissipation rate
|-- k          // turbulent kinetic energy
|-- nut        // turbulent viscosity
|-- nuTilda    // modified turbulent viscosity
|-- omega      // specific dissipation rate
|-- p          // pressure
|-- U          // velocity
</pre>


The exact setup of the 0 folder (which field values to include and what their initial values should be) depends on the case being setup. To serve as an example, we can open the 0/U file. The first line is the `dimensions [0 1 -1 0 0 0 0];` line. This line specifies the units used for the field value. For the wing case, the initial velocity condition is 10 m/s in the x direction, hence `internalField uniform (10 0 0);` is set. The following block (`boundaryField`) is where the actual boundary conditions are defined. Refer to the following figure for the setup of the internal and boundary fields.

<img src="{{ site.url }}{{ site.baseurl }}/images/user_guide/analysis_discretization.png" style="width:700px !important;" />

Fig. 1. A schematic description of the internal and boundary fields for a 2D simulation domain


<pre>
dimensions      [0 1 -1 0 0 0 0];
  
internalField uniform (10 0 0);

boundaryField
{
    wing                                   // wing patch name
    {
        type            fixedValue;        // type of boundary condition
        value           uniform (0 0 0);   // value of boundary condition
    }
  
    symmetryPlane
    {
        type            symmetry;
    }
  
    inout                                  // far field patch name
    {
        type            inletOutlet;
        inletValue      $internalField;
        value           $internalField;
    }
}
</pre>

The `wing` refers to the wing surface. In OpenFOAM, we call a boundary surface a `patch`. We fixed the value with `type fixedValue;` to `value uniform (0 0 0);` for the wing to provide a no-slip boundary condition on the wall. We use the `symmetry` boundary condition for the wing symmetry plane. The boundary name `inout` refers to the far field patch, which uses the `inletOutlet` boundary condition type. This boundary condition type is common when dealing with wing cases or channel flows, for example. The `inletOutlet` boundary condition automatically applies `fixedValue` when the flow enters the simulation domain with the values given by the `inletValue` key, and `zeroGradient` when the flow exits the domain. Here, we can use `$internalField` to specify that the value we want to prescribe is the same as the internalField value defined above, i.e., `uniform (10 0 0)`. The `value` key for the `inout` patch prescribes an initial value for this patch, and this value will be automatically updated (depending on whether the flow enters or leaves the domain) when the simulation starts.



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

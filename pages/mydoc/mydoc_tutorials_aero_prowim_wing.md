---
title: Prowim wing
keywords: tutorial, prowim
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_aero_prowim_wing.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is an aerodynamic shape optimization case for the Prowim wing-propeller configuration. Refer to [this paper]([https://www.sciencedirect.com/science/article/abs/pii/S1270963822005508?via%3Dihub]) for more simulations and optimization results.

<pre>
Case: Wing-propeller aerodynamic optimization
Geometry: Prowim wing
Objective function: Drag
Design variables: 120 FFD points moving in the y direction
Constraints: Volume, thickness, curvature and lift
Propeller model: Actuator disk
Mach number: 0.3
Mesh cells: 690 K
Adjoint solver: DARhoSimpleFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Prowim_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the Prowim wing-propeller case

|

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/main.tar.gz) and untar it. Then go to tutorials-main/Prowim_Wing_Propeller and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

We recommend running this case on an HPC system with 20 CPU cores:

<pre>
mpirun -np 20 python runScript.py 2>&1 | tee logOpt.txt
</pre>

This example includes a task to generate a Computer-Aided Design (CAD) file of the optimized wing geometry in IGES format.
This process works by using the original, undeformed geometry in IGES format, and deforming it given the state of the FFD at the end of the optimization.
For this specific example, a script is included to run the deformation, titled `deformGeo.sh`, but each step of the process can be carried out manually as well.
The process begins with generating the original geometry in IGES format.
This is done using pyGeo and calling the `generate_wing.py` script in the `deformGeo` directory to generate an IGES file of the initial geometry.
Also in this directory is the reference data which defines a state of the design variables in the FFD.
This JSON file, `OptRef_Example.json`, along with the undeformed IGES file must be copied to the root directory of the case.
Then, the geometry can be deformed by running the command:

<pre>
python runScript.py --task=deformGeo
</pre>

This task is shown in the code listing below.
The process begins by reading the dictionary of design variable states from the JSON file and then initializing a pyGeo object using the undeformed IGES file in the root directory.
Next, the design variables governing the FFD are updated using the design variable dictionary and the pyGeo method `DVGeo.updatePyGeo()`.
Finally, the geometry is deformed and output to a new IGES file with the name `wingNew.igs` by calling the pyGeo method `DVGeo.updatePyGeo()`.

```python
elif args.task == "deformGeo":
    # Import Optimization Values Dictionary
    with open("./OptRef_Example.json") as f:
        optRef = json.load(f)

    # Import IGES file as geometry object
    geo = pyGeo(fileName="./wing.igs", initType="iges")
    geo.doConnectivity()

    # Update Design Variables
    DVGeo.setDesignVars(optRef)

    # Deform Geometry and Output
    DVGeo.updatePyGeo(geo, "iges", "wingNew", nRefU=10, nRefV=10)
```

When using this function, it is important to provide an initial geometry that exactly matches the initial geometry used in the optimization.
Additionally, the quality of the deformation and it's representation of the optimized geometry will greatly depend on how refined its surfaces are; if the output geometry does not match the optimized geometry, provide a more refined initial geometry or increase the values of the parameters `nRefU` and `nRefV`.

```python
self.geometry.nom_addCurvatureConstraint1D(
            "curvature1",
            start=[0.12, 0, 0.02],
            end=[0.12, 0, 0.6],
            nPts=20,
            axis=[0, 1, 0],
            curvatureType="mean",
            scaled=False,
        )
```

The optimized wing shape might have articial wavy distribution in the spanwise direction, to prevent this a spanwise curvature constraint is imposed on on the wing surfaces. `start` and `end` are two endpoints of the reference line, `nPts` is the number of nodes on the reference line, `axis` is the direction used to project the reference line on the desired surface, `curvatureType` it the calculation method of the curvature, and `scaled` scales calculated curvatures during the optimization with initial curvature i `True` .

```python
self.add_constraint("geometry.curvature1", lower=0.0, upper=0.1, scaler=1.0)
```

Above line pass curvature constraints to the top level. `lower` is the lower boundary, `upper` is the upper boundary, `scaler` scales the constraint with the given number.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Prowim_optimization_animation.gif" width="500" />

Fig. 2. Animation of the Prowim wing-propeller case optimization

{% include links.html %}

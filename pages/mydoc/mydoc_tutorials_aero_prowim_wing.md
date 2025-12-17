---
title: Prowim wing
keywords: tutorial, prowim
summary: 
sidebar: mydoc_sidebar
permalink: tutorials-aero-prowim-wing.html
folder: mydoc
---


The following is an aerodynamic shape optimization case for the Prowim wing-propeller configuration. Refer to [this paper](https://www.sciencedirect.com/science/article/abs/pii/S1270963822005508?via%3Dihub) for more simulations and optimization results.

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

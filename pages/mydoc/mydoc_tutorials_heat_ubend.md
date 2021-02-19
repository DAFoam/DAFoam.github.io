---
title: U bend channel
keywords: tutorial, ubend
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_heat_ubend.html
folder: mydoc
---

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

The following is a heat transfer optimization case for the von Karman U bend channel, representative of a internal cooling section in turbines.

<pre>
Case: Heat transfer optimization for U bend cooling channels
Geometry: von Karman U bend channel
Objective function: Combined wall heat flux and total pressure loss
Design variables: 114 FFD points moving in the x, y, and z directions
Constraints: Symmetry constraint (total number: 38)
Mach number: 0.02
Reynolds number: 4.2e4
Mesh cells: 4.8 K
Solver: DASimpleTFoam
</pre>

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/UBend_FFD.png" width="500" />

Fig. 1. Mesh and FFD points for the U bend channel case

|

In this case, we set up a combined objective function of wall heat flux and total pressure loss. This is done by setting three parts for the objFunc. part1 and part2 are the total pressure at the inlet and outlet, respectively. part3 is the wall heat flux. The weights between the heat flux and total pressure loss is 0.5.

<pre>
"objFunc": {
    "obj": {
        "part1": {
            "type": "totalPressure",
            "source": "patchToFace",
            "patches": ["inlet"],
            "scale": 1.0 / CPL0 * CPL_weight,
            "addToAdjoint": True,
        },
        "part2": {
            "type": "totalPressure",
            "source": "patchToFace",
            "patches": ["outlet"],
            "scale": -1.0 / CPL0 * CPL_weight,
            "addToAdjoint": True,
        },
        "part3": {
            "type": "wallHeatFlux",
            "source": "patchToFace",
            "patches": ["ubendup"],
            "scale": 1.0 / HFL0 * HFL_weight,
            "addToAdjoint": True,
        }
    },
},
</pre>

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/UBend_Channel and run the "preProcessing.sh" script to generate the mesh:

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the optimization with 4 CPU cores:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

This case ran for 18 iterations. The heat flux remained the same while the total pressure loss reduced by 53.4%. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/UBend_movie.gif" width="640" />

Fig. 2. Evolution of wall heat flux and velocity during the optimization

{% include links.html %}

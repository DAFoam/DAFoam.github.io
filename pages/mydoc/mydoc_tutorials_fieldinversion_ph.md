---
title: Field inversion tutorial
keywords: field inversion, run script, optimization
summary: "We need to set runScript.py for field inversion."
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_field_inversion_ph.html
folder: mydoc
---
## Overview
The following is a demonstration of how to perform field inversion using DAFoam. We have selected the periodic hill flow as a demonstrative case. In this tutorial we will show how we can augment the Spalart-Allmaras model using steamwise velocity data. For the purposes of this tutorial, we will be treating the results from the k-epsilon model as the reference data. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/FI/phMesh.png" width="500" />
Fig. 1. Periodic hill geometry and mesh. 

{% include note.html content="We recommend going through the tutorial in [Get started](mydoc_get_started_download_docker.html) before running this case." %}

## The field inversion process
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/FI/flowchart.png" width="500" />
Fig. 2. Field inversion flow diagram. 


## Reference data for field inversion 


## Setting up the objective function


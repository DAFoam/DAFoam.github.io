---
title: Overview
keywords: verifications, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_verifications_overview.html
folder: mydoc
---

This section provides DAFoam configurations for verifying the accuracy of adjoint derivative computation. Here we compared the derivatives between the forward mode AD (reference)and the JacobianFree adjoint method. The configuration files are available from [here](https://github.com/DAFoam/verifications). 

To run a case, we need to first generate the mesh by running:

<pre>
./preProcessing.sh
</pre>

To compute the adjoint derivatives, run:

<pre>
mpirun -np 4 python runScript.py
</pre>

To compute the reference derivatives using the forward mode AD for a specific design variable, run: 

<pre>
mpirun -np 4 python runScript.py --task=runForwardAD --dvName="shape" --seedIndex=0
</pre>

The above command will run the primal solver with the forward mode AD, and print out the derivative for the 0th "shape" design variable to the screen during the computation. One can follow a similar syntax for other design variables and indices.

**NOTE:** For most of the case, the adjoint matches the referene by about 6 digits. This is because (a) OpenFOAM uses bounding and limiting in the CFD, and the resulting discontinuity will degrade the adjoint derivative accuracy. (b) not all OpenFOAM functions are AD in parallel, e.g., the meshWave wall distance calculation. However, we do have a machine-precision accurate case with specific settings, refer to DASimpleFoamMachinePrecision.

{% include links.html %}

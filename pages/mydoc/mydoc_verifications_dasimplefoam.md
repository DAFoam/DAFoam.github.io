---
title: DASimpleFoam
keywords: verifications, dasimplefoam
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_verifications_dasimplefoam.html
folder: mydoc
---

First, we need to generate the mesh by running:

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

## Shape variable
<pre>
dCD/dFFD               variable 0              variable 1            variable 2
JacobianFree Adjoint   0.009255243575551558    0.01047401958164599   0.02533621106400400
Forward AD Reference   0.009255240832202055    0.01047401678464814   0.02533620897519522
</pre>

<pre>
dCL/dFFD               variable 0              variable 1            variable 2
JacobianFree Adjoint   0.2420678446385925      0.2003391030258654    0.2803494795556929
Forward AD Reference   0.2420677747696623      0.2003390346061161    0.280349381693572
</pre>

<pre>
dCM/dFFD               variable 0              variable 1            variable 2
JacobianFree Adjoint   -0.2192318095476029     -0.2264412322773979   -0.2456426330965034
Forward AD Reference   -0.2192318311983444     -0.2264412538422797   -0.2456426563391394
</pre>

## Angle of attack
<pre>
dCD/dAOA               variable 0          
JacobianFree Adjoint   0.001315555375142706
Forward AD Reference   0.001315555386468653
</pre>

<pre>
dCL/dAOA               variable 0          
JacobianFree Adjoint   0.09954288373370906
Forward AD Reference   0.09954288344185892
</pre>

<pre>
dCM/dAOA               variable 0          
JacobianFree Adjoint   -0.001699253806194421
Forward AD Reference   -0.001699253814112301
</pre>


{% include links.html %}

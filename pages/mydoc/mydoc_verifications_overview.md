---
title: Overview
keywords: verifications, overview
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_verifications_overview.html
folder: mydoc
---

This section provides DAFoam configurations for verifying the accuracy of adjoint derivative computation (DAFoam achieves **machine precision accurate** adjoint). Here we compared the derivatives between the forward mode AD (reference) and the JacobianFree adjoint method. The configuration files are available from [here](https://github.com/DAFoam/verifications). 

To run a case, we need to first generate the mesh by running:

<pre>
./preProcessing.sh
</pre>

To compute the adjoint derivatives, run:

<pre>
mpirun -np 4 python runScript.py --mode=reverse --task=runAdjoint
</pre>

The adjoint derivatives will be saved to totalDerivHist.txt

To compute the reference derivatives using the forward mode AD for a specific design variable, run: 

<pre>
mpirun -np 4 python runScript.py --mode=forward --task=runForwardAD --dvName="shape" --seedIndex=0
</pre>

The above command will run the primal solver with the forward mode AD, and print out the derivative for the 0th "shape" design variable to the screen during the computation. See the following as an example. One can follow a similar syntax for other design variables and indices.

<pre>
Time = 1500
.....
CD-part1-force: 0.01807688896009773 ForwardAD Deriv: 0.009260839088106314
CL-part1-force: 0.3033625713510152 ForwardAD Deriv: 0.2419525437248765
CMZ-part1-moment: -0.00435313953943621 ForwardAD Deriv: -0.2192473028507385
</pre>

**NOTE**: we have to use meshWaveFrozen for wallDist in fvSchemes because the original meshWave method is not properly AD in OpenFOAM-v1812-AD. The meshWaveFrozen method is similar to meshWave, except that the wall distance will be computed only once (in the beginning of the optimization), and it will NOT be recomputed as the geometry changes during the optimization. We expect this has very little impact on the optimization results because IDWarp deforms the mesh based on the inverse-distance weighting method. The near wall mesh will deform as much as the wall, so the wall distance should remain the same.

{% include links.html %}

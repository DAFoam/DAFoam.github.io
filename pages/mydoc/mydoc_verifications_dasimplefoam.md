---
title: DASimpleFoam
keywords: verifications, dasimplefoam
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_verifications_dasimplefoam.html
folder: mydoc
---

First, download the configuration files from [here](https://github.com/DAFoam/verifications), then go to the DASimpleFoam folder, and run the commends mentioned in the overview section.

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

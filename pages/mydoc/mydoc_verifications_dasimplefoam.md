---
title: DASimpleFoam
keywords: verifications, dasimplefoam
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_verifications_dasimplefoam.html
folder: mydoc
---

First, download the configuration files from [here](https://github.com/DAFoam/verifications), then go to the DASimpleFoam folder, and run the commends mentioned in the overview section.

For most of the cases, the adjoint matches the reference values by **14 significant digits**.

## Shape variable
<pre>
dCD/dFFD               variable 0              variable 1            variable 2
Forward AD Reference   0.009260839088106553    0.01047989656042717   0.02535943905573043
JacobianFree Adjoint   0.009260839088106503    0.01047989656042720   0.02535943905573065
</pre>

<pre>
dCL/dFFD               variable 0              variable 1            variable 2
Forward AD Reference   0.2419525437248771      0.2002145064954005    0.2802869444676860
JacobianFree Adjoint   0.2419525437248756      0.2002145064953999    0.2802869444676880
</pre>

<pre>
dCM/dFFD               variable 0              variable 1            variable 2
Forward AD Reference   -0.2192473028507383     -0.2264587861502322   -0.2456468063599592
JacobianFree Adjoint   -0.2192473028507387     -0.2264587861502318   -0.2456468063599599
</pre>

## Angle of attack
<pre>
dCD/dAOA               variable 0    
Forward AD Reference   0.001315555355365731      
JacobianFree Adjoint   0.001315555355365766
</pre>

<pre>
dCL/dAOA               variable 0    
Forward AD Reference   0.09954288373144168      
JacobianFree Adjoint   0.09954288373144177
</pre>

<pre>
dCM/dAOA               variable 0   
Forward AD Reference   -0.001699253810007804       
JacobianFree Adjoint   -0.001699253810007761
</pre>


{% include links.html %}

---
title: ADODG3 wing - 3D aerodynamic shape optimization
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_adodg3.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

In the previous chapter, we have learned how to conduct optimization for 2D airfoils. This chapter will extend the optimization to a 3D wing called ADODG3. The following is a summary of the optimization.

<pre>
Case: 3D Wing aerodynamic optimization 
Geometry: ADODG3 Wing
Objective function: Drag coefficient (CD)
Lift coefficient (CL): 0.375
Design variables: 120 FFD points, twist, and angle of attack (total: 126).
Constraints: volume, thickness, LE/TE, and the lift coefficient (total number: 764)
Mach number: 0.3
Reynolds number: 0.22 million
Mesh cells: ~435,000
Solver: DARhoSimpleFoam
</pre>


{% include links.html %}

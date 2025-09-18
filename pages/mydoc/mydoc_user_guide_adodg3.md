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

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/ADODG3_Mesh_FFD.png" width="500" />
<br>
Fig. 1. Mesh and FFD points for the ADODG3 wing.

The "runScript.py" is based on the one used in the [NACA0012-Subsonic](https://dafoam.github.io/mydoc_user_guide_naca0012_variations.html) case with the following modifications:

- In "meshOptions", we set only one symmetry plane at z=0, instead of two symmetry planes used in the 2D airfoil case.

- We add a reference axis for the twist variable, and get the number of spanwise FFD point sections as nRefAxPts. In other words, if we have 10 FFD points in the spanwise direction, we will have 10 twist variables. Here we need to give a name to this axis "wingAxis", and this name will be used later when we define the twist function. "xFraction=0.25" means the axis is placed at the 25% chordwise (x) direction in the FFD box. "alignIndex=k" means the axis rotate with respect to the k index (z axis) in the FFD box. Here we assume the FFD's i, j, and k indices aligns with the x, y, and z directions. 

  ```python
  nRefAxPts = self.geometry.nom_addRefAxis(name="wingAxis", xFraction=0.25, alignIndex="k")
  ```

- We define a function to change the twist at these spanwise FFD sections. Here val, and geo are the two inputs. Note that we do NOT change the root twist (we already had angle of attack as design variable), so the first element in the twist design variable is the twist at the 2nd spanwise location.

  ```python
  def twist(val, geo):
      for i in range(1, nRefAxPts):
          geo.rot_z["wingAxis"].coef[i] = -val[i - 1]
  ```

- We call the following functions to add the twist design variable. Again, we have nTwist-1 twists because we do not change the root twist.

  ```python
  DVGeo.addGeoDVGlobal("twist", np.zeros(nTwists - 1), twist, lower=-10.0, upper=10.0, scale=1.0)
  daOptions["designVar"]["twist"] = {"designVarType": "FFD"}
  ```

- The leList and teList are oblique to the y axis. They should be close to the leading and trailing edges but completely within the wing surface.

  ```python
  leList = [[0.01, 0.0, 1e-3], [0.7, 0.0, 1.19]]
  teList = [[0.79, 0.0, 1e-3], [1.135, 0.0, 1.19]]
  ```

- We call the following functions to constrain the leading and trailing edge FFD movements by requiring them to move in the opposite directions. There is no need to manually set up the LE/TE linear constraints, as was done in the 2D airfoil case. Also, there is no need to impose symmetry constraints for k=0 and k=1 since this is a 3D wing case.

  ```python
  # Le/Te constraints
  DVCon.addLeTeConstraints(0, "iLow")
  DVCon.addLeTeConstraints(0, "iHigh")
  ```



{% include links.html %}

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

- We add a reference axis for the twist variable, and get the number of spanwise FFD point sections as `nRefAxPts`. In other words, if we have 10 FFD points in the spanwise direction, we will have 10 twist variables. Here we need to give a name to this axis `"wingAxis"`, and this name will be used later when we define the twist function. `xFraction=0.25` means the axis is placed at the 25% chordwise (x) direction in the FFD box. `alignIndex="k"` means the axis rotate with respect to the k index (z axis) in the FFD box. Here we assume the FFD's i, j, and k indices aligns with the x, y, and z directions. 

  ```python
  nRefAxPts = self.geometry.nom_addRefAxis(name="wingAxis", xFraction=0.25, alignIndex="k")
  ```

- We define a `twist` function to change the twist at these spanwise FFD sections. Here `val`, and `geo` are the two inputs. `val` is an array that has all the twist values the optimizer want to use, and we need to set these values to the `geo` object. `geo` is a pyGeo class, and `geo.rot_z["wingAxis"]` means the rotation (twist) angle for the `wingAxis` defined above. Here `coef[i]` is the ith spanwise twist angle. Note that we do NOT change the root twist (we already had angle of attack as design variable), so the first element in `val` is the twist at the 2nd spanwise location. That is why we assign `val[i-1]` to `coef[i]`. Also note that we use a minus sign for `val` because we want to use nose-up as positive twist, while pyGeo uses the right-hand rule to determine the rotation direction (which is nose down).

  ```python
  def twist(val, geo):
      for i in range(1, nRefAxPts):
          geo.rot_z["wingAxis"].coef[i] = -val[i - 1]
  ```

- We call the following functions to add the twist design variable to the `geometry` component. Again, we have nRefAxPts-1 twists because we do not change the root twist.

  ```python
  self.geometry.nom_addGlobalDV(dvName="twist", value=np.array([0] * (nRefAxPts - 1)), func=twist)
  ```

- The leList and teList are similar to the NACA0012 case. They should be close to the leading and trailing edges but completely within the wing surface. We use them to define the volume and thickness constraints. Note that we need more than 3 point in the spanwise direction `nSpan=25` because the case is 3D. The rule of thumb is that we should use a only a slightly larger number of sample points (in this case is 25 by 30 in the span and chord wise directions) as the FFD points. Here we also add leading and trailing edge constraints, e.g., `nom_add_LETEConstraint` to fix the leading and trailing edges. `volID` is the volume index for the FFD block. In this case we have only one block, so `volID=0`. `faceID="iLow"` means we make link displacements for the first layer of FFDs in the ith (x) direction. The top and bottom FFD move in the opposite directions for i=0, such that the leading edge does not move. Similarly, `faceID="iHigh"` means the last layer of FFDs in the ith direction.

  ```python
  leList = [[0.02, 0.0, 1e-3], [0.02, 0.0, 2.9]]
  teList = [[0.95, 0.0, 1e-3], [0.95, 0.0, 2.9]]
  self.geometry.nom_addThicknessConstraints2D("thickcon", leList, teList, nSpan=25, nChord=30)
  self.geometry.nom_addVolumeConstraint("volcon", leList, teList, nSpan=25, nChord=30)
  self.geometry.nom_add_LETEConstraint("lecon", volID=0, faceID="iLow")
  self.geometry.nom_add_LETEConstraint("tecon", volID=0, faceID="iHigh")
  ```

- We call the following functions to constrain the leading and trailing edge FFD movements by requiring them to move in the opposite directions. There is no need to manually set up the LE/TE linear constraints, as was done in the 2D airfoil case. Also, there is no need to impose symmetry constraints for k=0 and k=1 since this is a 3D wing case.

  ```python
  # Le/Te constraints
  DVCon.addLeTeConstraints(0, "iLow")
  DVCon.addLeTeConstraints(0, "iHigh")
  ```



{% include links.html %}

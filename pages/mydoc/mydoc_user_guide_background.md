---
title: DAFoam User Guide - Background
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_background.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## Constrained gradient-based optimization

DAFoam solves constrained nonlinear optimization problems using gradient-based optimization algorithms, with the gradients efficiently computed by the discrete adjoint method. In such problems, an objective function $f(\vec{x})$ is minimized by changing the design variables ($\vec{x}$), subject to certain constraints $\vec{g}(\vec{x})$ and $\vec{h}(\vec{x})$.

$$
\begin{aligned}
\text{minimize: } & f(\vec{x}), \\
\text{with respect to: } & \vec{x} \\
\text{subject to: } & \vec{h}(\vec{x}) = 0, \\
& \vec{g}(\vec{x}) \le 0.
\end{aligned}
$$

Here, $f$ is a scalar objective function to be minimized, and $\vec{x}$ is the vector of design variables, i.e., the variables we can modify in the design. $\vec{g}(\vec{x})$ and $\vec{h}(\vec{x})$ are the inequality and equality constraint functions, respectively. Here, we want to enforce $\vec{h}(\vec{x}) = 0$ and $\vec{g}(\vec{x}) \le 0$, thereby restricting the feasible design space. Note that $f$, $\vec{g}$, and $\vec{h}$ must be either explicit or implicit functions of the design variables $\vec{x}$.

A typical example is airfoil aerodynamic shape optimization, where the objective function is the drag coefficient $C_d$, the design variables $\vec{x}$ are control points that change the airfoil shape, and the constraints include a lift (equality) constraint ($C_l=0.5$) and a moment (inequality) constraint $C_m<b$. Here both the objective and constraint functions are implicit functions of the design variables.

{% include links.html %}

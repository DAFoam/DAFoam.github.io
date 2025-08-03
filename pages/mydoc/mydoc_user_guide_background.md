---
title: DAFoam User Guide - Background
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_background.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## 1. Constrained gradient-based optimization

### 1.1 Optimization problem formulation

DAFoam solves constrained nonlinear optimization problems using gradient-based optimization algorithms, with the gradients efficiently computed by the discrete adjoint method. In such problems, an objective function $f(\vec{x})$ is minimized by changing the design variables ($\vec{x}$), subject to certain constraints $\vec{g}(\vec{x})$ and $\vec{h}(\vec{x})$.

$$
\begin{aligned}
\text{minimize: } & f(\vec{x}), \\
\text{with respect to: } & \vec{x} \\
\text{subject to: } & \vec{h}(\vec{x}) = 0, \\
& \vec{g}(\vec{x}) \le 0.
\end{aligned}
$$

Here, $f$ is a scalar objective function to be minimized, and $\vec{x}$ is the vector of design variables, i.e., the variables we can modify in the design. $\vec{g}(\vec{x})$ and $\vec{h}(\vec{x})$ are the inequality and equality constraint functions, respectively. Here, we want to enforce $\vec{h}(\vec{x}) = 0$ and $\vec{g}(\vec{x}) \le 0$, thereby restricting the feasible design space. Note that $f$, $\vec{g}$, and $\vec{h}$ must be either explicit or implicit functions of the design variables $\vec{x}$. $f(\vec{x})$, $\vec{h}(\vec{x})$, and $\vec{g}(\vec{x})$ can be either linear or nonlinear functions.

A typical example is airfoil aerodynamic shape optimization, where the objective function is the drag coefficient $C_d$, the design variables $\vec{x}$ are control points that change the airfoil shape, and the constraints include a lift (equality) constraint ($C_l=0.5$) and a moment (inequality) constraint $C_m \le b$. Here both the objective and constraint functions are implicit functions of the design variables.

### 1.2 Iterative optimization process

In general, the above optimization problem can not be solved analytically, so we need to use an iterative approach to find the optimal solution $\vec{x}$. The iterative optimization process starts with an initial guess of the design variables $\vec{x}_0$, called initial design or baseline design. Then, an optimization algorithm compute a search direction and step size to update the design variable using

$$
\vec{x}^{n+1} = \vec{x}^n + \alpha^n \vec{d}^n
$$

Here $n$ is the optimization iteration number, $\alpha$ is a scalar step size, and $\vec{d}$ is the search direction vector.  $\vec{d}$ and  $\vec{x}$ have the same size. 

An optimizer typically first $\vec{d}$ is typically computed based on the gradients $\text{d}f/\text{d}\vec{x}$. 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/opt_process.png" width="200" />

{% include links.html %}

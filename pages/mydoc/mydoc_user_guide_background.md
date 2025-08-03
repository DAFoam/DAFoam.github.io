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

In general, the above optimization problem can not be solved analytically, so we need to use an iterative approach to find the optimal solution $\vec{x}$. The iterative optimization process starts with an initial guess of the design variables $\vec{x}_0$, called the initial design or baseline design. Then, an optimization algorithm computes a search direction and step size to update the design variable using

$$
\vec{x}^{n+1} = \vec{x}^n + \alpha^n \vec{d}^n
$$

Here $n$ is the optimization iteration number, $\alpha$ is a scalar step size, and $\vec{d}$ is the search direction vector.  $\vec{d}$ and  $\vec{x}$ have the same size. 

An example of iterative optimization processes for a 2D optimization problem is illustrated in the following figure. Here the x and y axes are the two design variables, and the contour denotes the value of the objective function. The baseline design $\vec{x}^0$ is located in the bottom left region of the 2D design space. The next design variables are computed using $\vec{x}^1=\vec{x}^0+\alpha^0 \vec{d}^0$. This process is repeated until the optimal design point ($\vec{x}^*$) is found.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/opt_process.png" style="width:500px !important;" />

### 1.3 Objective function evaluation

For simple optimization problems, the objective function ($f$) is an explicit function of the design variable $\vec{x}$, so we can directly compute the $f$ value for a given set of $\vec{x}$ values. However, for many engineering design problems, the objective function ($f$) is an implicit function of the design variable $\vec{x}$. In this case, $f$ depends on both the state variables $\vec{w}$ and design variable $\vec{x}$, and they are correlated by a governing equation $\vec{R}(\vec{w}, \vec{x})=0$. The objective function evaluation consists of two steps (see the following figure). 1. Use $\vec{x}$ as the input to solve the governing equation and obtain the converged state variable $\vec{w}$. 2. Use $\vec{x}$ and $\vec{w}$ as the inputs to compute $f(\vec{w}, \vec{x})$. In design optimization, we call the step 1 **the primal solution**. One example is to solve the Navier-Stokes governing equation to get the state variables (flow fields), and then use the flow fields (state variables) to compute the drag coefficient (objective function). We will discuss the details of primal solutions later.

<img src="{{ site.url }}{{ site.baseurl }}/images/xdsm/f_calculation.png" style="width:500px !important;" />

### 1.4 Search direction computation

The search direction $\vec{d}$ is typically computed based on the gradient vector $\nabla f = \text{d}f/\text{d}\vec{x}$. In the steepest descent optimization algorithm, the search direction is simply the opposite direction of the normalized gradient vector $\vec{d} = - \nabla f / || \nabla f ||$. For more advanced optimization algorithms, such as sequential quadratic programming (SQP), the search direction is typically a complex function of the gradient vector. For large-scale optimization problems with hundreds of design variables, computing gradients become computationally expensive. So, DAFoam uses the **discrete adjoint method** to efficiently compute the gradients, which will be discussed later.

### 1.5 Step size computation (line search)

Once the search direction $\vec{d}$ is computed, we need to take a step size to actually update the design variable. The step size determination is always a 1D problem, no matter how many design variables we have. So, this process is also called line search. The process typically starts with trying a default step size to update the design, i.e., $\vec{x}^{n+1} = \vec{x}^n + \alpha^\textrm{init} \vec{d}^n$. Then, we can use this new candidate design variable to evaluate $f$ (call the primal solution). If the objective function $f$ is reduced (the design is improved for this iteration), we accept the step size. Otherwise (i.e., $f$ increases instead of decreasing), we may reduce the step size by a factor, e.g., 0.1, and compute a new candidate design variable vector. This line search process will repeated until $f$ is reduced for this iteration. The line search ensures the objective function always reduces for all optimization iterations. Note that each line search iteration requires calling the primal solution once.

{% include links.html %}

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

DAFoam solves constrained nonlinear optimization problems using gradient-based optimization algorithms, with the gradients efficiently computed by the discrete adjoint method. In such problems, an objective function $f(\vec(x))$ is minimized by changing the design variables ($\vec{x}$), subject to certain constraints $\vec{g}(\vec{x})$ and $\vec{h}(\vec{x})$.

$$
\begin{aligned}
\text{minimize: } & f(\vec{x}), \\
\text{with respect to: } & \vec{x} \\
\text{subject to: } & \vec{h}(\vec{x}) = 0, \\
& \vec{g}(\vec{x}) \le 0.
\end{aligned}
$$

{% include links.html %}

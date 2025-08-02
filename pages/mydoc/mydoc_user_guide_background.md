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

DAFoam solves constrained nonlinear optimization problems using gradient-based optimization algorithms, with the gradients efficiently computed by the discrete adjoint method. In such problems, an objective function (\(f(x)\)) is minimized by changing the design variables ($x$), subject to certain constraints ($g(x)$, and $h(x)$).

\[
Changing x to:

minimize f(x),

subject to: 
h(x) = 0
g(x) \le 0
\]

{% include links.html %}

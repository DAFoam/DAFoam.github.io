---
title: OpenMDAO Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openmdao.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

OpenMDAO is an open-source optimization framework and a platform for building new analysis tools with analytic derivatives. DAFoam is coupled with OpenMDAO to perform MDO. To understand the basic of OpenMDAO, the following tutorial is presented. 

<img src="{{ site.url }}{{ site.baseurl }}/images/user_guide/example_xdsm.png" width="500" />

Fig. 1. Example eXtended Design Structure Matrix (XDSM). The red component is implicit
and the green one is explicit. The blue component is an independent variable that is not necessary for this optimization, but it shows how an independent variable component can be added to the system. The design variable is *x* and the objective function is *f*. *y* is the solution from the implicit component and is passed to the explicit component as
the input to compute *f*.



<img src="{{ site.url }}{{ site.baseurl }}/images/user_guide/example_n2.png" width="500" />

Fig. 2. The N2 diagram for the two-component optimization. 




{% include links.html %}

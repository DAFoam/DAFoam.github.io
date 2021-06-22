---
title: RAE2822 airfoil
keywords: validations, rae2822
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_validations_rae2822.html
folder: mydoc
---

This validation case examines the aerodynamic shape optimization of the RAE2822 airfoil. The flow conditions for the simulation are a Reynolds number of 6.5 million, Mach number of 0.729, and angle of attack of 2.31 degrees. Figure 1 displays the results of the simulation with a coarse mesh of 17,408 cells, a medium mesh of 60,672 cells, and a fine mesh of 108,675 cells along with the experimental data (Cook et al.,1979). The three simulations displayed in Figure 1 were run with the Spalart Allmaras turbulence model.

<img src="https://user-images.githubusercontent.com/86077528/122992939-b5852100-d374-11eb-90a4-67eebd3046f3.png" width="700" /> 

Fig. 1. The pressure distributions for simulations of various mesh cell numbers.

Figure 2 compares the experimental results (Cook et al.,1979) to simulations with the Spalart Allmaras and KOmegaSST turbulence models. Both of the simulations in Figure 2 have 60672 mesh cells.

<img src="https://user-images.githubusercontent.com/86077528/122993326-2cbab500-d375-11eb-9c87-93a6eb911355.png" width="700" />

Fig. 2. The pressure distributions for simulations of various turbulence models.

References 

Cook, P.H., M.A. McDonald, M.C.P. Firmin, "Aerofoil RAE 2822 - Pressure Distributions, and Boundary Layer and Wake Measurements," *Experimental Data Base for Computer Program Assessment*, AGARD Report AR 138, 1979.

{% include links.html %}

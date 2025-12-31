---
title: "DAFoam: An Open-Source Platform for Physics-Based Engineering Optimization"
keywords: DAFoam, OpenFOAM, adjoint, CFD, optimization, inverse problems, machine learning, AI, surrogate
sidebar: mydoc_sidebar
permalink: index.html
summary:
---

DAFoam (Discrete Adjoint for OpenFOAM) is an open, versatile, and efficient platform for solving physics-based (PDE-constrained) engineering optimization and inverse problems. DAFoam's salient features are as follows.

- **High-Fidelity Multidisciplinary Design Optimization**. (1) Adjoint-based aerodynamic, aero-structural, and aero-thermal optimization using high-fidelity CFD and FEA solvers, (2) Shape, topology, and operating-condition optimization with thousands of design variables and constraints, and (3) AI-agent–enabled, fully conversational design workflows, including geometry generation, meshing, simulations, and post-processing.

- **Machine Learning and Data Assimilation**. (1) RANS turbulence model defect corrections using field inversion machine learning (FIML), (2) Inference of initial and boundary conditions, geometries, material properties, and source terms using high-fidelity data, and (3) Accurate surrogate modeling for uncertainty quantification and interactive design-space exploration.

- **Open, Extensible, and Vibrant Ecosystem**. (1) A modular architecture to add customized disciplines/solvers, design variables, objective functions, and constraints, (2) Long-term community support through the GitHub Discussions forum and one-on-one meetings for new user and developer onboarding, and (3) Comprehensive documentation and tutorials, hands-on workshops, and user and developer guides.

- **Demonstrated Breadth and Impact**. (1) DAFoam has been used to design various engineered systems, including aircraft, wind turbines, hydroturbines, automobiles, ships, heat exchangers, and medical devices, (2) External researchers from 10+ countries use DAFoam in their research, resulting in about 20 DAFoam-publications per year, and (3) DAFoam has received support from major funding agencies and industry partners, including NSF, NASA, and Ford

DAFoam source code is available on [GitHub](https://github.com/mdolab/dafoam), and it interfaces with several open-source tools, including [OpenFOAM](https://www.openfoam.com), [MACH-Aero](https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/index.html), and [OpenMDAO](https://openmdao.org). Follow the rest of the steps in Get Started to run your first DAFoam case.


<div markdown="0" id="carousel" class="carousel slide" data-ride="carousel" data-interval="2000" data-pause="hover" >
    <!-- Menu -->
    <ol class="carousel-indicators">
        <li data-target="#carousel" data-slide-to="0" class="active"></li>
        <li data-target="#carousel" data-slide-to="1"></li>
        <li data-target="#carousel" data-slide-to="2"></li>
        <li data-target="#carousel" data-slide-to="3"></li>
        <li data-target="#carousel" data-slide-to="4"></li>
        <li data-target="#carousel" data-slide-to="5"></li>
    </ol>

    <!-- Items -->
    <div class="carousel-inner" markdown="0">
        <div class="item active">
            <img src="{{ site.url }}{{ site.baseurl }}/images/slider7001400/DPW6Flow.png" alt="Slide 1" />
        </div>
        <div class="item">
            <img src="{{ site.url }}{{ site.baseurl }}/images/slider7001400/propeller_wakes.png" alt="Slide 2" />
        </div>
        <div class="item">
            <img src="{{ site.url }}{{ site.baseurl }}/images/slider7001400/Rotor67AeroStructCover.png" alt="Slide 3" />
        </div>
        <div class="item">
            <img src="{{ site.url }}{{ site.baseurl }}/images/slider7001400/UBendAeroThermal.png" alt="Slide 4" />
        </div>
        <div class="item">
            <img src="{{ site.url }}{{ site.baseurl }}/images/slider7001400/drivAerStreamline.png" alt="Slide 5" />
        </div>    
        <div class="item">
            <img src="{{ site.url }}{{ site.baseurl }}/images/slider7001400/JBC_front_page.png" alt="Slide 6" />
        </div>    
    </div>
</div>


{% include links.html %}

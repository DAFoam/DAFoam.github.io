---
title: "DAFoam: An Open-Source Platform for Physics-Based Engineering Optimization"
keywords: DAFoam, OpenFOAM, adjoint, CFD, optimization, inverse problems, machine learning, AI, surrogate
sidebar: mydoc_sidebar
permalink: index.html
summary:
---

DAFoam (Discrete Adjoint for OpenFOAM) is an open, versatile, and efficient platform for solving physics-based (PDE-constrained) engineering optimization and inverse problems. DAFoam's salient features are:

- **High-Fidelity Multidisciplinary Design Optimization**. (1) Adjoint-based [aerodynamic](https://dafoam.github.io/tutorials-aero-naca0012-incompressible.html), [aero-structural](https://dafoam.github.io/tutorials-aerostruct-mach-wing.html), and [aero-thermal](https://dafoam.github.io/tutorials-heat-ubend-circular.html) optimization using high-fidelity CFD and FEA solvers, (2) Shape, [topology](https://dafoam.github.io/tutorials-topo-channel-cht.html), and operating-condition optimization with hundreds of design variables and constraints, and (3) [AI-agent](https://dafoam.github.io/ai-agent-overview.html) enabled, fully conversational design workflows, including geometry generation, meshing, simulations, and post-processing.

- **Machine Learning and Data Assimilation**. (1) RANS turbulence model defect corrections using field inversion machine learning ([FIML](https://dafoam.github.io/tutorials-fieldinversion-ramp.html)), (2) [Data assimilation](https://dafoam.github.io/tutorials-da-naca0012.html) to infer geometries, initial/boundary conditions, and model parameters/terms, and (3) Accurate surrogate modeling for uncertainty quantification and digital twins.

- **Open, Extensible, and Vibrant Ecosystem**. (1) A modular architecture to add customized disciplines/solvers, design variables, objective functions, and constraints, (2) Long-term community support through the [Discussions Forum](https://github.com/mdolab/dafoam/discussions) and one-on-one meetings for new user and developer onboarding, and (3) Comprehensive documentation and [tutorials](https://dafoam.github.io/tutorials-overview.html), hands-on [workshops](https://dafoam.github.io/workshops.html), and user and developer [guides](https://dafoam.github.io/user-guide-overview.html).

- **Demonstrated Breadth and Impact**. (1) DAFoam has been used to design various engineered systems, including aircraft, wind turbines, hydro-turbines, automobiles, ships, heat exchangers, and medical devices, (2) External researchers from 10+ countries use DAFoam in their research, resulting in about 20 [DAFoam-publications](https://dafoam.github.io/publications.html) per year, and (3) DAFoam has received [funding support](https://dafoam.github.io/acknowledgement.html) from federal agencies and industry partners, including NSF, NASA, and Ford

DAFoam source code is available on [GitHub](https://github.com/mdolab/dafoam), and it interfaces with several open-source tools, including [OpenFOAM](https://www.openfoam.com), [MACH-Aero](https://mdolab-mach-aero.readthedocs-hosted.com/en/latest/index.html), and [OpenMDAO](https://openmdao.org). You can follow the remaining steps in "Get Started" to run your first DAFoam optimization.


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

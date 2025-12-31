---
title: "DAFoam: An Open-Source Platform for Physics-Based Engineering Optimization"
keywords: DAFoam, OpenFOAM, adjoint, CFD, optimization, inverse problems, machine learning, AI, surrogate
summary: 
sidebar: mydoc_sidebar
permalink: test-home.html
folder: mydoc
---

DAFoam (Discrete Adjoint for OpenFOAM) is an open, versatile, and efficient platform for solving physics-based (PDE-constrained) engineering optimization and inverse problems.

### What Can DAFoam Do?

- **High-Fidelity Multidisciplinary Design Optimization**
  - Perform gradient-based aerodynamic, aero-structural, and aero-thermal optimization by coupling computational fluid dynamics (CFD) and finite-element analysis (FEA) solvers
  - Enable shape, topology, and operating-condition optimization with thousands of design variables and constraints through discrete adjoint methods
  - Support AI-agent–enabled, fully conversational design workflows, including geometry generation, meshing, simulations, and post-processing

- **Machine Learning and Data Assimilation**
  - Correct Reynolds-Averaged Navier-Stokes (RANS) turbulence model deficiencies using model-consistent field inversion and machine learning (FIML)
  - Infer initial and boundary conditions, geometries, material properties, and source terms using experimental or high-fidelity numerical data
  - Generate comprehensive simulation datasets and train accurate surrogate models for uncertainty quantification and interactive design-space exploration

### Why Should You Choose DAFoam?

- **Open, Extensible, and Vibrant Ecosystem**
  - Feature a modular architecture to add customized physical disciplines/solvers, design variables, objective functions, and constraints
  - Provide long-term community support through the GitHub Discussions forum and one-on-one meetings for new user and developer onboarding
  - Offer comprehensive documentation and tutorials, along with hands-on workshops and user and developer guides

- **Demonstrated Breadth and Impact**
  - DAFoam has been used to design a wide range of engineered systems, including aircraft, wind turbines, hydroturbines, automobiles, ships, heat exchangers, and medical devices
  - Researchers from more than 10 countries have published over 40 peer-reviewed journal and conference papers using DAFoam
  - DAFoam has received support from major funding agencies and industry partners, including NSF, NASA, and Ford

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

<div markdown="span" class="alert alert-info" role="alert"><i class="fa fa-info-circle"></i> 
<b>[Latest Announcements](news.html):</b>   
{% for post in site.posts limit:3 %}
  {{ post.date | date: "%m/%d/%Y" }}. {{ post.title }}. <a href="{{ post.permalink }}">Details.</a>  
{% endfor %}
</div>


{% include links.html %}

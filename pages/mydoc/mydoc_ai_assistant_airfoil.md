---
title: Airfoil
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_ai_assistant_airfoil.html
folder: mydoc
---

Once the DAFoam MCP server is installed and connected to Claude, you can open the Docker Desktop and the Claude Desktop app, and start using it to analyze and optimize airfoil cases. We support three functionalities.

## Airfoil mesh generation. 

- Mesh generation. To generate an airfoil mesh, you can ask Claude: "Generate a mesh for the NACA0012 airfoil". Once Claude generates the mesh, you can click the provided link to view the mesh in your browser. You can ask it to generate meshes a different airfoil profile. If the airfoil profile is not included in the DAFoam MCP server, it will automatically download it from the UIUC dataset.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-mesh-0012.png" style="width:700px !important;" />


- Mesh visualization. You can say "View the airfoil mesh near the trailing edge" to zoom in the generated mesh. You can also ask Claude to zoom in more to view more details.

- Change mesh parameters. You can prescribe the desired number of mesh cells and the desired yPlus (to get a good estimation of the yPlus, you also need to give a reference Mach number). For example, you can say "Generate a mesh for NACA4412 with 20K cells, yPlus=1, and Ma=0.3". If you do not prescribe the details, Claude will use default mesh parameters.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-mesh-4412.png" style="width:700px !important;" />

## Airfoil aerodynamic analysis.

- Run CFD simulations. You can ask Claude: "Run a CFD simulation with aoa=3, Ma=0.1, Re=1e6". Claude will run the CFD simulation in the background. 

- Ask CFD run status. You can say "Check run status" to see if the CFD finishes.

- Monitor convergence. If the CFD is running in the background, you can ask "View the CFD convergence" and click the provided link to visualize the residual and function convergence history.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-cfd-convergence.png" style="width:700px !important;" />

- View pressure profile. If the CFD finishes, you can ask Claude to plot the pressure profile.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-cfd-view-pressure.png" style="width:700px !important;" />

- View flow field. You can say "View the velocity field" to see velocity profile. You can also ask Claude to "View the turbulence field and zoom in to the trailing edge". Click the provided link to see the contours in your browser.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-cfd-view-nut.png" style="width:700px !important;" />

## Airfoil aerodynamic optimization. 

- Run optimization. You can ask Claude: "Run an optimization with CL constraint 0.5, Ma=0.1, Re=1e6". Claude will run the optimization in the background. 

- Ask optimization run status. You can say "Check run status" to see if the optimization finishes.

- Monitor convergence. If the optimization is running in the background, you can ask "View the optimization convergence history" and click the provided link to visualize the convergence history of CD, CL, CM, etc.

- View pressure profile or variable. You can ask Claude to plot the pressure profile or any flow fields.

{% include links.html %}

---
title: Wing agent
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-wing.html
folder: mydoc
---

Here we demonstrate how to use the AI agent for wing aerodynamic design on an HPC system. Please follow the instructions in Overview–>HPC Installation to set up the DAFoam MCP server and Claude Code. In this example, we use Iowa State University’s Nova HPC as the reference system.

## Connecting to the HPC Using VS Code Remote SSH

The recommended way to connect to an HPC when using the DAFoam MCP server is via the **VS Code Remote SSH** extension. This approach is supported on Windows, macOS, and Linux.

- First, download VS Code 1.100.3 from [here](https://code.visualstudio.com/updates/v1_100).  
  **NOTE:** Some newer versions of VS Code may experience issues when connecting to HPC systems.

- Open VS Code. From the left panel, click `Extensions`, then search for `Remote SSH` by Microsoft and click `Install`.

- After installing Remote SSH, set up the SSH connection: (1) Click the blue `Open a Remote Window` button in the lower-left corner of VS Code. (2) In the pop-up window on the top, select `Connect to Host`, then choose `+ Add New SSH Host`. (3) In the pop-up window, enter your SSH command, for example: `ssh my_user_name@nova.its.iastate.edu`. (4) When prompted, select the SSH configuration file to update (choose `~/.ssh/config` or similar).

- Once the SSH configuration is complete, click `Connect to Host` again and select your newly added host (e.g., `nova.its.iastate.edu`). You will be prompted to enter your password and, if applicable, a verification code to log in to the HPC.

- After successfully logging in, click `Open Folder` in the left panel and navigate to the path of your `dafoam_mcp_server` repository. This enables: (1) Access to an integrated terminal on the HPC, (2) Browsing and editing all files in the repository, and (3) Viewing any opened files within VS Code. If the terminal is not visible after opening the folder, click `Toggle Panel` in the top-right corner of VS Code. An example of VS Code Remote SSH connected to the Nova HPC is shown below.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-vscode-hpc-login.png" style="width:700px !important;" />

## Wing geometry and mesh generation. 

- Geometry generation. To generate the CAD wing geometry mesh, you can ask Claude: "Generate a wing with the NACA0012 at the root and NACA4412 at the tip. The span is 3 m. The root chord is 1 m, and the tip chord is 0.7 m. The root has a twist of 2 degs.". Once Claude generates the mesh, you can click the provided link to view the geometry in your browser.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-geometry.png" style="width:700px !important;" />


- Mesh generation. To generate the wing mesh, you can ask Claude: "Generate a mesh for the wing". Once Claude generates the mesh, you can click the provided link to view the mesh in your browser. To adjust the mesh density, you can change the mesh refinement level, number of boundary layer mesh, and far field mesh size.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-mesh.png" style="width:700px !important;" />

  You can also click the provided link "Interactive 3D View" to open a web brower to view the mesh using Trame. In Trame, you can zoom, rotate, traslate the view to visualize more details of the mesh.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-mesh-trame.png" style="width:700px !important;" /> 

## Wing aerodynamic analysis.

- Run CFD simulations. You can ask Claude: "Run a CFD with Ma=0.5, Re=1e6, and aoa=1.5 deg". Claude will run the CFD simulation in the background. 

- Ask CFD run status. You can say "Check run status" to see if the CFD finishes.

- Monitor convergence. If the CFD is running in the background, you can ask "View the CFD convergence" and click the provided link to visualize the residual and function convergence history.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-cfd-convergence.png" style="width:700px !important;" />

- View pressure profile. If the CFD finishes, you can ask Claude to plot the pressure profile.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-pressure-profile.png" style="width:700px !important;" />

- View flow field. You can say "View the pressure field" to see the pressure profile. Click the provided link to see the contours in your browser.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-pressure.png" style="width:700px !important;" />


{% include links.html %}

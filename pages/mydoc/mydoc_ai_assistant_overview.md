---
title: Overview
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_ai_assistant_overview.html
folder: mydoc
---

The DAFoam MCP server enables the pre-processing, simulations, optimization, and post-processing of various DAFoam-based optimization cases. Currently, we support only airfoil cases and the DAFoam MCP server is in the first beta version.

## Installation

Install the MCP server (airfoils)

- Download and install the Docker Desktop for [MacOS](https://docs.docker.com/desktop/setup/install/mac-install) or [Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Open Docker Desktop and keep it open.
- Open a Terminal (MacOS) or Command Prompt (Windows). Run the following command to download the DAFoam Docker image:
  <pre>
  docker pull dafoam/opt-packages:latest
  </pre>
- Run the following command to download the dafoam_mcp_server repo from GitHub

  <pre>
  git clone https://github.com/dafoam/dafoam_mcp_server.git
  </pre>
  Alternative: If you don't have git, you can also download the repo from [here](https://github.com/dafoam/dafoam_mcp_server/archive/refs/heads/main.zip) and unzip it. Then, rename the unzipped folder to dafoam_mcp_server.
  
- Open a Terminal (MacOS) or Command Prompt (Windows) and cd into the `dafoam_mcp_server` directory, then run the following to build the dafoam_mcp_server docker image
  <pre>
  docker build -t dafoam_mcp_server . 
  </pre>

Connect the DAFoam MCP server to a client (Claude).

- Download and install the Claude Desktop from https://www.claude.com/download. Open Claude Desktop (you may need to sign up for an account).
- In Claude Desktop, locate to the bottom left and click: "Your Account->Settings->Developer". Then, click "Edit Config", this will open a directory where Claude saves your claude_desktop_config.json file. 
- Open claude_desktop_config.json and add the following lines into it. **NOTE:** you need to replace `abs_path_to_your_dafoam_mcp_server` with the absolute path of the dafoam_mcp_server folder on your local system. For example, you may use `/Users/phe/Desktop/dafoam_mcp_server:/home/dafoamuser/mount` for MacOS and `C:\\Users\\phe\\Desktop\\dafoam_mcp_server:/home/dafoamuser/mount` for Windows (we need to use double slash in the path for Windows!). The DAFoam MCP will make modifications ONLY in this dafoam_mcp_server folder.

  <pre>
  {
    "mcpServers": {
      "dafoam_mcp_server": {
        "command": "docker",
        "args": [
          "run", 
          "-i", 
          "--rm",
          "-p",
          "8001:8001",
          "-v", 
          "/abs_path_to_your_dafoam_mcp_server:/home/dafoamuser/mount",
          "dafoam_mcp_server"
        ]
      }
    }
  }
  </pre>

- IMPORTANT! You need to close and re-open Claude Desktop to make the new MCP effective.

- The airfoil MCP is ready to use in Claude Desktop. To run your first case. Ask Claude: "Generate a mesh for the NACA0012 airfoil". Once Claude generates the mesh, you can click the provided link to view the mesh in your browser. Then, ask: "Run a CFD simulation with aoa=3". Claude will run the CFD simulation in the background. Then, you can ask "View the CFD convergence" and click the provided link to visualize the residual and function convergence history.

For developers: If you see an error, the logs file are in ~/Library/Logs/Claude/mcp-server-dafoam_mcp_server.log 


{% include links.html %}

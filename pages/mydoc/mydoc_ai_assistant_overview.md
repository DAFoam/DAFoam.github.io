---
title: Overview
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_ai_assistant_overview.html
folder: mydoc
---

The DAFoam AI Assistant enables the conversational pre-processing, simulations, optimization, and post-processing of various DAFoam cases. Currently, we support only airfoil cases with the Claude LLM. The DAFoam MCP server is in the beta state.

## Installation

Install the MCP server

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

- Download and install the Claude Desktop from [here](https://www.claude.com/download). Open Claude Desktop (you may need to sign up for an account).
- In Claude Desktop, locate to the bottom left and click: "Your Account->Settings->Developer". If you don't see this in Claude Desktop, go to the top left and lick "Toggle Sidebar". Then, click "Edit Config", this will open a directory where Claude saves your claude_desktop_config.json file. **NOTE:** If there is an empty bracket when you open the .json file (something like "{}"), this MUST be deleted.  
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
          "--platform",
          "linux/amd64",
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

- IMPORTANT! You need to close and re-open Claude Desktop to make the new MCP effective. **NOTE:** On Mac, you may need to Force Quit the Claude desktop application before you re-open it.

For developers: If you see an error, the logs file are in ~/Library/Logs/Claude/mcp-server-dafoam_mcp_server.log 


{% include links.html %}

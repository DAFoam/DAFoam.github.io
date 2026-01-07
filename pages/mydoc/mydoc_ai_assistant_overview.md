---
title: Overview
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-overview.html
folder: mydoc
---

The DAFoam AI Agent enables the conversational pre-processing, simulations, optimization, and post-processing of various DAFoam cases. Currently, we support only airfoil and wing cases with the Claude LLM. The AI agent can be installed locally or on the HPC.

## Local Installation

The local installation works for Linux, Windows, and MacOS and consist of the following two steps.

### Install the DAFoam MCP server using Docker

- Download and install the Docker Desktop for [MacOS](https://docs.docker.com/desktop/setup/install/mac-install) or [Windows](https://docs.docker.com/desktop/setup/install/windows-install/). Open Docker Desktop and keep it open.
- Open a Terminal (MacOS) or Command Prompt (Windows). Run the following command to download the DAFoam Docker image. NOTE: if you have preciously downloaded the `dafoam/opt-packages:latest` image, delete it and re-download to ensure you have the latest.
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

### Connect the DAFoam MCP server to the LLM client (Claude Desktop).

- Download and install the Claude Desktop from [here](https://www.claude.com/download). Open Claude Desktop (you may need to sign up for an account).
- In Claude Desktop, locate to the top left and click "Toggle sidebar", and then locate to the bottom left and click: "Your Account->Settings->Developer". Then, click "Edit Config", this will open a directory where Claude saves your claude_desktop_config.json file. **NOTE:** If there is an empty bracket when you open the .json file (something like "{}"), this MUST be deleted.  
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
          "--name",
          "dafoam_mcp_server",
          "--platform",
          "linux/amd64",
          "-p",
          "8001:8001",
          "-p",
          "8002:8002",
          "-v", 
          "/abs_path_to_your_dafoam_mcp_server:/home/dafoamuser/mount",
          "dafoam_mcp_server"
        ]
      }
    }
  }
  </pre>

- IMPORTANT! You need to close and re-open Claude Desktop to make the new MCP effective. **NOTE:** On Mac and Windows, you may need to Force Quit the Claude desktop application before you re-open it. Once the Claude Desktop is re-open, you can click the "Search and Tools" button to verify if the DAFoam MCP server is running. See the picture below. For developers: If you see an error, the logs file are in ~/Library/Logs/Claude/mcp-server-dafoam_mcp_server.log 

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI_Check_DAFoam_MCP_Server.png" style="width:500px !important;" />

- Occasionally, you may see the error shown below when opening the Claude Desktop app. If this happens, the DAFoam MCP server is not loading properly. You can simply force-quit Claude and reopen it. The error should disappear.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-claude-error.png" style="width:400px !important;" />


## HPC Installation

### Connecting to the HPC Using VS Code Remote SSH

The recommended way to connect to an HPC when using the DAFoam MCP server is via the **VS Code Remote SSH** extension. This approach is supported on Windows, macOS, and Linux.

- First, download VS Code 1.100.3 from [here](https://code.visualstudio.com/updates/v1_100).  
  **NOTE:** Some newer versions of VS Code may experience issues when connecting to HPC systems.

- Open VS Code. From the left panel, click `Extensions`, then search for `Remote SSH` by Microsoft and click `Install`.

- After installing Remote SSH, set up the SSH connection: (1) Click the blue `Open a Remote Window` button in the lower-left corner of VS Code. (2) In the pop-up window on the top, select `Connect to Host`, then choose `+ Add New SSH Host`. (3) In the pop-up window, enter your SSH command, for example: `ssh my_user_name@nova.its.iastate.edu`. (4) When prompted, select the SSH configuration file to update (choose `~/.ssh/config` or similar).

- Once the SSH configuration is complete, click `Connect to Host` again and select your newly added host (e.g., `nova.its.iastate.edu`). You will be prompted to enter your password and, if applicable, a verification code to log in to the HPC.

- After successfully logging in, click `Open Folder` in the left panel and navigate to the path of your `dafoam_mcp_server` repository. This enables: (1) Access to an integrated terminal on the HPC, (2) Browsing and editing all files in the repository, and (3) Viewing any opened files within VS Code. If the terminal is not visible after opening the folder, click `Toggle Panel` in the top-right corner of VS Code. An example of VS Code Remote SSH connected to the Nova HPC is shown below.

  <img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-wing-vscode-hpc-login.png" style="width:700px !important;" />

### Setup DAFoam, Claude Code, and MCP Server

- Login into your HPC through VS Code Remote SSH. cd into your \$HOME directory (e.g., `/home/my_user_name`). Here we use the \$HOME directory installation as an example, you can also install DAFoam MCP server and DAFoam packages into a different directory.

- Compile DAFoam from source, follow the instructions from [here](https://dafoam.github.io/installation-source.html). Here we assume DAFoam is compiled in /home/my_user_name/dafoam.

- Run the following command to download the dafoam_mcp_server repo into /home/my_user_name

  <pre>
  git clone https://github.com/dafoam/dafoam_mcp_server.git
  </pre>

  
- cd into the /home/my_user_name/dafoam_mcp_server directory and change the base_path in dafoam_mcp_server.py to `/home/my_user_name/dafoam_mcp_server`

- You also need to modify the job submission sbatch script `myJob.sh` in the airfoils and wings folder according to your HPC setup. You need to replace line 10 in `myJob.sh` with the absolute path of your DAFoam package's `loadDAFoam.sh` file on the HPC. 

- Install the Claude code by running the following command. Here the install.sh will automatically detect your system and copy the claude code exe into your `~/.local/bin` directory. It will also add `~/.local/bin` to your \$PATH variable in `~/.bash_profile`. In some HPCs, you may need to manually add `~/.local/bin` to your \$PATH in your `~/.bashrc`.

  <pre>
  curl -fsSL https://claude.ai/install.sh | bash
  </pre>

  Important! You need to verify your claude installation by running this command from the terminal.

  <pre>
  claude -v
  </pre>

  You should see your claude version printed on the terminal.

- After the claude code is installed, you need to add the DAFoam MCP server information by running the following command. Here we need to provide the absolute paths on the HPC for the loadDAFoam.sh script (this script should be generated after you compile DAFoam from source) and the dafoam_mcp_server.py file (this file should be in the dafoam_mcp_server folder).

  <pre>
  claude mcp add --transport stdio dafoam_mcp_server -- bash -c "source /home/my_user_name/dafoam/loadDAFoam.sh && python /home/my_user_name/dafoam_mcp_server/dafoam_mcp_server.py"
  </pre>

  The above command will add relevant MCP information into the claude code configuration file in `~/.claude.json`. You don't need to manually change `~/.claude.json`.

- Verify the MCP installation by running

  <pre>
  claude mcp list
  </pre>

  You should see the dafoam_mcp_server is "connected". Important, please verify you see the mcp server connected before running any simulations.

{% include links.html %}

---
title: Installation
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-installation.html
folder: mydoc
---

The AI agent can be installed locally or on an HPC. If you are new to the MDO Agent Deck, we recommend starting with the local installation.

## Installation (local computers)

The local installation works for Linux, Windows, and MacOS, and it is the easiest way to run the agents with small cases. If you plan to run larger cases, e.g., wing aero-structural optimization, you need to install the agents on an HPC.

### Step 1. Install a LLM client

We need to first install an LLM client's command line interface (CLI). The MDO Agent Deck supports three LLM clients: Codex, Claude Code, and Gemini, but here you need to install **ONLY ONE** CLI client, and the Codex CLI is recommended.

**MacOS/Linux (Terminal):**

Codex CLI: `npm install -g @openai/codex`

Claude code CLI: `curl -fsSL https://claude.ai/install.sh | bash`

Gemini CLI: `npm install -g @google/gemini-cli`

**Windows CMD (Command Prompt):**

Codex CLI: `npm install -g @openai/codex`

Claude code CLI: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`

Gemini CLI: `npm install -g @google/gemini-cli`


### Step 2. Install VSCode

Download VS Code 1.100.3 from [here](https://code.visualstudio.com/updates/v1_100). **NOTE:** Some newer versions of VS Code may experience issues when connecting to HPC systems. 

Optional: For VSCode on Windows, you can configure your terminal to use CMD by opening the Command Palette from the top panel, searching for "Terminal: Select Default Profile", and then selecting CMD.

### Step 3. Install Docker Desktop

Download and install Docker Desktop App for [MacOS](https://docs.docker.com/desktop/setup/install/mac-install), [Windows](https://docs.docker.com/desktop/setup/install/windows-install), or [Linux](https://docs.docker.com/desktop/setup/install/linux)

After the Docker Desktop is installed, open it and keep it open.

Then, open a terminal and run the following command to download the pre-compiled MDO Agent Deck image:

`docker pull dafoam/agent:latest`

### Step 4. Download the working directory

Download `mdo_agent_results` repo from [here](https://github.com/DAFoam/mdo_agent_results/archive/refs/heads/main.zip). 

Unzip it and you will see a folder called `mdo_agent_results-main`. Rename it to `mdo_agent_results`. This will be the main working directory for your agents. 

**IMPORTANT**: Do not manually create a folder and use it as the LLM's working directory. You must use `mdo_agent_results`. This is because `mdo_agent_results` contains pre-defined LLM configuration files (hidden by default). You do not need to modify these configuration files.

The local installation is finished!

## Installation (HPC)

This section is for running large-scale cases on an HPC. If you are using the local installation and running the agents on your local computer, you do not need to follow these steps.

### Step 1. Install VSCode and Remote SSH

Download VS Code 1.100.3 from [here](https://code.visualstudio.com/updates/v1_100). **NOTE:** Some newer versions of VS Code may experience issues when connecting to HPC systems. 

Open VS Code. From the left panel, click `Extensions` (see Fig. 1 below), then search for `Remote SSH` by Microsoft and click `Install`.

After installing Remote SSH, set up the SSH connection: 

- Click the `Open a Remote Window` button in the lower-left corner of VS Code (see Fig. 1 below).

- In the pop-up window on the top, select `Connect to Host`, then choose `+ Add New SSH Host`. 

- In the pop-up window, enter your SSH command, for example: `ssh my_user_name@nova.its.iastate.edu`.

- When prompted, select the SSH configuration file to update (choose `~/.ssh/config` or similar).

- Once the SSH configuration is complete, click `Connect to Host` again and select your newly added host (e.g., `nova.its.iastate.edu`). You will be prompted to enter your password and, if applicable, a verification code to log in to the HPC.

- If the terminal is not visible after opening the folder, click `Toggle Panel` in the top-right corner of VS Code (see Fig. 1 below).

DO NOT close the VSCode and the opened terminal on the HPC, we will use it to install other packages in the following.

### Step 2. Install a LLM client on the HPC

Using the terminal in VSCode via Remote SSH, we need to install an LLM client's command line interface (CLI) on the HPC. The MDO Agent Deck supports three LLM clients: Codex, Claude Code, and Gemini, but you only need to install **ONE** CLI client. The Codex CLI is recommended.

Codex CLI: `npm install -g @openai/codex`

Claude code CLI: `curl -fsSL https://claude.ai/install.sh | bash`

Gemini CLI: `npm install -g @google/gemini-cli`

### Step 3. Install the agents and DAFoam on the HPC

Using the terminal in VSCode via Remote SSH, we need to compile the DAFoam package from scratch. Follow the instructions from [here](https://dafoam.github.io/installation-source.html). In this example, we assume DAFoam is installed in `/home/your_user_name/dafoam`.

After DAFoam is compiled, load its environment, e.g., `source /home/your_user_name/dafoam/loadDAFoam.sh`, and then run the following command to install the MDO Agent Deck:

`pip install mdo_agent_deck`

Here mdo_agent_deck is hosted on PyPI. 

### Step 4. Create the working directory

Using the terminal in VSCode via Remote SSH, we need to create a working directory called `mdo_agent_results` on the HPC, for example at `/home/your_user_name/mdo_agent_results`.

Next, create MCP configuration files in the `mdo_agent_results` folder. Follow **ONLY ONE** of the approaches below, depending on which LLM client you are using.

**Codex**

First, create a new subfolder called `.codex` inside `mdo_agent_results`, and then, create a new file called `config.toml` inside `mdo_agent_results/.codex`. Finally, add the following to your `mdo_agent_results/.codex/config.toml` file. 

```bash
[mcp_servers.mdo_agent_deck]
command = "bash"
args = ["-c", ". /replace_this_with_the_abs_path_to_your_loadDAFoam.sh && mdo-agent-deck-mcp"]
```

**IMPORTANT**: You need to replace `/replace_this_with_the_abs_path_to_your_loadDAFoam.sh` with the absolute path of your loadDAFoam.sh file on the HPC, e.g., `/home/your_user_name/dafoam/loadDAFoam.sh`

**Claude Code**

First, create a new file called `.mcp.json` inside `mdo_agent_results`. Next, add the following to your `mdo_agent_results/.mcp.json` file. 

```bash
{
    "mcpServers": {
        "mdo_agent_deck": {
          "type": "stdio",
          "command": "bash",
          "args": [
            "-c",
            ". /replace_this_with_the_abs_path_to_your_loadDAFoam.sh && mdo-agent-deck-mcp"
          ],
          "env": {}
        }
    }
}
```

**IMPORTANT**: You need to replace `/replace_this_with_the_abs_path_to_your_loadDAFoam.sh` with the absolute path of your loadDAFoam.sh file on the HPC, e.g., `/home/your_user_name/dafoam/loadDAFoam.sh`


**Gemini**

First, create a new subfolder called `.gemini` inside `mdo_agent_results`, and then, create a new file called `settings.json` inside `mdo_agent_results/.gemini`. Finally, add the following to your `mdo_agent_results/.gemini/settings.json` file. 

Put the same content in `mdo_agent_results/.gemini/settings.json` as in `mdo_agent_results/.mcp.json` above. Remember to change `/replace_this_with_the_abs_path_to_your_loadDAFoam.sh` accordingly.


### Step 5. Edit the MDO Agent Deck config

Navigate to where mdo_agent_deck is installed in Miniconda. An example is `/home/your_user_name/dafoam/packages/miniconda3/lib/python3.10/site-packages/mcp_server.py`.

Open `mcp_server.py` and set `run_mode` to either `"HPC"` (submit a job from the head node) or `"Native"` (interactive compute nodes). Also set `work_dir` to the absolute path of the `mdo_agent_results` working directory. An example is as follows:

```python
AGENT_DECK_CONFIG = {
    "run_mode": "HPC",
    "work_dir": "/homme/your_user_name/mdo_agent_results",
    "load_modules": "",
}
```

The agents are ready to use on the HPC

## Test the agent

The following steps work for both local and HPC installations.

**IMPORTANT**: The MCP server setup works only in the `mdo_agent_results` folder.

First, open VSCode. For HPC installation, you need to use Remote SSH to connect to the HPC. No need to do such for local installation.

Then, in VSCode, click the "Explorer" icon from the left bar (see Fig. below). From there, you can select "Open Folder" and open the `mdo_agent_results` folder as your working directory.

Next, click the "Toggle Panel" button in the top right corner to open a terminal (see Fig. 1 below).

In the terminal, navigate to the `mdo_agent_results` folder. If you use the HPC or Native mode, you need to load the DAFoam environment. No need to do such for the Docker mode.

Then, launch your LLM client in full-permission mode to avoid interruptions. Choose **ONLY ONE** of the following, depending on which LLM client you are using.

Claude Code: `claude --dangerously-skip-permissions`

Codex: `codex --yolo`

Gemini: `gemini --yolo`

If this is the first time you add a new MCP server, your client may show a "New MCP server found" prompt. Choose "Use this MCP server".

Some LLM clients may also warn you about the skipped-permissions setup. You can allow it if needed. If you prefer, you can omit the `--dangerously-skip-permissions` or `--yolo` arguments.

Then, run `/mcp` and verify if the `mdo_agent_deck` is `connected`. If yes, you can start asking questions.

You can ask something like:

"Generate a CFD mesh for the NACA0012 airfoil with 20K cells with yPlus 5."

The agent will parse your prompt into solver input arguments and run predefined commands to generate the mesh, then return clickable paths to the mesh figures along with a summary of the mesh. You can hold the Command key (MacOS) or Control key (Windows and Linux) and click these paths to view the figures directly in VSCode (see Fig. 1 below).

The agent will also return a clickable link for a Trame server to view the mesh interactively. You can open this server from your default browser by clicking the link.

For the best visual experience, we recommend using the "Light Modern" color theme in VSCode. To change the theme, open the Command Palette in VSCode, search for "Preferences: Color Theme", and select "Light Modern".

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-local-vscode.png" style="width:600px !important;" />

Fig. 1. An example of VSCode interface on local computers

{% include links.html %}

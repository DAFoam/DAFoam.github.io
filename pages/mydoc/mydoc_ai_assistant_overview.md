---
title: Overview of MDO Agent Deck
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-overview.html
folder: mydoc
---

The MDO Agent Deck is an agentic AI framework that enables the conversational pre-processing, simulation, optimization, and post-processing of many design optimization problems. Currently, we support the airfoil, wing, and aircraft agents. The AI agent can be installed locally or on an HPC.

## Installation (local computers)

The local installation works for Linux, Windows, and MacOS, and it is the easist way to run the agents with small cases. If you plan to run larger cases, e.g., wing aero-structural optimizatin, you need to install the agents on an HPC.

### Step 1. Install a LLM client

We need to first install an LLM client's command line interface (CLI). The MDO Agent Deck supports three LLM clients: Codex, Claude Code, and Gemini, but here you need to install **ONLY ONE** CLI client, and the Codex CLI is recommended.

**MacOS/Linux:**

Codex CLI:

`npm install -g @openai/codex`

Claude code CLI:

`curl -fsSL https://claude.ai/install.sh | bash`

Gemini CLI:

`npm install -g @google/gemini-cli`

**Windows CMD (Command Prompt):**

Codex CLI:

`npm install -g @openai/codex`

Claude code CLI:

`curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`

Gemini CLI:

`npm install -g @google/gemini-cli`


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

Unzip it and you will see a folder called `mdo_agent_results-main`. This will be the main working directory for your agents. 

**IMPORTANT**: you can not manually create a folder and use it as LLM's working directory! You must use `mdo_agent_results-main`. This is because `mdo_agent_results-main` has some pre-defined LLM configuraiton files (hidden by default). You DO NOT need to change these configuration files, though.

The local installation is finished!

## Installation (HPC)

TBD

## Test the agent

**IMPORTANT**: The MCP server setup is local and works only in the `mdo_agent_results-main` folder.

First, open VSCode and click the "Explorer" icon from the left bar. From there, you can select "Open Folder" and open the `mdo_agent_results-main` folder as your working directory.

Next, click the "Toggle Panel" button in the top right corner to open a terminal.

In the terminal, cd into the `mdo_agent_results-main` folder and open your LLM client in full-permission mode to avoid interruptions. Again, you need to choose **ONLY ONE** of the following, depending which LLM client you are using.

**Claude Code:**

`claude --dangerously-skip-permissions`

**Codex:**

`codex --yolo`

**Gemini:**

`gemini --yolo`

If this is the first time you add a new MCP server, your client may show a "New MCP server found" prompt. Choose "Use this MCP server".

Some LLM clients may also warn you about the skipped-permissions setup. You can allow it if needed. If you prefer, you can omit the `--dangerously-skip-permissions` or `--yolo` arguments.

Then, run `/mcp` and verify if the `mdo_agent_deck` is `connected`. If yes, you can start asking questions.

You can ask something like:

"Generate a CFD mesh for the NACA0012 airfoil with 20K cells with yPlus 5."

The agent will parse your promopt into solver input argements and run predefined commands to generate the mesh and then return clickable paths for the mesh figures along with a summary of the mesh. You can hold the Command key (MacOS) or Control key (Windows and Linux) and click these paths to view the figures directly in VSCode.

The agent will also return a clickable link for a Trame server to view the mesh interactively. You can open this server from your default browser by clicking the link.

For the best visual experience, we recommend using the "Light Modern" color theme in VSCode. To change the theme, open the Command Palette in VSCode, search for "Preferences: Color Theme", and select "Light Modern".

{% include links.html %}

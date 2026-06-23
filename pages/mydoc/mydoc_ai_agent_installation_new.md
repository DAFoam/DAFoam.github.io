---
title: Installation
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-installation-new.html
folder: mydoc
---

## Overall

There are four options to install and run the MDO Agent Deck framework: (A) Local Computers with LLM Apps, (B) Local Computers with VSCode, (C) HPC Clusters with LLM Apps, and (D) HPC Clusters with VSCode. Options A and B run on your local computer using pre-compiled Docker images, while Options C and D run on a high-performance computing (HPC) cluster with self-compiled codes. You need to choose **ONLY ONE** option to follow. If you are new to the MDO Agent Deck, we recommend you choose Option A, which is the easiest to set up and run.


## Option A: Local Comupters with LLM Apps

This option works for both Windows, and MacOS, and it is the easiest way to run the agents with small cases. If you plan to run larger cases, e.g., wing aero-structural optimization, you need to install the agents on an HPC (see Options C and D).

### Step 1. Install an LLM Desktop App

First, install an LLM Desktop App. The MDO Agent Deck supports multiple LLMs, but for this setup, you only need to install **ONLY ONE** LLLM app.

**NOTE**: You must sign up for an account for the selected LLM and log in using your subscription. Do **NOT** use API keys. If you already have a paid subscription for one of the following LLM providers, install its app. Otherwise, choose a LLM that offers a free but limited usage quota (we recommend Codex). If the quota for one free-tier LLM runs out, you may need to switch to another free-tier LLM. Note that most free-tier LLMs limit you to roughly 10 prompts per cycle and are suitable for evaluation only. For production use, a paid plan is required.

- Claude (Anthropic; paid plan only): [Download](https://claude.com/download)
- Codex (OpenAI; limited free quota): [Download](https://chatgpt.com/codex/)

### Step 2. Install Docker Desktop

Download and install the Docker Desktop app for [MacOS](https://docs.docker.com/desktop/setup/install/mac-install), [Windows](https://docs.docker.com/desktop/setup/install/windows-install), or [Linux](https://docs.docker.com/desktop/setup/install/linux).

After the Docker Desktop is installed, open it and keep it open.

Then, open a terminal and run the following command to download the pre-compiled MDO Agent Deck image:

`docker pull dafoam/agent:latest`

If a newer version of the agent image is available, simply run the command above again to download the latest image.

### Step 3. Download the working directory

Download `mdo_agent_work` repo from [here](https://github.com/DAFoam/mdo_agent_work/archive/refs/heads/docker.zip). 

Unzip it and you will see a folder called `mdo_agent_work-docker`. Rename it to `mdo_agent_work`. This will be the main working directory for your agents. 

**IMPORTANT**: Do not manually create a folder and use it as the LLM's working directory. You must use `mdo_agent_work`. This is because `mdo_agent_work/results` contains pre-defined LLM configuration files (hidden by default). You do not need to modify these configuration files.

The local installation is finished!

### Step 4. Test the agents

Follow the instructions below for your selected LLM to test the installation by running a small case.

<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Claude</button>
<button class="tab-button">Codex</button>
</div>
<div class="tab-content">

Open the Claude Desktop App and sign in. In the top left, click the sidebar icon to expand it, then change the mode from "Chat" to "Code". Next, click the "Local" icon right above the chat box and select "Add another folder". In the pop-up, select the `mdo_agent_work/results` folder. You can now ask questions such as `Generate a CFD mesh for the NACA2412 airfoil with 20K cells and yPlus 3`. During agent execution, you may be asked for permission multiple times. To skip this, change the "Mode" below the chat box to "Bypass permissions". **IMPORTANT: The Bypass permissions mode may modify or damage system files. Use with caution!** Once the task is finished, you can click the names of the generated mesh pictures to view them in the app, or the links from the Trame or HTML servers to visualize the results.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-installation-claude-app.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-installation-claude-result.png" style="width:400px !important;" />

Fig. An example of the Claude Code interface


</div>
<div class="tab-content">

Open the Codex Desktop App and sign in. Click the "folder" icon right below the chat box and select "Add new project"->"Use existing folder". In the pop-up, select the `mdo_agent_work/results` folder. You can now ask questions such as `Generate a CFD mesh for the NACA2412 airfoil with 20K cells and yPlus 3`. During agent execution, you may be asked for permission multiple times. To skip this, change the "Mode" below the chat box to "Approve for me". **IMPORTANT: The Approve for me mode may modify or damage system files. Use with caution!**. Once the task is finished, you can click the links from the Trame or HTML servers to visualize the mesh results.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-installation-codex-app.png" style="width:700px !important;" />

Fig. An example of the Codex interface

</div>
</div>


## Option B: Local Comupters with VSCode

Option B also supports both Windows and MacOS, and it relies on VSCode and LLM command-line interface (CLI) instead of LLM Desktop Apps. Compared with Option A, Option B has a built-in interface for case file management, which allows you to quick visualize case log files, figures, etc, and it also has a unified interface across different LLM models; however, it requires a few additonal steps for installation.

### Step 1. Install an LLM client CLI

First, install a command-line interface (CLI) for an LLM client. The MDO Agent Deck supports multiple LLM clients, but for this setup, you only need to install **ONE** CLI client.

**NOTE**: You must sign up for an account for the selected LLM and log in using your subscription. Do **NOT** use API keys. If you already have a paid subscription for one of the following LLM providers, install its app. Otherwise, choose a LLM that offers a free but limited usage quota (we recommend Codex). If the quota for one free-tier LLM runs out, you may need to switch to another free-tier LLM.

Please follow the official installation instructions for your selected client. The installation steps may differ by operating system and may require additional dependencies such as Node.js.

- Claude (Anthropic; paid plan only): [Download](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- Codex (OpenAI; limited free quota): [Download](https://help.openai.com/en/articles/11096431)
- Antigravity (Google; limited free quota): [Download](https://antigravity.google/download#antigravity-cli)
- Cursor (Anysphere; limited free quota): [Download](https://cursor.com/cli)

After the installation is finished, verify that your CLI is available in the terminal:

<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Codex</button>
<button class="tab-button">Claude Code</button>
<button class="tab-button">Antigravity</button>
<button class="tab-button">Cursor</button>
</div>
<div class="tab-content">
codex -V
</div>
<div class="tab-content">
claude -V
</div>
<div class="tab-content">
agy --version
</div>
<div class="tab-content">
agent -v
</div>
</div>

You should see the version of your LLM client in the terminal.


### Step 2. Install Docker Desktop

Same as the Step 2 in Opion A.

### Step 3. Download the working directory

Same as the Step 3 in Opion A.

### Step 2. Install VS Code

Download VS Code from [here](https://code.visualstudio.com/download) and install it.

Optional: For VS Code on Windows, you can configure your terminal to use a desired bash interface by opening the Command Palette from the top panel, searching for "Terminal: Select Default Profile", and then selecting CMD, PowerShell, or bash.

The local installation is finished!

## Option C: HPC Clusters with LLM Apps







## Option D: HPC clusters with VSCode 

This section is for running large-scale cases on an HPC. If you are using the local installation and running the agents on your local computer, you do not need to follow these steps.

### Step 1. Install VS Code and Remote SSH

Download VS Code from [here](https://code.visualstudio.com/download) and install it.

Optional: Some newer versions of VS Code may experience issues when connecting to HPC systems. If you run into this issue, try an older version of VS Code: [1.100.3](https://code.visualstudio.com/updates/v1_100). 

Open VS Code. From the left panel, click `Extensions` (see Fig. 1 below), then search for `Remote SSH` by Microsoft and click `Install`.

After installing Remote SSH, set up the SSH connection: 

- Click the `Open a Remote Window` button in the lower-left corner of VS Code (see Fig. 1 below).

- In the pop-up window on the top, select `Connect to Host`, then choose `+ Add New SSH Host`. 

- In the pop-up window, enter your SSH command, for example: `ssh my_user_name@nova.its.iastate.edu`.

- When prompted, select the SSH configuration file to update (choose `~/.ssh/config` or similar).

- Once the SSH configuration is complete, click `Connect to Host` again and select your newly added host (e.g., `nova.its.iastate.edu`). You will be prompted to enter your password and, if applicable, a verification code to log in to the HPC.

- If the terminal is not visible after opening the folder, click `Toggle Panel` in the top-right corner of VS Code (see Fig. 1 below).

DO NOT close VS Code or the open terminal on the HPC. We will use them to install other packages in the following steps.

### Step 2. Install a LLM client on the HPC

Using the terminal in VS Code via Remote SSH, we need to install an LLM client's command line interface (CLI) **on the HPC**. Please follow the same instrucitons from  **Installation (local computers) -> Step 1. Install an LLM client**, shown above.

### Step 3. Install the agents and DAFoam on the HPC

Using the terminal in VS Code via Remote SSH, we need to compile the DAFoam package from scratch. Follow the instructions from [here](https://dafoam.github.io/installation-source.html). In this example, we assume DAFoam is installed in `/home/your_user_name/dafoam`.

After DAFoam is compiled, load its environment, e.g., `. /home/your_user_name/dafoam/loadDAFoam.sh`, and then run the following command to install the MDO Agent Deck:

`pip install mdo_agent_deck`

The `mdo_agent_deck` package is hosted on PyPI.

### Step 4. Create the working directory

Using the terminal in VS Code via Remote SSH, we will need to first download `mdo_agent_work` repo from [here](https://github.com/DAFoam/mdo_agent_work/archive/refs/heads/hpc.zip). Note: this link is DIFFERENT from the one from local installation above.

Unzip it and you will see a folder called `mdo_agent_work-hpc`. Rename it to `mdo_agent_work`. This will be the main working directory for your agents. You can put `mdo_agent_work` any where on the HPC, e.g., `/home/your_user_name/mdo_agent_work`.

**IMPORTANT**: Do not manually create a folder and use it as the LLM's working directory. You must use `mdo_agent_work`. This is because `mdo_agent_work/results` contains pre-defined LLM configuration files (hidden by default). You do not need to modify these configuration files.

The agents are ready to use on the HPC.

## Test the agent

The following steps work for both local and HPC installations.

First, open VS Code. For HPC installation, you need to use Remote SSH to connect to the HPC. You do not need to do this for local installation.

Then, in VS Code, click the "Explorer" icon in the left sidebar (see Fig. below). From there, select "Open Folder" and open the `mdo_agent_work` folder as your working directory.

Next, click the "Toggle Panel" button in the top-right corner to open a terminal (see Fig. 1 below).

In the terminal, navigate to the `mdo_agent_work/results` folder. If you use HPC or Native mode, you **MUST load the DAFoam environment**. You do not need to do this for Docker mode.

**IMPORTANT**: Open the `mdo_agent_work` folder in Explorer, then use the terminal to navigate to `mdo_agent_work/results` before starting the LLM CLI. This is intentional and helps avoid conflicts with VS Code LLM extensions. You must start the LLM in the `mdo_agent_work/results` folder. The name of the `results` folder can be arbitrary. If you need to run multiple cases, you can make copies of the `results` folder inside `mdo_agent_work`, e.g., `mdo_agent_work/results1` and `mdo_agent_work/results2`.

Then, launch your LLM client in full-permission mode to avoid interruptions. Choose **ONLY ONE** of the following, depending on which LLM client you are using.

<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Codex</button>
<button class="tab-button">Claude Code</button>
<button class="tab-button">Antigravity</button>
<button class="tab-button">Cursor</button>
</div>
<div class="tab-content">
codex --yolo
</div>
<div class="tab-content">
claude --dangerously-skip-permissions
</div>
<div class="tab-content">
agy --dangerously-skip-permissions
</div>
<div class="tab-content">
agent --yolo
</div>
</div>

You need to sign up for an account and log in to the LLM CLI. DO NOT use API keys; use subscription login instead.

If this is the first time you add a new MCP server, your client may show a "New MCP server found" prompt. Choose "Use this MCP server".

Some LLM clients may also warn you about the skipped-permissions setup. You can allow it if needed. If you prefer, you can omit the `--dangerously-skip-permissions` or `--yolo` arguments.

Then, run `/mcp` and verify if the `mdo_agent_deck` is `connected`. If yes, you can start asking questions.

You can ask something like:

"Generate a CFD mesh for the NACA0012 airfoil with 20K cells with yPlus 5."

The agent will parse your prompt into solver input arguments and run predefined commands to generate the mesh, then return clickable paths to the mesh figures along with a summary of the mesh. You can hold the Command key (MacOS) or Control key (Windows and Linux) and click these paths to view the figures directly in VS Code (see Fig. 1 below).

The agent will also return a clickable link for a Trame server to view the mesh interactively. You can open this server from your default browser by clicking the link.

For the best visual experience, we recommend using the "Light Modern" color theme in VS Code. To change the theme, open the Command Palette in VS Code, search for "Preferences: Color Theme", and select "Light Modern".

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-local-vscode.png" style="width:600px !important;" />

Fig. 1. An example of the VS Code interface on local computers


{% include links.html %}

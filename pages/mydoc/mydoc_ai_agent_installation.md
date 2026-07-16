---
title: Installation
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-installation.html
folder: mydoc
---

## Overview

There are four options to install and run the MDO Agent Deck framework: (A) Local Computers with LLM Apps, (B) Local Computers with VSCode, (C) HPC Clusters with LLM Apps, and (D) HPC Clusters with VSCode. Options A and B run on your local computer using pre-compiled Docker images, while Options C and D run on a high-performance computing (HPC) cluster with self-compiled codes. You need to choose **ONLY ONE** option to follow. If you are new to the MDO Agent Deck, we recommend you choose Option A, which is the easiest to set up and run.


## Option A: Local Computers with LLM Apps

This option works for both Windows and MacOS, and it is the easiest way to run the agents with small cases. If you plan to run larger cases, e.g., wing aero-structural optimization, you need to install the agents on an HPC (see Options C and D).

### Step 1. Install an LLM Desktop App

First, install an LLM Desktop App. The MDO Agent Deck supports multiple LLMs, but for this setup, you need to install **ONLY ONE** LLM app.

**NOTE**: You must sign up for an account for the selected LLM and log in using your subscription. Do **NOT** use API keys. If you already have a paid subscription for one of the following LLM providers, install its app. Otherwise, choose an LLM that offers a free but limited usage quota (we recommend Codex). Note that most free-tier LLMs limit you to roughly 10 prompts per cycle and are suitable for evaluation only. For production use, a paid plan is required.

- Claude (Anthropic; paid plan only): [Download](https://claude.com/download)
- Codex (OpenAI; limited free quota): [Download](https://chatgpt.com/codex/)

### Step 2. Install Docker Desktop

Download and install the Docker Desktop app for:

- [MacOS](https://docs.docker.com/desktop/setup/install/mac-install) 
- [Windows](https://docs.docker.com/desktop/setup/install/windows-install)

After the Docker Desktop is installed, open it and keep it open.

Then, open a terminal and run the following command to download the pre-compiled MDO Agent Deck image:

`docker pull dafoam/agent:latest`

If a newer version of the agent image is available, simply run the command above again to download the latest image.

### Step 3. Download the working directory

Download `mdo_agent_work` repo from [here](https://github.com/DAFoam/mdo_agent_work/archive/refs/heads/docker.zip). 

Unzip it and you will see a folder called `mdo_agent_work-docker`. Rename it to `mdo_agent_work`. This will be the main working directory for your agents. 

**IMPORTANT**: Do not manually create a folder and use it as the LLM's working directory. You must use `mdo_agent_work`. This is because `mdo_agent_work/results` contains pre-defined LLM configuration files (hidden by default). You do not need to modify these configuration files.

The installation is finished!

### Step 4. Test the agents

Follow the instructions below for your selected LLM to test the installation by running a small case.

<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Claude</button>
<button class="tab-button">Codex</button>
</div>
<div class="tab-content">

1. Close both Docker and Claude Desktop apps. Then, open the Docker app first, wait until it is ready, and then open the Claude Desktop App. 

2. In the top left, click the sidebar icon to expand it, then change the mode from "Chat" to "Code". 

3. Click the "Local" icon right above the chat box and select "Add another folder". In the pop-up, select the `mdo_agent_work/results` folder. 

4. Then, ask `Is mdo_agent_deck's must_call_first tool available?`. Once the agent confirms the MCP status (if not ask it to check again or close Claude and re-open), you can now ask questions such as `Generate a CFD mesh for the NACA2412 airfoil with 20K cells and yPlus 3`. The agent will run the case in the background.

5. Once the task is finished, you can click the names of the generated mesh pictures to view them in the app, or the links from the Trame or HTML servers to visualize the results.

During agent execution, you may be asked for permission multiple times. To skip this, change the "Mode" below the chat box to "Auto mode". **IMPORTANT: The auto mode may modify or damage system files. Use with caution!**

**NOTE**: If you need to start a new chat, close Claude and re-open. This ensures the mdo_agent_deck is reset to run the next case. Try not to run multiple cases in one chat window, as it will use a lot of tokens!

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-installation-claude-app.png" style="width:400px !important;" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-installation-claude-result.png" style="width:400px !important;" />

Fig. An example of the Claude Code interface


</div>
<div class="tab-content">

1. Close both Docker and Codex Desktop apps. Then, open the Docker app first, wait until it is ready, and then open the Codex Desktop App. 

2. Click "Choose project" and hover over "New project". Click "Use an existing folder". In the pop-up, select the `mdo_agent_work/results` folder. 

3.  Then, ask `Is mdo_agent_deck's must_call_first tool available?`. Once the agent confirms the MCP status (if not ask it to check again or close Codex and re-open), you can now ask questions such as `Generate a CFD mesh for the NACA2412 airfoil with 20K cells and yPlus 3`. The agent will run the case in the background.

4. Once the task is finished, you can click the links from the Trame or HTML servers to visualize the mesh results.

During agent execution, you may be asked for permission multiple times. To skip this, change the "Mode" below the chat box to "Approve for me". **IMPORTANT: The Approve for me mode may modify or damage system files. Use with caution!** 

**NOTE**: If you need to start a new chat, close Codex and re-open. This ensure the mdo_agent_deck is reset to run the next case. Try not to run multiple cases in one chat window, it will use a lot of token!

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-installation-codex-app.png" style="width:700px !important;" />

Fig. An example of the Codex interface

</div>
</div>


## Option B: Local Computers with VSCode

Option B also supports both Windows and MacOS, and it relies on VSCode and LLM command-line interface (CLI) instead of LLM Desktop Apps. Compared with Option A, Option B has a built-in interface for case file management, which allows you to quickly visualize case log files, figures, etc, and it also has a unified interface across different LLM models; however, it requires a few additional steps for installation.

### Step 1. Install an LLM client CLI

First, install a command-line interface (CLI) for an LLM client. The MDO Agent Deck supports multiple LLM clients, but for this setup, you only need to install **ONE** CLI client.

**NOTE**: You must sign up for an account for the selected LLM and log in using your subscription. Do **NOT** use API keys. If you already have a paid subscription for one of the following LLM providers, install its app. Otherwise, choose an LLM that offers a free but limited usage quota (we recommend Codex). Note that most free-tier LLMs limit you to roughly 10 prompts per cycle and are suitable for evaluation only. For production use, a paid plan is required.

Please follow the following installation instructions for your selected client. The installation steps may differ by operating system and may require additional dependencies such as Node.js.

- Claude (Anthropic; paid plan only): [Install](https://docs.anthropic.com/en/docs/claude-code/getting-started)
- Codex (OpenAI; limited free quota): [Install](https://help.openai.com/en/articles/11096431)
- Antigravity (Google; limited free quota): [Install](https://antigravity.google/download#antigravity-cli)
- Cursor (Anysphere; limited free quota): [Install](https://cursor.com/cli)


### Step 2. Install Docker Desktop

Same as the Step 2 in Option A.

### Step 3. Download the working directory

Same as the Step 3 in Option A.

The installation is finished!

### Step 4. Test the agents

- Open VS Code. Then, click the "Explorer" icon in the left sidebar (see the Fig. below). From there, select "Open Folder" and open the `mdo_agent_work` folder as your working directory.

- Click the "Toggle Panel" button in the top-right corner to open a terminal (see the Fig. below). Then, in the terminal, navigate to the `mdo_agent_work/results` folder. **IMPORTANT**: Open the `mdo_agent_work` folder in Explorer, then use the terminal to navigate to `mdo_agent_work/results` before starting the LLM CLI. This is intentional and helps avoid conflicts with VS Code LLM extensions. You must start the LLM in the `mdo_agent_work/results` folder. The name of the `results` folder can be arbitrary. If you need to run multiple cases, you can make copies of the `results` folder inside `mdo_agent_work`, e.g., `mdo_agent_work/results1` and `mdo_agent_work/results2`.

- Launch your LLM client in the VSCode terminal and sign in. Choose **ONLY ONE** of the following, depending on which LLM client you are using.

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

**IMPORTANT: All the above commands bypass the permission, so they may modify or damage system files. Use with caution! If you prefer manual permissions, run the LLM CLI without the --yolo or --dangerously-skip-permissions argument**

- In the LLM CLI chat box, run `/mcp` and verify if the `mdo_agent_deck` is `connected` or `running`. If yes, the agent is ready to run.

- You can ask something like: `Generate a CFD mesh for the NACA2412 airfoil with 20K cells with yPlus 5`. The agent will parse your prompt into solver input arguments and run predefined commands to generate the mesh, then return clickable paths to the mesh figures along with a summary of the mesh. You can hold the Command key (MacOS) or Control key (Windows) and click these paths to view the figures directly in VS Code (see the Fig. below). The agent will also return a clickable link for a Trame server to view the mesh interactively. You can open this server from your default browser by clicking the link.

**NOTE**: For the best visual experience, we recommend using the "Light Modern" color theme in VS Code. To change the theme, open the Command Palette in VS Code, search for "Preferences: Color Theme", and select "Light Modern".

<div style="text-align: center;">
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-local-vscode.png" style="width:500px !important;" />

Fig. An example of the VS Code interface for Codex. Other LLMs have similar interfaces 
</div>

## Option C: HPC Clusters with LLM Apps

This Option is for running large-scale cases on an HPC cluster. Currently only Claude Desktop App supports remote HPC connection.

### Step 1. Install an LLM Desktop App on your computer

Same as Step 1 in Option A. **NOTE:** you need to install the LLM desktop app on your computer, instead of the HPC.

### Step 2. Compile the agents and DAFoam on the HPC

Use SSH to login to the HPC. Then, compile the DAFoam package from scratch there. Follow the instructions from [here](https://dafoam.github.io/installation-source.html). In this example, we assume DAFoam is installed in `/home/your_user_name/dafoam` and will use this path for the instructions below.

After DAFoam is compiled, load its environment, e.g., `. /home/your_user_name/dafoam/loadDAFoam.sh`, and then run the following command to install the MDO Agent Deck:

`pip install mdo_agent_deck`

**NOTE** The `mdo_agent_deck` package is hosted on PyPI.

Then, add the following line to your `~/.bashrc` on the HPC to automatically load DAFoam when logging in.

`. /home/your_user_name/dafoam/loadDAFoam.sh`

### Step 3. Create the working directory on the HPC

Use SSH to login to the HPC, then, download `mdo_agent_work` repo from [here](https://github.com/DAFoam/mdo_agent_work/archive/refs/heads/hpc.zip). Note: this link is DIFFERENT from the one from Options A and B above.

Unzip it and you will see a folder called `mdo_agent_work-hpc`. Rename it to `mdo_agent_work`. This will be the main working directory for your agents. You can put `mdo_agent_work` anywhere on the HPC, e.g., `/home/your_user_name/mdo_agent_work`.

**IMPORTANT**: Do not manually create a folder and use it as the LLM's working directory. You must use `mdo_agent_work`. This is because `mdo_agent_work/results` contains pre-defined LLM configuration files (hidden by default). You do not need to modify these configuration files.

### Step 4. Customize the HPC job submission script

Open `mdo_agent_work/results/myHPCJob.sh` and adjust the `#SBATCH` directives (walltime, nodes, cores, job name) to match your HPC cluster. Keep the filename as `myHPCJob.sh`, keep it in the `mdo_agent_work/results/` folder, and always keep `./Allrun.sh` as the last line of the script. This script will be used by the agent to submit jobs on your HPC.

### Step 5. Test the agents


<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Claude</button>
</div>
<div class="tab-content">

1. Open the Claude Desktop App and sign in. 

2. In the top left, click the sidebar icon to expand it, then change the mode from "Chat" to "Code". 

3. Click the "Local" icon right above the chat box and select "Add SSH Host". In the pop-up, fill out the "Name" (e.g., `my_hpc`) and "SSH Host" (e.g., `my_user_name@myhpc.com`). Leave the "SSH Port" and "Identity File" as is.  Once done, click "Add SSH Connection".

4. Click the "Local" icon again and select the newly added SSH server, e.g., `my_hpc`. You will be prompted to enter your HPC account password and the verification code (if applicable). **NOTE:** The Claude app does not distinguish between the password and verification code prompts from your HPC, so the pop-up window will always say it needs a password. If it asks for the password twice, the second prompt is likely requesting your verification code.

5. Once connected, you can click the button right next to "Local" to "Browse Remote Folder". Navigate to the `mdo_agent_work/results` folder.

6. The agent is ready to use. You can ask something like: `Generate a CFD mesh for the NACA2412 airfoil with 20K cells with yPlus 5`. **NOTE**: On the HPC, the agent will submit jobs to run cases on compute nodes, instead of head nodes.

7. Once the task is finished, you can click the names of the generated mesh pictures to view them in the app, or the links from the Trame or HTML servers to visualize the results. You cannot directly access the case folder on the Claude Desktop App. To view the files in the case folder, you need to use a separate SSH to connect to the HPC and navigate to `mdo_agent_work/results`.

During agent execution, you may be asked for permission multiple times. To skip this, change the "Mode" below the chat box to "Bypass permissions". **IMPORTANT: The Bypass permissions mode may modify or damage HPC system files. Use with caution!**

</div>
</div>

## Option D: HPC clusters with VSCode 

This option is for running large-scale cases on an HPC cluster. Option D is similar to Option C, except that it uses VSCode as the interface to the HPC. Compared with the Claude Desktop App, VSCode allows you to run agents and view files in the case folder simultaneously.

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

### Step 2. Install an LLM client on the HPC

Using the terminal in VS Code via Remote SSH, install an LLM client's command-line interface (CLI) **on the HPC**. The installation commands are the same as those for local computers; refer to **Option B -> Step 1. Install an LLM client CLI** above.

### Step 3. Install the agents and DAFoam on the HPC

Same as the Step 2 in Option C. Except that you can use the terminal from VSCode to compile DAFoam and the agent.

### Step 4. Create the working directory

Same as the Step 3 in Option C. Except that you can use the terminal from VSCode to download the working directory repo.

### Step 5. Customize the HPC job submission script

Same as the Step 4 in Option C.

### Step 6. Test the agents

- Open VS Code and use Remote SSH to connect to the HPC.

- In VS Code, click the "Explorer" icon in the left sidebar (see the Fig. in Option B above). From there, select "Open Folder" and open the `mdo_agent_work` folder on the HPC as your working directory.

- Click the "Toggle Panel" button in the top-right corner to open a terminal (see the Fig. in Option B above).

- In the terminal, navigate to the `mdo_agent_work/results` folder on the HPC. **IMPORTANT**: Open the `mdo_agent_work` folder in Explorer, then use the terminal to navigate to `mdo_agent_work/results` before starting the LLM CLI. This is intentional and helps avoid conflicts with VS Code LLM extensions. You must start the LLM in the `mdo_agent_work/results` folder. The name of the `results` folder can be arbitrary. If you need to run multiple cases, you can make copies of the `results` folder inside `mdo_agent_work`, e.g., `mdo_agent_work/results1` and `mdo_agent_work/results2`.

- Launch your LLM client in the VSCode terminal on the HPC and sign in. Choose **ONLY ONE** of the following, depending on which LLM client you are using.

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

**IMPORTANT: All the above commands bypass the permission, so they may modify or damage system files. Use with caution! If you prefer manual permissions, run the LLM CLI without the --yolo or --dangerously-skip-permissions argument**

- In the LLM CLI chat box, run `/mcp` and verify if the `mdo_agent_deck` is `connected` or `running`. If yes, the agent is ready to run.

- You can ask something like: `Generate a CFD mesh for the NACA2412 airfoil with 20K cells with yPlus 5`. The agent will parse your prompt into solver input arguments and run predefined commands to generate the mesh, then return clickable paths to the mesh figures along with a summary of the mesh. You can hold the Command key (MacOS) or Control key (Windows) and click these paths to view the figures directly in VS Code (see the Fig. in Option B above). The agent will also return a clickable link for a Trame server to view the mesh interactively. You can open this server from your default browser by clicking the link.

**NOTE**: For the best visual experience, we recommend using the "Light Modern" color theme in VS Code. To change the theme, open the Command Palette in VS Code, search for "Preferences: Color Theme", and select "Light Modern".

## Option E: Local LLM

This option works for Linux, MacOS, and Windows. This option is for running the agents with a local LLM.

### Step 1. Download local LLM
First, download Ollama which will allow you to download LLMs and manage your various models.

- Ollama [download](https://ollama.com/download)

After the download is complete, start ollama by running `ollama serve` in the terminal. Then download an LLM via `ollama pull <model name>`. You can find a searchable list of models [here](https://ollama.com/search). The recommended model to run is `qwen3.5:9b`. To get the model name, select the model you want to download by clicking on it. Then copy and paste the name of the specific version of that model you wish to download.

Once the model is downloaded, you can run the model in your terminal using the following command: `ollama run <model name>`.

**IMPORTANT: After prompting the model, run `ollama ps` in another terminal window. You should see the GPU usage at 100%. If there is any CPU usage then the model you downloaded is too large for your hardware. Consider running a smaller model.**

### Step 2. Download the working directory

Download `mdo_agent_work` repo from [here](https://github.com/DAFoam/mdo_agent_work/archive/refs/heads/docker.zip). 

Unzip it and you will see a folder called `mdo_agent_work-docker`. Rename it to `mdo_agent_work`. This will be the main working directory for your agents.

### Step 3. Download OpenCode and configure MCP file
Once the local LLM is up and running, it must be connected to the MCP server. To do this, it is recommended to use OpenCode. Download OpenCode by running the following command: `curl -fsSL https://opencode.ai/install | bash`. There is also a desktop version available to [download](https://opencode.ai/download).

OpenCode requires the use of `opencode.json` in lieu of `mdo_agent_work/results/.mcp.json`, though the two files are very similar with `opencode.json` having an additional entry for the LLM you wish to run. In `opencode.json`, you will need to only adjust the entries under `models`. The example `opencode.json` file below shows a configuration for the `qwen3.5:9b` model. Ensure that this file is in the same `results/` directory as `.mcp.json`.  

```
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "qwen3.5:9b": {
          "name": "qwen"
        }
      }
    }
  },
  "mcp": {
    "mdo_agent_deck": {
      "type": "local",
      "command": [
        "docker",
        "run",
        "-i",
        "--rm",
        "--name",
        "mdo_agent_deck",
        "-p",
        "8001:8001",
        "-p",
        "8002:8002",
        "--mount",
        "type=bind,src=.,target=/home/dafoamuser/mount",
        "-w",
        "/home/dafoamuser/mount",
        "mdo_agent_deck:latest",
        "bash",
        "-lc",
        "source /home/dafoamuser/dafoam/loadDAFoam.sh && mdo-agent-deck-mcp"
      ]
    }
  }
}
```

Once this file is created, `cd` to `results/` and run `opencode` to launch the agent. You will see on the right hand side a verification that the LLM is connected to the MCP server. Additionally, you can run `/mcps` in OpenCode to view the available MCP servers. If you are connected, you should see `mdo_agent_deck connected` in the pop-up window. Hit `esc` to close this window.

**IMPORTANT: OpenCode has two modes: Build and Plan. Build mode allows OpenCode to modify files. Plan mode does not. In order to run the agents properly, ensure you are in Build mode. This can be toggled via the tab key.**

### Step 4. Test the agents
Follow the instructions below to test the agents.

- `cd` to the `results` directory and run `opencode`
- Run `/mcps` to verify that opencode is connected to the MCP server
- If connected, you can ask the agent to run a task such as: `Simulate the NACA0012 airfoil in a steady state simulation using 20k cells`. The agent will parse this input in order to generate the appropriate mesh and run the CFD simulation for you.

### Step 1. Install Ollama and prepare the model

For local agentic CFD workflows, we recommend Ollama to host an LLM locally. In this tutorial, we use qwen3.5:9b because it is both capable enough to handle such an agentic workflow, and small enough to function on mainstream hardware. First, follow the steps below:

- Download [Ollama](https://ollama.com/download) from here and install it.
- Open a terminal, and verify the installation by `ollama --version`.
- Pull the qwen3.5:9b base model by `ollama pull qwen3.5:9b`.
- Use `ollama ls` to list all local models, and verify that qwen3.5:9b is listed.

Next, we create a tuned variant from the qwen3.5:9b base model for the agentic tasks. In any directory, create a file named `Modelfile.qwen-agent` with the content below:

```
FROM qwen3.5:9b
PARAMETER num_ctx 65536
PARAMETER temperature 0.6
PARAMETER top_p 0.8
PARAMETER top_k 20
PARAMETER min_p 0
PARAMETER presence_penalty 0
PARAMETER repeat_penalty 1.0
```

Then, in the same directory, build the agentic variant by `ollama create qwen3.5-agent:9b -f Modelfile.qwen-agent`. Use `ollama ls` again, and verify that the new agentic variant called `qwen3.5-agent:9b` is listed.

Now, test the inference speed of the locally hosted LLM by `ollama run qwen3.5-agent:9b --verbose`. After the brief loading, you can start chatting and ask a question like "Can you give me an overview of your understanding of CFD?" After the LLM responds, take note of the `eval rate` in tokens/s at the end, and the performance is considered sufficient if the value is greater than 15. Once done with the performance evaluation, you may end the chat session by typing `/bye`. During or shortly after the test chat session, you can check the VRAM or RAM usage by `ollama ps`. Our agentic variant of qwen3.5:9b with a 64K context window should be less than 8 GB in size, and it should fit 100% inside a mainstream discrete GPU.

<!-- By default, Ollama only loads the LLM at the first user message, and automatically unloads after some idle time. To make the LLM persistent in RAM/VRAM... -->

### Step 2. Install and configure Cline

Cline is an open-source agentic harness built as an IDE extension. Make sure VSCode is installed first, and install Cline by `code --install-extension saoudrizwan.claude-dev` in the terminal. After the installation, the Cline icon should show up on the activity bar (left) of VSCode. Click the Cline icon, and at the top of the Cline panel, we can see "New Task", "MCP Servers", "History", "Account", and "Settings"

Next, we connect Cline to our locally hosted `qwen3.5-agent:9b`. Open "Settings" (gear icon) and set:

- API Provider: `Ollama`
- Base URL: leave default (`http://localhost:11434`)
- Model: `qwen3.5-agent:9b`
- Context window: `65536`

Then, we connect Cline to the `mdo_agent_deck` MCP server. Click "MCP Servers" (server stack icon), "Configure", and then "Configure MCP Servers", and then put the following content into cline_mcp_settings.json, and change the placeholder `ABSOLUTE_PATH_TO_mdo_agents_results` to your actual absolute path. For Windows users, make sure to use "\\\\" instead of "\\".  

```json
{
  "mcpServers": {
    "mdo_agent_deck": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-p", "8001:8001",
        "-p", "8002:8002",
        "--mount", "type=bind,src=ABSOLUTE_PATH_TO_mdo_agents_results,target=/home/dafoamuser/mount",
        "-w", "/home/dafoamuser/mount",
        "mdo_agent_deck:latest",
        "bash", "-lc",
        "source /home/dafoamuser/dafoam/loadDAFoam.sh && mdo-agent-deck-mcp"
      ],
      "disabled": false,
      "timeout": 600,
      "autoApprove": [
        "must_call_first", "get_skills", "get_pre_context",
        "get_skill_input_info", "get_skill_advanced_parameters",
        "set_skill_inputs", "set_skill_advanced_parameters",
        "generate_lhs_samples", "prepare", "run", "submit_run_batch",
        "review_run", "wait_for_run", "analyze", "review_analyze",
        "get_post_context"
      ]
    }
  }
}
```

The `mdo_agent_deck` MCP server should then show up with a green light on, and a corresponding Docker container should also spawn. You can click "Restart Server" if it is shown as a red light instead. 

Note that Cline has a known bug in which it may auto-append its own cline_mcp_settings.json with "}", hence corrupting it. If the MCP server randomly stopped working, this may likely be the case. You can solve this by checking cline_mcp_settings.json and removing those "}" manually, or locking cline_mcp_settings.json as read-only.

### Step 3. Test the agents

With both the LLM and the MCP server connected to Cline, we can now run some local agentic CFD workflows. Click "New Task", and you can start an agentic CFD run via a prompt. 

You can try something like `You have MCP tools from the mdo_agent_deck server. First call must_call_first, then follow the returned workflow steps exactly, in order. Task: run a DAFoam RANS CFD analysis of the NACA0012 airfoil at 5 degrees angle of attack, Reynolds number 1e6; use 20000 cells, 2 CPU cores, and default values for the rest.` The agent will then parse the user intent, perform meshing, CFD, and post-processing in sequential order, and then report the results back to the human user. 

Note that the hints about `mdo_agent_deck` and `must_call_first` are not strictly necessary, but they help enforce reliability for a small language model like qwen3.5:9b.


{% include links.html %}

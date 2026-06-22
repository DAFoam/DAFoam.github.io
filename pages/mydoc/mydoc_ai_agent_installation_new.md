---
title: Installation
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-installation-new.html
folder: mydoc
---

The AI agent can be installed locally or on an HPC. If you are new to the MDO Agent Deck, we recommend starting with the local installation.

## Installation (local computers)

The local installation works for Windows and and MacOS, and it is the easiest way to run the agents with small cases. If you plan to run larger cases, e.g., wing aero-structural optimization, you need to install the agents on an HPC.

<div class="tab-container" data-tab-group="platform">
<div class="tab-buttons">
<button class="tab-button">Claude Code</button>
<button class="tab-button">Codex</button>
<button class="tab-button">Antigravity</button>
<button class="tab-button">Cursor</button>
</div>
<div class="tab-content">

**Step 1. Install Claude Code Desktop App**

Download and install the Claude Desktop App, following the instructions from: https://code.claude.com/docs/en/desktop-quickstart.

Open the Claude Desktop App, then sign up for an account (do not use API keys), and then login. You need the Pro plan to enable the Claude Code feature. 

Expand the side bar and select "</> Code". Then, at the bottom, click the "Local" button and click "open a new folder". Select the "mdo_agent_work/results" folder. Click the permission mode option, and select "Bypass permissions". Click the LLM models and select "Sonnet 4.6" and right next to it, select "Effort->Medium".

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




{% include links.html %}

---
title: Overview of MDO Agent Deck
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-overview.html
folder: mydoc
---

## Latest Release: v0.1.3

The MDO Agent Deck is an agentic AI framework for multidisciplinary design optimization (MDO). It exposes engineering workflows through an MCP server and orchestrates domain agents such as `airfoil`, `wing`, and `aircraft`. The MDO Agent Deck framework is not open source. Instead, it is distributed on PyPI as compiled shared library package for evaluation purpose. Check [LICENSE](https://pypi.org/project/mdo-agent-deck/) for more details.

## Trustworthy Agentic AI Framework for MDO

The framework is designed to be trustworthy for engineering using the following guardrails:

- Narrowly scoped, domain-specific agents.
- Strictly constrained input parameters per skill.
- A robust review-and-correction loop at each phase.
- Fully transparent and auditable execution workflows.

## How the Framework Works

For each user request/prompt, the agent execution follows a strict sequence:

1. The MCP server identifies the best domain agent and skill for the request.
2. It semetically parse the input information from user-prompt to the skill's input values.
3. It creates a new isolated case folder for that run.
4. It runs the **prepare** phase and checks the review result.
5. It runs the **run** phase and checks the review result.
6. It runs an **analyze** phase and checks the final review result.

This review gate after every phase is a key guardrail. If a review fails, the workflow stops and requests correction before moving forward.

For example, if a user asks:

`Generate a CFD mesh for NACA0012 at Mach 0.05, Reynolds 20,000, y+ target 50.`

The execution will look like this:

1. The MCP server identifies the `airfoil` agent and the `generate-cfd-mesh` skill for this request.
2. It semantically parses the user prompt into skill inputs (`airfoil_profile=naca0012`, `mach_number=0.05`, `reynolds_number=20000`, `y_plus_target=50`).
3. It creates a new isolated case folder, e.g., `airfoil_mesh_naca0012_ma005_20k_y50_0000`
4. In **prepare**, it copies geometry and mesh configuration files into that folder, then checks the review result.
5. In **run**, it launches the predefined mesh generation commands/scripts for that case.
6. In **analyze**, it computes mesh quality metrics and generates deliverables, then checks the final review result.

The user then receives a clear status plus output paths, such as:
   - mesh files in the case folder
   - plots under `plots/`
   - quality metrics JSON (for example `mesh_analysis_metrics.json`)

If any review fails (for example invalid input ranges or mesh quality below threshold), the workflow stops at that phase and reports what must be fixed.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-overview-diagram.png" style="width:700px !important;" />

Fig. 1. Schematic of the agentic AI workflow


## Transparency and Auditability

The framework records workflow and runtime context in the working directory:

- `agent_workflow.json`: auditable case-by-case phase history (`set_skill_inputs`, `prepare`, `review_prepare`, `run`, `review_run`, `analyze`, `review_analyze`) with timestamps and status.
- `agent_state.json`: persisted bindings (inputs and case directories) so sessions can resume after MCP server restarts.

This design supports traceability, debugging, and reproducibility for engineering studies.

## Deployment Modes

The MCP server supports three run modes:

- `Docker`: default containerized workflow.
- `Native`: direct execution on local/HPC environment.
- `HPC`: submit jobs to the cluster queue and run them when compute resources are available.

{% include links.html %}

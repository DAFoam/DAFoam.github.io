---
title: Overview of MDO Agent Deck
keywords: ai assistant
summary: 
sidebar: mydoc_sidebar
permalink: ai-agent-overview.html
folder: mydoc
---

The MDO Agent Deck is an agentic AI framework for multidisciplinary design optimization (MDO). It exposes engineering workflows through an MCP server and orchestrates domain agents such as `airfoil`, `wing`, and `aircraft`.

## Trustworthy Agentic AI Framework for MDO

The framework is designed to be trustworthy for engineering using the following guardrails:

- Narrowly scoped, domain-specific agents.
- Strictly constrained input parameters per skill.
- A robust review-and-correction loop at each phase.
- Fully transparent and auditable execution workflows.

## Core Architecture

At a high level, `mdo_agent_deck` is the top-level orchestrator:

- `mcp_server.py` exposes MCP tools (`get_skills`, `get_skill_input_info`, `set_skill_inputs`, `prepare`, `run`, `review_run`, `analyze`).
- `AgentDeck` loads installed agent packages from a registry and coordinates case directories, state persistence, and workflow auditing.
- Each agent provides one or more skills that follow a common interface (`prepare`, `run`, `review_run`, `analyze`, `review_analyze`).

## How the Framework Works

For each user request, a skill execution follows a strict sequence:

1. The system identifies the best domain agent and workflow step for the request.
2. It validates and fills required inputs.
3. It creates a new isolated case folder for that run.
4. It runs a **prepare** phase and checks the review result.
5. It runs the main **run** phase and checks the review result.
6. If the run is still active, the system keeps checking status until completion.
7. It runs an **analyze** phase and checks the final review result.

This review gate after every phase is a key guardrail. If a review fails, the workflow stops and requests correction before moving forward.

For example, if a user asks:

`Generate a CFD mesh for NACA0012 at Mach 0.05, Reynolds 20,000, y+ target 50.`

A typical execution looks like this:

1. The LLM routes the request to the `airfoil` agent and selects the `generate-cfd-mesh` skill.
2. It validates inputs (airfoil profile, flow condition tags, mesh controls, and naming fields).
3. It creates a new case folder, for example:
   - `results/airfoil_mesh_naca0012_ma005_20k_y50_0000`
4. In **prepare**, it copy geometry and mesh configuration files into that folder.
5. In **run**, it launches the mesh generation commands/scripts for that case.
6. In **analyze**, it computes mesh quality metrics and generates deliverables (for example mesh snapshots and summary metrics).
7. The user receives a clear status plus output paths, such as:
   - mesh files in the case folder
   - plots under `plots/`
   - quality metrics JSON (for example `mesh_analysis_metrics.json`)

If any review fails (for example invalid input ranges or mesh quality below threshold), the workflow stops at that phase and reports what must be fixed.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/AI-overview-diagram.png" style="width:700px !important;" />

Fig. 1. Schematic of the agentic AI workflow


## Case Folder and Run Isolation

Each skill run is mapped to a unique case directory under the working directory:

- Users provide a concise `case_name` such as `mesh_naca0012_20k`.
- AgentDeck prefixes with agent name and appends a run-id suffix (for example `_0000`, `_0001`).
- This prevents stale files from older runs from contaminating new runs.

For multi-step workflows, downstream steps start from a clean copy of the previous step results, so each stage stays reproducible and isolated.

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

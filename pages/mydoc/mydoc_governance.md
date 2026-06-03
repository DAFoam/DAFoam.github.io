---
title: Governance
keywords: governance, community, contribution, leadership
summary: 
sidebar: mydoc_sidebar
permalink: governance.html
folder: mydoc
---

This document describes the governance structure of the DAFoam Open-Source Ecosystem (OSE). The structure is designed to ensure the long-term sustainability of the project by establishing a clear leadership committee, a standardized code contribution workflow, and rules to keep community contributions robust and secure.

## 1. OSE Leadership Committee

The DAFoam OSE is managed by a leadership committee consisting of one chair and two committee members.

- Chair: Leads the committee, executes the plans agreed upon during annual meetings, and oversees the day-to-day operations of the OSE.
- Committee members: Provide recommendations to improve the OSE and assist the chair in enforcing the rules in this governance document.
- Meetings: The committee holds an annual meeting to review the current status of the OSE and plan future activities, including conferences, workshops, documentation, courses, tutorials, and new optimization features.
- Rotation: The chair and committee members serve two-year terms, which can be renewed. At the end of each term, the committee reviews the current membership and may invite new contributors to join if needed to keep the leadership active and representative of the community.

## 2. Code Contribution Workflow

To ensure robust and consistent code development, all contributions to DAFoam follow the standardized workflow described below.

### 2.1 New Code Contribution

1. Fork the [DAFoam GitHub repository](https://github.com/mdolab/dafoam) and develop your feature on a separate branch.
2. Follow the DAFoam code style: use clang-format for the C++ layer and black for the Python layer. Contributions that do not pass the formatter checks will not be merged.
3. Add regression tests that cover the new code. All regression tests must pass before a pull request can be merged. In addition, all new contributions are checked with a code coverage tool (Codecov) to ensure thorough testing.
4. Once development is complete, open a pull request against the main repository. The pull request description must include a brief summary of the new feature and any backward incompatibilities introduced.
5. At least one reviewer approval is required before merging.

### 2.2 New Feature Request

Users who want a new optimization feature added to DAFoam should:

1. Open an Issue in the [DAFoam GitHub repository](https://github.com/mdolab/dafoam) using the feature-request template.
2. Describe the desired feature (e.g., support for time-dependent problems) with relevant background information or references.
3. The DAFoam developer team will reach out to discuss the feature request in more detail.

### 2.3 Bug Reporting

Users who encounter a bug should:

1. Open an Issue in the [DAFoam GitHub repository](https://github.com/mdolab/dafoam) using the bug-report template.
2. Upload a minimal test case that reproduces the issue.
3. The DAFoam developer team will follow up, assign the issue to the responsible developer, and provide an estimated timeline for the fix.

## 3. Code Robustness and Security

All pull requests go through the following checks before they can be merged.

### 3.1 Contributor Identity

Contributors must use GitHub's Verified Commit feature to authenticate their identity. All commits in a pull request must be verified before the pull request is considered for merging, ensuring that changes come from authenticated accounts.

### 3.2 Code Scanning

Every pull request is automatically scanned using GitHub's code-scanning feature to identify potential security issues, such as injection of malicious or vulnerable code into DAFoam's source code, tests, build scripts, or run processes.

### 3.3 Third-Party Library Check

DAFoam relies on well-established open-source libraries (PETSc, SciPy, NumPy, CGNS, TensorFlow, OpenMPI) that have been rigorously tested. Any new third-party library proposed by external contributors will be reviewed by the committee to minimize security vulnerabilities before it is integrated.

{% include links.html %}

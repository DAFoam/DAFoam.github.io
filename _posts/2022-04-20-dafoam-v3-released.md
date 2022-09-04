---
title:  "DAFoam v3 released for MDO"
categories: jekyll update
permalink: dafoam_v3_released.html
---

We just released a major DAFoam upgrade to version 3. In version 3, we have developed an efficient interface to integrate DAFoam with [OpenMDAO](https://github.com/OpenMDAO/OpenMDAO) for multidisciplinary design optimization through the [Mphys](https://github.com/OpenMDAO/Mphys) interface. Refer to the [v3.0.0](https://github.com/mdolab/dafoam/releases/tag/v3.0.0) release note for more details.

While most of the settings are exact same as before, version 3 uses very different runScript.py because it is coupled with OpenMDAO. We suggest users get familiar with OpenMDAO before using DAFoam v3 run scripts. Check the Getting Started section from the [OpenMDAO documentation](https://openmdao.org/newdocs/versions/latest/getting_started/getting_started.html).

We have also updated some of the [tutorials](https://github.com/dafoam/tutorials) for v3. The version 2 run scripts are now called _v2.py. **NOTE: All the version 2 run scripts are currently compatible with DAFoam v3**. In other words, you can use DAFoam v3.0.0 to run any v2 scripts. However, we may drop the support for v2 in the future. 

**The v2 website has been moved to https://dafoamv2.github.io** and will no longer be maintained.

{% include links.html %}

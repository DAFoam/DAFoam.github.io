---
title: NACA0012 variations - compressibility, multi-point, multi-cases
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_naca0012_variations.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

## Subsonic and transonic optimization

Place holder text, don't change!

## Multi-point optimization

Place holder text, don't change!

## Multi-case optimization

The following is a multi-case aerodynamic shape optimization problem for the NACA0012 airfoil. This tutorial will show you how to use one runScript.py to run multiple cases within one folder. Go to the directory: /tutorials-master/NACA0012_Airfoil/multicase, we will see two subdirectories, SA and SST, which are the two cases we are going to run. To do that, we need create the builder to initialize the DASolvers for both cases In the `setup(self)` function.

'''python
    def setup(self):

        # create the builder to initialize the DASolvers for both cases (they share the same mesh option)
        dafoam_builder_sa = DAFoamBuilder(daOptionsSA, meshOptions, scenario="aerodynamic", run_directory="SA")
        dafoam_builder_sa.initialize(self.comm)

        dafoam_builder_sst = DAFoamBuilder(daOptionsSST, meshOptions, scenario="aerodynamic", run_directory="SST")
        dafoam_builder_sst.initialize(self.comm)
'''

{% include links.html %}

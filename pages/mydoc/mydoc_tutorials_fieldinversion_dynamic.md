---
title: Field inversion machine learning for an airfoil in dynamic stall
keywords: field inversion, run script, optimization
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_field_inversion_dynamic.html
folder: mydoc
---

## Overview
This tutorial showcases DAFoam's FIML capability in augmenting RANS turbulence models in predicting time-resolved unsteady flow with a moving boundary. Here we use the unsteady flow in the NACA0012 airfoil dynamic stall as an example. The airfoil is pitching up with 0.5 rad/s. We use only the Cd time-series from the k-omega SST as the training data. We then augment the SA model to match the spatial-temporal distribution of the flow fields from the SST model.

This work is currently under review in the AIAA Journal. "Zilong Li, Lean Fang, Anupam Sharma, Ping He. Field Inversion Machine Learning for Time-Resolved Unsteady Flows in Airfoil Dynamic Stall". A preview is available from arxiv.org.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil_Dynamic_Stall_U.gif" style="width:700px !important;" />

Fig. 1. Velocity contour of the airfoil dynamic stall

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/Airfoil_DynamicStall/unsteady/train and run the "preProcessing.sh" script. 

<pre>
./preProcessing.sh
</pre>

Then, go to the train/field-inversion directory and use the following command to run the field inversion:

<pre>
./Allrun.sh
</pre>

After the field inversion process is done, go to the train/machine-learning directory and use the following command to run the machine learning:

<pre>
./Allrun.sh
</pre>

After the machine learning procedure is done, we are ready to run the prediction simulations. Go to the predict/predict-pitch-rate-0.35 or predict/predict-pitch-rate-0.5 directory and use the following command to run FIML for the prediction cases:

<pre>
./Allrun.sh
</pre>

The FIML prediction results are as follows. As we can see that, the trained SA model matches the reference SST model very well.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil_Dynamic_Stall_CL.gif" style="width:500px !important;" />

Fig. 2. Time series of CL

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil_Dynamic_Stall_P.gif" style="width:500px !important;" />


Fig. 4. Temporal evolution of the velocity profile in the downstream

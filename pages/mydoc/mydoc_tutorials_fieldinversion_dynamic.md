---
title: Field inversion machine learning for an airfoil in dynamic stall
keywords: field inversion, run script, optimization
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_field_inversion_dynamic.html
folder: mydoc
---

## FIML for time-accurate unsteady flow around an airfoil in dynamic stall

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

The FIML prediction results for the pitch rate = 0.35 rad/s case are as follows:

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cd.png" width="500" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cl.png" width="500" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cm.png" width="500" />

Fig. 1. Temporal evolution of airfoil drag, lift, and pitching moment among baseline, reference, steady- and unsteady-FIML (pitch rate 0.35 rad/s).

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cp-1.png" width="500" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cp-2.png" width="500" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cp-3.png" width="500" />
<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Airfoil-DynamicStall-cp-4.png" width="500" />

Fig. 2. Surface pressure profiles at various time instances among baseline, reference, steady- and unsteady-FIML (pitch rate 0.35 rad/s).

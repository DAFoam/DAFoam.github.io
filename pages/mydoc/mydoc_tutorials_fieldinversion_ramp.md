---
title: Field inversion machine learning for a ramp
keywords: field inversion, run script, optimization
sidebar: mydoc_sidebar
permalink: mydoc_tutorials_field_inversion_ramp.html
folder: mydoc
---

## Overview
This is a new tutorial for steady and unsteady field inversion machine learning (FIML) using the latest DAFoam version. Please check the tutorial from [here](https://github.com/DAFoam/tutorials/tree/main/Ramp). 

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Ramp_mesh.png" width="400" />

Fig. 1 Mesh and the vertical probe profile for a 45-degree ramp.

## Field inversion machine learning for steady-state flow over the ramp

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/Ramp/steady/train and run the "preProcessing.sh" script. 

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the case:

<pre>
mpirun -np 4 python runScript_FIML.py 2>&1 | tee logOpt.txt
</pre>

This case uses our latest FIML interface, which incorporates a neural network model into the CFD solver to compute the augmented field variables. We augment the k-omega model and make it match the k-omega SST model. The FIML optimization is formulated as:

<pre>
Objective function: Regulated prediction error for the bottom wall pressure and the CD values
Design variables: Weights and biases for the built-in neural network
Augmented variables: betaFIK and betaFIOmega for the k and omega equations, respectively
Training configurations: c1: U0 = 10 m/s. c2: U0 = 20 m/s
Prediction configuration: U0 = 15 m/s
</pre>

The optimization converged in 14 iterations, and the objective function reduced from 3.9575071E+01 to 3.5429828E+00.

To test the trained model's accuracy for an unseen flow condition (i.e., U0 = 15 m/s), we can copy the designVariable.json (this file will be generated after the FIML optimization is done.) to tutorials-master/Ramp/steady/predict/trained. Then, go to tutorials-master/Ramp/steady/predict and run `Allrun.sh`. This command will run the primal for the baseline (k-omega), reference (k-omega SST), and the trained (FIML k-omega) models. The trained will read the optimized neural network weights and biases from designVariable.json, assign them to the built-in neural network model (defined in the `regressionModel` key in daOption) and run the primal solver.

For the U0 = 15 m/s case, the drag from the reference, baseline, and trained models are: 0.3881, 0.4458, 0.3829, respectively. The trained model significantly improve the drag prediction accuracy for this case.

## Field inversion machine learning for time-accurate unsteady flow over the ramp

To run this case, first download [tutorials](https://github.com/DAFoam/tutorials/archive/master.tar.gz) and untar it. Then go to tutorials-master/Ramp/unsteady/train and run the "preProcessing.sh" script. 

<pre>
./preProcessing.sh
</pre>

Then, use the following command to run the case:

<pre>
mpirun -np 4 python runScript.py 2>&1 | tee logOpt.txt
</pre>

The setup is similar to the steady state FIML except that we consider both spatial and temporal evolutions of the flow. In other words, the trained model will improve both spatial and temporal predictions of the flow. We augment the SA model and make it match the k-omega SST model. 

<pre>
Objective function: Regulated prediction error for the bottom wall pressure at all time steps
Design variables: Weights and biases for the built-in neural network
Augmented variables: betaFINuTilda for the nuTilda equations
Training configuration: U0 = 10 m/s
Prediction configuration: U0 = 5 m/s
</pre>

The optimization exited with 50 iterations. The objective function reduced from 4.7564760E-01 to xxx.

Once the unsteady FIML is done. We can copy the last dict from designVariableHist.txt to tutorials-master/Ramp/unsteady/predict/trained. Then, go to tutorials-master/Ramp/unsteady/predict and run `Allrun.sh`.  This command will run the primal for the baseline (SA), reference (k-omega SST), and the trained (FIML SA) models, similar to the steady-state case.

The following animation shows the comparison among these prediction case. The trained SA model significantly improves the spatial temporal evolution of velocity fields.

<img src="{{ site.url }}{{ site.baseurl }}/images/tutorials/Ramp_ufiml.png" width="400" />

Fig. 2 Comparison among the reference, baseline, and trained models.

{% include links.html %}
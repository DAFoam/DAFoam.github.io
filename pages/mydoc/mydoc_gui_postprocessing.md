---
title: Optimization Post Processing GUI
keywords: gui, post, processing
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_gui_postprocessing.html
folder: mydoc
---

PvOptPostProcessing and PvOptView are Paraview based graphical user interfaces included in the PvOptGUI plugin to aid users in post processing their data. PvOptPostProcessing can be used to view the iterations from a DAFoam log file, while PvOptView can be used to view results from any .hst file. PvOptView provides a ParaView interface to open OptView, a post-processing utlity from [pyOptSparse](https://github.com/mdolab/pyoptsparse). These GUI's are currently in the beta version.

---

To post process data, first open ParaView with PvOptGUI following the instructions mentioned on [this page](mydoc_gui_overview.html).

## PvOptPostProcessing

Open the PvOptPostProcessing source by first clicking the sources tab in the toolbar at the top of the screen. Then hover over PvOptGUI and select PvOptPostProcessing.

Once the source is loaded, simply click *select log file* and choose the DAFoam log file you wish to post process.

Finally, click the *Post Process* button to open the GUI

![pvOptPostProcessing](/images/tutorials/GUI_pyGUI_post.png)

## PvOptView

One can open the PvOptView source by first clicking the sources tab in the toolbar at the top of the screen. Then hover over PvOptGUI and select PvOptView.

Once the source is loaded, simply click *select history file* and choose the .hst file you wish to post process.

Finally, click the *Post Process* button to open the GUI

![pvOptView](/images/tutorials/GUI_optView.png)

[OptView](https://github.com/mdolab/pyoptsparse/blob/master/pyoptsparse/postprocessing/OptView.py) is an open-source post-processing utlity from pyOptSparse

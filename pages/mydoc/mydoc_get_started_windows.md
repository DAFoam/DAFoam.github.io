---
title: Command to start the Docker image on Windows
keywords: run, tutorial, windows
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_get_started_windows.html
folder: mydoc
---

Use the following command to start the DAFoam Docker image on Windows. All the other commands are same as Linux and MacOS.

<pre>
docker run -it --rm -u dafoamuser --mount "type=bind,src=%cd%,target=/home/dafoamuser/mount" -w /home/dafoamuser/mount dafoam/opt-packages:v2.0.2 bash
</pre>

{% include links.html %}

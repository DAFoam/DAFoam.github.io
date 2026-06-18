---
title: Download DAFoam image
keywords: docker
summary: The pre-compiled DAFoam image is ready to use for various operating systems.
sidebar: mydoc_sidebar
permalink: get-started-download-docker.html
folder: mydoc
---

The easiest way to run DAFoam optimizations is to use the **pre-compiled package** through Docker Hub. For advanced users, refer to [this page](installation-source.html) on how to compile everything from scratch. The Get Started section assumes you use the pre-compiled package.

Before downloading the pre-compiled package, you need to install **Docker**. Follow the installation instructions for

- [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)
- [MacOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac/)
- [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu)

Once the above installation is done, open a **Terminal** (Linux and MacOS) or **Command Prompt** (Windows) and verify the Docker installation by running:

<pre>
docker --version
</pre>

You should be able to see your installed Docker version.

Once Docker is installed and verified, run this command from the terminal to download the DAFoam image:

<pre>
docker pull dafoam/opt-packages:{{ site.latest_version }}
</pre>

Now you are ready to [run DAFoam optimization](get-started-run.html).


{% include links.html %}

---
title: Download DAFoam image
keywords: docker
summary: The pre-compiled DAFoam image is ready to use for various operating systems.
sidebar: mydoc_sidebar
permalink: mydoc_get_started_download_docker.html
folder: mydoc
---

The easiest way to run DAFoam optimizations is to use the **the pre-compiled package** through Docker Hub. Before downloading the pre-compiled package, you need to install **Docker**. Follow the installation instructions for [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu), [Fedora](https://docs.docker.com/install/linux/docker-ce/fedora), [CentOS](https://docs.docker.com/install/linux/docker-ce/centos), [MacOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac/), and  [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows/). 

Here we give examples for Ubuntu, MacOS, and Windows.
 
- If you use **Ubuntu 18.04**, install the latest Docker by running this command in the terminal:

  <pre>
  sudo apt-get remove docker docker-engine docker.io containerd runc && sudo apt-get update && sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent   software-properties-common -y && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && sudo add-apt-repository "deb [arch=amd64] https:// download. docker.com/linux/ubuntu $(lsb_release -cs) stable" && sudo apt-get update && sudo apt-get install docker-ce -y
  </pre>
  
  Then you need to add your user name to the docker group by running this command:
  
  <pre>
  sudo usermod -aG docker $USER
  </pre>
  
  After this, you need to **logout and re-login your account** to make the usermod command effective. 

- If you use **MacOS**, click **Get Stable** to download the installer (`Docker.dmg`) from [here](https://hub.docker.com/editions/community/docker-ce-desktop-mac). Double click `Docker.dmg` and follow the instructions to install. Once done, open the Docker Desktop app. When asked, create a Docker Hub account, and use it to login the Docker Desktop app. Keep the Docker Hub app open when runing Docker commands.

- If you use **Windows**, click **Get Stable** to download the installer (`Docker Desktop Installer.exe`) from [here](https://hub.docker.com/editions/community/docker-ce-desktop-windows/). Double click `Docker Desktop Installer.exe` and follow the instructions to install. Once done, open the Docker Desktop app. When asked, create a Docker Hub account, and use it to login the Docker Desktop app. Keep the Docker Hub app open when runing docker commands.

Once the above installation is done, open a terminal and verify the docker installation by:

<pre>
docker --version
</pre>

You should be able to see your installed Docker version.

Once the Docker is installed and verified, run this command from the terminal to download the DAFoam image:

<pre>
docker pull dafoam/opt-packages:v2.0.0
</pre>

Now you are ready to [run DAFoam optimization](mydoc_get_started_run.html).


{% include links.html %}

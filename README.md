# Yazi

As a school project, we decided to create a bunch of pentest containers all available in open source and easily customisable.
In addition to the containers we added an iso based on Alpine Linux containing natively the solution.

## Overview

This project uses podman as our container solution instead of docker. The main script to manage container are made in python to make it almost native for every Linux distribution.
For now its only fully operationnal on Linux, we will probably make it available for Windows in the future.

## Features

- 5 base images available
- Fully customisable images
- Shared workspace between host/container
- CLI Script to make use easier
- Fully documented

## Installation

To install yazi you can : 

1. Clone the repository:
   ```bash
   git clone https://github.com/ebnaii/yazi.git
   cd yazi
   chmod +x install.sh
   ./install.sh
2. Run : 
   ```bash
   curl https://raw.githubusercontent.com/ebnaii/yazi/main/install.sh?token=GHSAT0AAAAAACUJXZ7NBRDV2CN2MADBB3L6ZUINEUA | bash
## Usage 

Installation script will create an alias to call the main script.
From that you can start every command with the script using : **```yazi COMMAND```**, you can refer to the help menu to check all the commands available by running **```yazi help```**.

We provide a base of 5 images for your containers but you can easily custom them by looking at each Dockerfile. Don't like a tools ? Delete it and replace it with a tool you prefer.
You can even create whole Dockerfile for special purposes by adding a folder with a Dockerfile and your config files in ```yazi/scripts/``` alongside the 5 we provide. These new images will be detected by the install script, don't forget if you want to add a version and a tag do to so in the label at the start of your Dockerfile.

You can send file from/to your host with the workspace.
There is a workspace automatically created for every container you create. On the host side, its located at **```~/.yazi/workspaces/YOUR_CONTAINER```**. On the container side, you spawn in, if you moved, its on the root at **```/workspace```**

## UNINSTALL

You can delete all the images thanks to the script, then just delete the files in your home at ```~/yazi``` and ```~/.yazi```. You will also need to delete the alias in your ```.bashrc``` or ```.zshrc```.

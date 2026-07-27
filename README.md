This repository is a (slightly) customized version of the [BYU Controlbook](https://github.com/byu-controlbook/controlbook_public/) intended for NC State University's CSC/ECE/MAE 409/509 (Control Systems for Robotics) course taught by Dr. Justin Bradley. Differences are limited to details and logistics rather than substance.

---
# **Setting up Controlbook Code and Python Environment**

# Introduction

The goal of this document is to illustrate for how to setup your environment for doing the labs and homework for the [Controlbook](https://github.com/byu-controlbook/controlbook_public). This document is based on a similar document in included as part of the [Controlbook repo](https://github.com/byu-controlbook/controlbook_public/blob/master/Setting_Up_Controlbook_Code_and_Python_Environment_for_ME_EN_431___EC_EN_483.pdf). The goal is to minimize that document to only the necessary pieces for CS students and others already familiar with developing software projects in Python.

# Prerequisites

You'll need to ensure you've got a few things installed and configured properly for use in a terminal/shell (or similar).

* **Python**: This class's code was designed around Python 3.10/3.11, but as of 2025-01-20 appears to work well on Python 3.13.1.
  * *NOTE:* I have found using Homebrew on macOS to be very convenient for installing and managing python installations. 
* **Git**: You either need a command line (most likely) version of `git` or [GitHub Desktop](https://github.com/apps/desktop).
* **IDE**: I'm using [Visual Studio Code](https://code.visualstudio.com/), but you're welcome to use whatever you like to develop in Python!

# How to Setup Your Repo

We recommend making a private clone of [this repo](https://github.com/jmb275/controlbook) and using it to maintain your code for the course. Using these steps allows you to maintain connection to this repo as an upstream remote to receive updates, but without pushing to it.

1. Create a private repo
2. Clone the repo and connect to upstream remote
   * Clone your new private, personal repo
   * Connect to upstream remote (this repo) by running (in your shell):
     ```{.bash}
     git remote add upstream https://github.com/jmb275/controlbook.git
     ```
   * Type `git remote -v` to ensure connection to both repos
3. Fetch and merge from the public repo to get the first copy of it and get changes in the future:
   ```{.bash}
   git fetch upstream <branch>
   git merge --allow-unrelated-histories upstream/<branch>
   git push
   ```
   
**NOTE:** Be sure to substitute the correct branch for `<branch>` above. This will be given to you.

# Setting up Python

You are welcome to configure your Python environment however you like. However, we recommend the following approach, which is also the approach the TA will take when grading.

## Virtual Environments

As an aside, virtual environments greatly enhance the ability to customize a development environment to specific projects -- a growing complexity in software development. A virtual environment essentially allows developers to provide small configuration files for development dependencies (e.g., library, binary) that are easily shared and allow a developer to quickly and easily obtain the *correct* environment. There are at least two main benefits to this approach:

* **Easier collaboration**: It makes it easier to collaborate and debug when developing as a team. The virtual helps ensure everyone has the same develoment environment.
* **Dependency isolation**: Each project may have different versions of the same libraries thereby requiring deconfliction. 

## Setting up `venv`

We recommend using `venv` to configure your Python environment primarily because it is built in, easy to setup, and minimizes complexity for everyone's installation. `venv` basically creates a `.venv` directory into which python dependencies are installed, and which houses configuration files to setup the correct environment.

You can eiher setup your `venv` in VSCode or in your terminal/shell. Either way works, you just need to ensure the `venv` is "activated" before you run your code.

1. Setup the `venv`:
   * **Option 1: VSCode**: Use the information [here](https://code.visualstudio.com/docs/python/environments#_creating-environments) to setup the virtual environment. When asked, select the correct python version, and use `requirements.txt` as the file from which to install dependencies. Finally, ensure a terminal is started with that virtual environment (the terminal should have a `.venv` next to the command prompt).
   * **Option 2: CLI**: Run the following in your shell:
     ```{.bash}
     python -m venv .venv
     source .venv/bin/activate # On Linux/macOS
     .\.venv\Scripts\activate # On Windows
     ```
2. Install required libraries: **after activating the virtual environment** you can install the libraries into the `venv` by running:
   ```{.bash}
   pip3 install -r requirements.txt
   ```

# Test Matplotlib

Now that everything is setup check to make sure it all works. Navigate to an example file (e.g., `_A_arm/python/hw03_armSim.py`) and run it. You can run this from VSCode or from your shell and it should work. If it doesn't, please let us know.

## Common Errors

On macOS we have noticed that `tkinter` does not install when installing python using Homebrew. Running `brew install python-tk` resolves this.


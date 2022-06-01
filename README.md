[![PyPI version](https://badge.fury.io/py/mypydot.svg)](https://badge.fury.io/py/mypydot)
![CI](https://github.com/andres-ortizl/mypydot/actions/workflows/main.yml/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mypydot)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mypydot)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=bugs)](https://sonarcloud.io/summary/new_code?id=mypydot)

## Mypydot

Mypydot is a tool created for managing your dotfiles using a Python application

# Motivation

I just wanted the basic functionality to manage my own dotfiles. I decided to do it in Python because It seems more
natural
to me rather than do It using shell scripting.

## Install

```pip install mypydot```

## Instructions

### Create new dotfiles

Using it for the first time : ```mypydot --option create``` . This command will create a new folder called .mypydotfiles
in your $HOME directory. In this folder you will find the following folder structure :

| Folder     |                                                                                                                               | 
|------------|-------------------------------------------------------------------------------------------------------------------------------|
| `language` | In case you want to save some dotfiles related with your favourite programming languages                                      |  
| `os`       | Operating system dotfiles                                                                                                     |  
| `shell`    | Everything related to bash & zsh, etc..                                                                                       |  
| `tools`    | Docker, Git, Editors, etc. You can also find here a few almost empty scripts for storing your aliases, exports and functions. |  
| `conf.yml` | This file contains every file that you want to track in your dotfiles repository, feel free to add & remove symlinks !        |  

Once you run this process you will notice that you have a few new lines your .bashrc and in your .zshrc

```
export MYPYDOTFILES=/Users/username/.mypydotfiles
source $MYPYDOTFILES/shell/main.sh
```

This lines will be used to source yours aliases, exports and functions to be available in your terminal.
Besides that, nothing else is edited.

### Resync dotfiles ( for restoring or sync new files)

```mypydot --option sync``` . This will iterate again over your .conf.yml file trying to sync new dotfiles.

# References

https://github.com/mathiasbynens/dotfiles

https://github.com/CodelyTV/dotly

https://github.com/denisidoro/dotfiles

https://github.com/webpro/awesome-dotfiles

Thank you!
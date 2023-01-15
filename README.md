[![PyPI version](https://badge.fury.io/py/mypydot.svg)](https://badge.fury.io/py/mypydot)
![CI](https://github.com/andres-ortizl/mypydot/actions/workflows/main.yml/badge.svg)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=coverage)](https://sonarcloud.io/summary/new_code?id=mypydot)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=mypydot&metric=bugs)](https://sonarcloud.io/summary/new_code?id=mypydot)

## Mypydot

Mypydot is a tool created for managing your dotfiles using a Python application

## Showcase

small screenshots of the application
![home](screenshots/home.png)
![selection](screenshots/selection.png)
![installing](screenshots/installing.png)
![bye](screenshots/bye.png)

# Motivation

I just wanted the basic functionality to manage my own dotfiles. I decided to do it in Python because It seems more
natural
to me rather than do It using shell scripting.

## Install

```pip install mypydot```

## Instructions

### Create new dotfiles

Using it for the first time : ```mypydot``` . This command will create a new folder called .mypydotfiles
in your $HOME directory. In this folder you will find the following folder structure :

| Folder     |                                                                                                                               |
|------------|-------------------------------------------------------------------------------------------------------------------------------|
| `language` | In case you want to save some dotfiles related with your favourite programming languages                                      |
| `os`       | Operating system dotfiles                                                                                                     |
| `shell`    | Small setup of aliases and exports that can be accessed from everywhere                                                       |
| `config`   | Docker, Git, Editors, etc. You can also find here a few almost empty scripts for storing your aliases, exports and functions. |
| `conf.yml` | This file contains every file that you want to track in your dotfiles repository, feel free to add & remove symlinks !        |

Once you run this process you will notice that you have a few new lines your .bashrc and in your .zshrc

```
export MYPYDOTFILES=/Users/username/.mypydotfiles
source $MYPYDOTFILES/shell/main.sh
```

This lines will be used to source yours aliases, exports and functions to be available in your terminal.
Besides that, nothing else is edited.

### Resync dotfiles

Select your existing conf file and the modules you want to resync / install

# References

https://github.com/mathiasbynens/dotfiles

https://github.com/CodelyTV/dotly

https://github.com/denisidoro/dotfiles

https://github.com/webpro/awesome-dotfiles

Thank you!

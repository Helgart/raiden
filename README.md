# Raiden infrastructure #

## Command usage ##
```
#!bash

usage: raiden [-h] [--platform PLATFORM] [--applications APPLICATIONS] action

positional arguments:
  action                Define launcher action, can be start, stop, restart, delete

optional arguments:
  -h, --help                                   show this help message and exit
  --platform PLATFORM              Define the platform folder path
  --applications APPLICATIONS Define the application folder path
```

## What is Raiden ##
Raiden is made to help you manage a server using a docker base architecture.

## Dependencies ##
For Raiden to work you need the following package to be installed with **docker** and **python 2.7** (not tested on anterior versions for now) :

* python-yaml

## Configuration files ##

### Configuration file exemple ###


```
#!yaml

name: nginx
order: 1
options:
    detached: true
    interactive: true
    tty: true
    expose:
        - "80:80"
```
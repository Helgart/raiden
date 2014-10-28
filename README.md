# Raiden infrastructure #

## Command usage ##
```
#!bash

usage: raiden [-h] [-v V] [--pools POOLS] [--targets TARGETS] action

positional arguments:
  action                        Define launcher action, can be start, stop, restart, delete

optional arguments:
  -h, --help                   show this help message and exit
  -v V                           Define log level from 0 (debug) to 3 (error only), default 1 (info)
  --pools POOLS         Define the container pool folder path
  --targets TARGETS  List of targeted containers. if not defined, command will target all containers
  --env ENV                 Define environement to launch
```

## What is Raiden ##
Raiden is made to help you manage a server using a docker base architecture.

## Dependencies ##
For Raiden to work you need the following package to be installed with **docker** and **python 2.7** (not tested on anterior versions for now) :

* python-yaml

## Configuration files ##

Each container folder must have a *raiden.yml* file wich define how container must run, and how it will interact with others. If no configuration file, container will ignored by raiden since he won't know what to do with it. For now oly 3 parameters are mandatory : *name* and *type*.

### Parameters details ###

| Name | Description | Value exemple | Mantatory |
|---------|-----------------|----------|--------------|
| name  | Name of container, will be used by raiden to name images and containers   | apache | **yes** |
| type | Can be *platform*, *application* or *layer*, application type container will be launching first to let platform type perfom some links with them | platform | **yes** |
| options | Running options for container, explained just after |  | no |
| environement | Override options depending on environement defined on --env option |  | no |

### Running options details ###

| Name | Description | Value exemple |
|---------|-----------------|----------|
| expose | List of port to follow from host to container. Use the synthax *host_port:container_port* | 8080:80 |
| mount | List of folders to follow from host to container. Use the synthax *host_folder:container_folder* | /some/local/path:/some/container/path |
| link | list of container we should have access to. Using docker *--link* option | yass |
| depend | List of image dependencies, those image will be run (or just build) first | laravel |

### Configuration file exemple ###


```
#!yaml

## Default configuration
name: apache
type: platform
options:
    expose:
        - "80:80"
    mount:
        - "pool:/etc/apache2/conf.d"
    link:
        - other_container_name
    depend:
        - php

## Environement overloading
environements:
    dev:
       expose:
            - "8080:80"
```

## Environements ##

Even if it's just for opened ports or more, you always need some specific configuration depending on where ou run your application.
In raiden configuration file you can add environements using *environement* parameter to override *options* parameters.

## Launching order ##

Containers will be launch by their dependencies order. If you have linked containers, those container will be launch first.

## Want to know more ? ##

Platform exemple, or container type definition ? See our wiki for more details !
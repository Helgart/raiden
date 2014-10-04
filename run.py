#!/usr/bin/python

import os

path = os.path.dirname(os.path.realpath(__file__))

os.system("docker build -t raiden " + path + "/nginx")
os.system("docker run --name raiden -ti -p 80:80")

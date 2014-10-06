#!/usr/bin/python

import os
import launcher.finder

path = os.path.dirname(os.path.realpath(__file__))
modules = os.path.realpath(path + "/platform")

launcher.finder.load(modules)

#!/usr/bin/env python
from os import path
from sys import argv
from subprocess import call

for item in argv[1:]:
    full_path = path.abspath('./' + item)
    call(['gnome-terminal','-e', 
          "bash -c '" +  full_path + ";read'"])

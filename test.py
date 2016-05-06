#!usr/bin/python
#coding=utf-8

import os
import subprocess

output = subprocess.check_output("ls")
print output

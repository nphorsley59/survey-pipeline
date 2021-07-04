""" Copy the code snippet below to set the system path of a script to the 
root directory of the repository. """

import os
import sys

# locate root dir
flare = '\\flare.py'
path = os.getcwd()
while not os.path.isfile(path + flare):
    path = os.path.dirname(path)
sys.path.append(path)
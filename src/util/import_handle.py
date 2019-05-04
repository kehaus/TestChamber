""" 
contains TestChamber repository base path

This determines base path of local repository. In this way it allows to import 
data from different locations of the repository.

date:	04/30/2019
"""


import os

BASE_PATH = os.getcwd()

DATA_PATH = os.path.join(BASE_PATH, "DATA")


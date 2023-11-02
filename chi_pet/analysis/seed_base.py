#!/usr/bin/env python
# Basic
import sys
import os
import pdb
import re
import yaml
from subprocess import call
# Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import *
from .base_funcs import *
from .analyzer import Analyzer
# import cv2


"""@package docstring
File: seed_base.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Base code to collect and hold all data from one seed
"""


class SeedBase(Analyzer):
    def __init__(self, path, **kwargs):
        Analyzer.__init__(self, path, subnodeType=None, **kwargs)

    def MakeSeedLabel(self):
        snum = re.findall(r"\d*\.?\d+", self.name)
        try:
            slabel = r's $=$ {}'.format(snum[-1])
            return slabel, int(snum[-1])
        except BaseException:
            print("Could not make seed label. Using name of seed directory.")
            return self.name, 0


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

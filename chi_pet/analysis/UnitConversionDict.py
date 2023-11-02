#!/usr/bin/env python
# In case of poor (Sh**y) commenting contact alamson@flatironinstitute.org
# Basic
import sys
import os
import pdb
import yaml
# Analysis
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from math import *

'''
Name: UnitConversionDict.py
Description: Object that takes in dictionary of parameterts to convert from
             sim units to real units. Used for labeling parameters in graphs
Input: Either yaml file or dictionary of units
'''

# Class definition


class UnitConversionDict(object):
    def __init__(self, dictionary='', yaml_file=''):
        self.ud = {}
        if dictionary:
            self.ud = dictionary
        elif yaml_file:
            self.ud = yaml.load(os.path.abspath(yaml_file))
        else:
            print("No dictionary or yaml_file given to UnitConversionDict\
                    class")

    def __getitem__(self, k):
        if k in self.ud:
            return self.ud[k]
        else:
            return ('', 1.0, float)


##########################################
if __name__ == "__main__":
    print("UnitConversionDict not implemented for executable use.")

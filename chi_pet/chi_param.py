#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import sys
import os
# Testing
# import pdb
# import time, timeit
# import line_profiler
# Analysis
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import h5py
# import yaml
# from math import *
# Speed
# from numba import jit
# Other importing


"""@package docstring
File: chi_param
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""


class ChiParam(object):

    """!Class that holds all the values of a changing parameter."""

    def __init__(self, name, vals=None, level=0):
        """!TODO: to be defined1.

        @param name: TODO
        @param vals: TODO

        """
        self._name = name
        self._vals = vals
        self._level = level


class ChiParamVariations(object):

    """!Docstring for ChiParamVariations. """

    def __init__(self, chi_param_list=None):
        """!Initialize a list of varied parameters to make chi_nodes

        @param chi_param_list: TODO

        """
        self._chi_param_list = chi_param_list


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

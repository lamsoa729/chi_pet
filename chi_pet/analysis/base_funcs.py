#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import numpy as np
import sys
import os
import pdb
# Analysis
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from math import *

'''
Name: base_funcs.py
Description: Library that holds general functions and classes used with
             used with analysis base classes
'''


class VirtualMethodError(Exception):
    """ Error when the method you are trying to use has not been defined in
        the inherited class.
    """

    def __init__(self, method, className):
        err_str = "Must right {} method in derived class {}.".format(
            method, className.__name__)
        Exception.__init__(self, err_str)


def create_datadir(path, datadir_name='data'):
    """ Create a directory to put graphs and run/simulation data files
    Inputs:  path         = path to directory where data directory will live
             datadir_name = name of the data directory that will be created
    Outputs: data_path    = absolute path to data directory
    """
    try:
        abs_path = os.path.abspath(path)
    except BaseException:
        print(" ## Could not find the absolute path of {} directory.".format(path))
        raise

    data_path = os.path.join(path, datadir_name)

    # Try to make a data directory but if one exists just skip it
    if not os.path.isdir(data_path):
        try:
            os.mkdir(data_path)
        except OSError as error:
            print(
                "Could not make data directory {} already exists.".format(data_path))
            raise

    return data_path


# Define a moving average


def moving_average(a, n=2):
    """ Define moving average
    Inputs:  a = array of values to be averaged over
             n = number of data points to average over
    Outputs: array of values created by the moving average
    """
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return np.divide(ret[n - 1:], n)


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

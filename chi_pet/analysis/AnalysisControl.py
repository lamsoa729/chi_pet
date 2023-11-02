#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact alamson@flatironinstitute.org
# Basic
import sys
import os
from parser_setup import parser_setup
# Testing
# import pdb
# import time, timeit
# import line_profiler
# Analysis
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import pandas as pd
# import yaml
# from math import *
# Speed
# from numba import jit
# Other importing
# sys.path.append(os.path.join(os.path.dirname(__file__), '[PATH]'))


"""@package docstring
File:
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""


class AnalysisControl():

    """!Virtual class to control analysis programs"""

    def __init__(self, opts, Test=None, Seed=None, Sim=None, Run=None):
        """!Initialize control structure with argument parser options

        @param opts: TODO

        """
        self._opts = opts
        self._cwd = os.getcwd()
        # Object types, must be defined in derived class
        self._Test = Test
        self._Seed = Seed
        self._Sim = Sim
        Self._Run = Run

        # Run analysis
        self.ReadOpts()
        self.ProgOpts()

    def ReadOpts(self):
        """!Read options from argpaser and estabilish working directory
        @return: void

        """
        if not self.opts.workdir:
            self.opts.workdir = self.cwd

        # Figure out analyzer
        if self.opts.test:
            self.test = self._Test(self.opts.workdir)
        elif self.opts.seed:
            self.analyzer = self._Seed(self.opts.workdir)
            # self.RunSeed()
        elif self.opts.sim:
            self.analyzer = self._Sim(self.opts.workdir)
        else:
            self.analyzer = self._Run(self.opts.workdir)

    def ProgOpts(self):
        """!Execute methods based on commandline options given
        @return: void

        """
        if self.opts.test:
            self.test.RunTests()
            return

        # Run through options
        if self.opts.load:
            analyzer.Load()
        elif self.opts.analyze or self.opts.overwrite:
            analyzer.Analyze(overwrite_flag=self.opts.overwrite)
        if self.opts.write:
            analyzer.Save()
        if self.opts.graph:
            analyzer.Graph()


##########################################
if __name__ == "__main__":
    print "Not implemented yet"

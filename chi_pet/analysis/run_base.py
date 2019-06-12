#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import sys
import os
import pdb
# Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import *
from .path_funcs import Get_dir_names
from .analyzer import Analyzer
from .sim_base import SimBase
# from seed_base import SeedBase
from base_funcs import *


'''
Name: run_base.py
Description:
Input:
Output:
'''


class RunBase(Analyzer):

    """!Docstring for RunBase. """

    def __init__(self, path="cur_dir", subnode_path="simulations",
                 subnodeType=SimBase, **kwargs):
        """!Initialize run base with simulation base.

        @param path: TODO
        @param **kwargs: TODO

        """
        Analyzer.__init__(self, path, nodeType=nodeType, **kwargs)

        if self._path is None:
            self._path = os.path.abspath(os.getcwd())
        elif not os.path.isdir(self._path):
            raise FileNotFoundError("Directory [{}] does not exist."
                                    "Try again.".format(self._path))
        else:
            self._path = os.path.abspath(self._path)

        self._name = self._path.split('/')[-1]
        self.simdir_path = os.path.join(self._path, subnode_path)

        # Objects to be filled later
        self._subnodes = []
        self.p_names = []
        self.p_range = {}
        self.p_vals = {}

        self.simType = simType
        # self.seedType = seedType

        # flags
        self.analyze_flag = False

        # Data frame for entire run
        self.run_df = pd.DataFrame()

    # Creates sim objects and stores them in a list
    def Collect(self):
        self._subnodes = [self._subnode(os.path.join(self.simdir_path, sim_path))
                          for sim_path in Get_dir_names(self.simdir_path)]
        # Sometimes _subnodes are empty so its necessary to make sure you get
        empty_subnodes = True
        # data from a full one.
        for sim in self._subnodes:
            if len(sim.seeds) != 0:
                empty_subnodes = False
                # FIXME This is not a good way to get parameter values.
                #       Better to get them directly from the files that make up
                #       the seed runs. That way there are no rounding errors.
                self.p_names = list(sim.params.keys())
                break
        if empty_subnodes:
            raise RuntimeError(
                "Could not find any simulations with valid seeds.")
        # Get range of parameter values
        for pn in self.p_names:
            self.p_vals[pn] = []
            for sim in self._subnodes:
                if len(sim.seeds) == 0:
                    continue  # In case a sim is empty of seeds
                self.p_vals[pn] += [float(sim.params[pn])]
            self.p_vals[pn] = np.unique(self.p_vals[pn]).tolist()
            self.p_range[pn] = (min(self.p_vals[pn]), max(self.p_vals[pn]))

    def WriteRunDataFrame(self):
        """Output data frame that can be read back into this function for quick
        graphing.
        @return: void, output dataframe file to run directory
fig, ax = plt.subplots(figsize=(10,7))
        """
        if not self.datadir:
            self.datadir = create_datadir(self._path)
        with open("{}_Seed.dat".format(os.path.join(self.datadir, self.run_name)), 'w') as df:
            self.run_df.to_csv(df, sep=" ", index=False)

    def ReadRunDataFrame(self, run_df_file=None, uc=""):
        """Read in dat file written out by WriteDataFrame function

        @param run_df_file: data frame file for run from WriteDataFrame
        @return: void, change or create self.run_df from data file

        """
        if not self.datadir:
            self.datadir = os.path.join(self._path, 'data')
        if not self.run_df.empty and bool(uc):
            self.p_names = list(
                set(list(self.run_df)).intersection(list(uc.ud.keys())))
            return

        # If Run has not created run data frame, find it in the data path
        elif not run_df_file:
            dat_files = []
            dat_files += [f for f in os.listdir(self.datadir)
                          if f.endswith('.dat')]
            # If only one .dat file exists in data_dir, try to use that as your
            # data frame
            if len(dat_files) == 0:
                raise RuntimeError("No run dataframe files to choose from,",
                                   " in {}.".format(self.datadir))
            elif len(dat_files) == 1:
                run_df_file = os.path.join(self.datadir, dat_files[0])
            else:
                raise RuntimeError("Too many possible run dataframe files ",
                                   "to choose from in {}.".format(self.datadir))
        try:
            print(run_df_file)
            run_df_file = os.path.abspath(run_df_file)
        except BaseException:
            # print "Could not find path to {}".format(run_df_file)
            raise

        self.run_df = pd.read_csv(run_df_file, delimiter=' ', header=0)

        if bool(uc):
            self.p_names = list(
                set(list(self.run_df)).intersection(list(uc.ud.keys())))
        else:
            self.p_names = list(self.run_df)
        return

    # Simulation analysis functions
    def Analyze(self, overwrite_flag=False):
        if not self.analyze_flag:
            if len(self._subnodes) == 0:
                self.Collect()
            for sim in self._subnodes:
                sim.AnalyzeSim(overwrite_flag=overwrite_flag)
            self.analyze_flag = True

    def OrderSimList(self, param=''):
        """ Method to order self._subnodes list by param value """
        # If a parameter is not given print warning and use the first parameter
        if not param:
            param = self.p_names[0]
            print(("*** WARNING: No parameter given to order _subnodes, ",
                   "using parameter {} to order list.*** ".format(param)))
        self._subnodes.sort(key=lambda sim: sim.params[param])
        return param

    # def Read_subnodes(self, analysis_files):
        # for sim in self._subnodes:
        # sim.Read(analysis_files, header=0, index_col=0)

    def PrintRunData(self):
        for sim in self._subnodes:
            sim.PrintSimData()

    _Collect = Collect
    _Graph_subnodes = Graph_subnodes


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

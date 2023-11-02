#!/usr/bin/env python

# Basic
import sys
import os
import pdb
import ast
from subprocess import call
import re
# Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from path_funcs import Get_dir_names
from seed_base import SeedBase
from math import *
from base_funcs import *

"""!@package docstring
File: sim_base.py
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description: Base class that holds multiple seeds that have the same
parameters aka a sim.
"""

class SimBase(object):
    def __init__(self, simdir, rundir=None, datadir=None, seedType=SeedBase):
        if simdir is None:
            self.sim_path = os.path.abspath(os.getcwd())
        elif not os.path.isdir(simdir):
            raise FileNotFoundError("Directory [{}] does not exist."
                                    "Try again.".format(simdir))
        else:
            self.sim_path = os.path.abspath(simdir)
        self.name = self.sim_path.split('/')[-1]
        self.title = self.MakeSimTitle(self, self.sim_path)
        self.params = self.MakeSimParamDict(self, self.sim_path)
        if rundir is None:
            self.rundir = rundir
        elif not os.path.isdir(rundir):
            raise FileNotFoundError("Directory [{}] does not exist."
                                    "Try again.".format(rundir))
        else:
            self.rundir = rundir

        self.datadir = datadir

        self.seedType = seedType
        self.seeds = []

        self.CollectSeeds(seedType)
        print("*** Collected sim {} ***".format(self.name))

    def CollectSeeds(self, seedType):
        seed_pattern = re.compile(r"s\d+")

        # Make list of seeds of type seedType
        self.seeds = [seedType(os.path.join(self.sim_path, sd))
                      for sd in Get_dir_names(self.sim_path) if seed_pattern.match(sd)]
        self.seeds.sort(key=lambda sd: sd.seed_num)

    def WriteSimData(self):
        # Create data dir in the correct path
        if not self.datadir:
            if not self.rundir is None:
                self.datadir = create_datadir(self.rundir)
            else:
                self.datadir = create_datadir(self.sim_path)
        # Write all seed data
        # for sd in self.seeds:
        #     sd.WriteAllData()

    @staticmethod
    def MakeSimParamDict(self, sim_path, uc=''):
        params = {}
        sim_name = sim_path.split('/')[-1]
        # Check for an MD5 hash to make sure we don't bomb
        is_hash = re.findall(r"([a-fA-F\d]{32})", sim_name)
        if len(is_hash) > 0:
            return params
        p_name = re.findall("[a-zA-Z]+", sim_name)
        p_value = re.findall(r"\d*\.?\d+", sim_name)
        # Delete duplicate variables

        def list_duplicates(seq):
            seen = set()
            seen_add = seen.add
            return [idx for idx, item in enumerate(seq)
                    if item in seen or seen_add(item)]
        ind_dup = list_duplicates(p_name)
        for i in sorted(ind_dup, reverse=True):
            del p_name[i]
            del p_value[i]

        # CJE stuff
        while 'e' in p_name:
            p_name.remove('e')
        match_number = re.compile(
            r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        p_value2 = re.findall(match_number, sim_name)

        for p, v in zip(p_name, p_value2):
            if uc:
                params[p] = ast.literal_eval(v) * uc[p][1]
            else:
                params[p] = ast.literal_eval(v)

        return params

    @staticmethod
    def MakeSimTitle(self, sim_path, uc=''):
        name = sim_path.split('/')[-1]
        # Check for an MD5 hash to make sure we don't bomb
        is_hash = re.findall(r"([a-fA-F\d]{32})", name)
        if len(is_hash) > 0:
            label = r"hash {}".format(is_hash)
            return label
        else:
            label = ""
        param = re.findall("[a-zA-Z]+", name)
        p_value = re.findall(r"\d*\.?\d+", name)

        # CJE Stuff for scientific notation
        while 'e' in param:
            param.remove('e')
        match_number = re.compile(
            r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *-?\ *[0-9]+)?')
        p_value2 = re.findall(match_number, name)

        slabel = r'{} $=$ {}{}, '
        for p, v in zip(param, p_value2):
            if uc:
                label += slabel.format(p,
                                       str(ast.literal_eval(v) * uc[p][1]), uc[p][0])
            else:
                label += slabel.format(p,
                                       str(ast.literal_eval(v)), '')
        return label[:-2]

    def ReadSeedDictsForSim(self, data_file_list='',
                            header=None, index_col=None):
        for sd in self.seeds:
            sd.MakeDataDict(data_file_list,
                            header=header,
                            index_col=index_col)
        print("    Sim read ({}) ".format(self.name))

    def PrintSimData(self):
        for sd in self.seeds:
            sd.PrintData()

    def DelDataArray(self):
        raise NotImplementedError("DelDataArray")

    def GraphSimulation(self, png_name):
        raise VirtualMethodError("GraphSimulation")

    def AnalyzeSim(self, overwrite_flag=False):
        print(" ----- Analyzing sim {} ----- ".format(self.name))
        for sd in self.seeds:
            sd.AnalyzeSeed(overwrite_flag)
            sd.SaveSeed()

    def GetParamNames(self):
        return list(self.params.keys())


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

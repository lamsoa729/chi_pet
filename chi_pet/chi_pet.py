#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Basic
import sys
import os
import shutil
import pdb
import yaml
import argparse
# Analysis
import re
from chi_parser import chi_parser
from chi_lib import *
# from ChiParams import ChiParam, ChiSim
# from ChiLaunch import ChiLaunch
# from ChiCreate import ChiCreate
# from ChiParticleSwarm import ChiParticleSwarm
# from ChiGeneticAlgorithm import ChiGeneticAlgorithm
# from ChiRun import ChiRun

'''
Name: chi_pet.py
Description: Main control program for xi(chi)-launcher. Runs all newagebob code.
Input: To view options type Chi.py -h
Output:
'''


class ChiPet(object):
    def __init__(self, opts):

        self.opts = opts
        self.yml_files_dict = {}  # combined dictionary of all yaml files
        self.cwd = os.getcwd()
        self.ChiParams = []
        self.ReadOpts()
        self.ProgOpts()

    def ReadOpts(self):
        # TODO This might not be fully integrated just yet
        if not self.opts.workdir:
            self.opts.workdir = self.cwd

        if not self.opts.states and self.opts.args_file:
            yd = CreateDictFromYamlFile(self.opts.args_file)
            self.opts.states = list(yd.keys())

    def ProgOpts(self):
        wd = self.opts.workdir  # Shortcut for work directory
        if self.opts.launch != "NOLAUNCH":
            # If no sim dirs are given find them all in simulations
            if self.opts.launch == []:
                self.opts.launch = find_dirs(os.path.join(wd, "simulations"))
                # If no dirs were found return with warning
                if self.opts.launch == []:
                    print(" No sim directories were found our given. ")
                    return
            # Find run.not and delete
            try:
                os.remove(os.path.join(wd, "run.not"))
            except OSError:
                print(
                    "run.not was not found in workdir. Might want to go searching for it.")
                pass
            # Create run.ing in workdir
            touch(os.path.join(wd, "run.ing"))
            ChiLaunch(simdirs=self.opts.launch, opts=self.opts)

        elif self.opts.create:
            touch(os.path.join(wd, "run.not"))
            c = ChiCreate(self.opts, self.opts.workdir)
            c.Create(self.opts.create)

        elif self.opts.shotgun:
            c = ChiCreate(self.opts, self.opts.workdir)
            c.Create(self.opts.shotgun)

        elif self.opts.particleswarmcreate:
            c = ChiParticleSwarm(self.opts, self.opts.workdir, 0)
            c.Create(self.opts.particleswarmcreate)

        elif self.opts.geneticalgorithmcreate:
            c = ChiGeneticAlgorithm(self.opts, self.opts.workdir, 0)
            c.Create(self.opts.geneticalgorithmcreate)

        elif self.opts.run:
            c = ChiRun(self.opts)
            c.Run(self.opts)

        elif self.opts.prep:
            seed_lst = find_seed_dirs(self.opts.workdir)
            for sd_dir in seed_lst:
                if self.opts.args_file:
                    shutil.copy(self.opts.args_file, sd_dir)
                for s in self.opts.states:
                    touch(os.path.join(sd_dir, 'sim.{}'.format(s)))

        elif self.opts.remove:
            seed_lst = find_seed_dirs(self.opts.workdir)
            for sd_dir in seed_lst:
                for fn in self.opts.remove:
                    path = os.path.join(sd_dir, fn)
                    if os.path.exists(path):
                        os.remove(path)


##########################################
if __name__ == "__main__":
    opts = chi_parser()
    x = ChiPet(opts)
    # x.MakeDirectoryStruct()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""@package docstring
File: chi_pet.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Control program for chi_pet.

"""

# Basic
import shutil
import os
# import yaml
# Analysis
# import re
from . import chi_lib as clib
from .chi_parser import chi_parser
from .old.chi_create import ChiCreate
from .old.chi_root_node import ChiRootNode
from pathlib import Path


class Chi(object):
    def __init__(self, opts):

        self.opts = opts
        self.yml_files_dict = {}  # combined dictionary of all yaml files
        self._chi_params = []
        self.read_opts()
        self.run()

    def read_opts(self):
        # TODO This might not be fully integrated just yet
        if not self.opts.workdir:
            self.opts.workdir = Path.cwd()

        if not self.opts.states and self.opts.args_file:
            yd = clib.create_dict_from_yaml_file(self.opts.args_file)
            self.opts.states = list(yd.keys())

    def run(self):
        wd = self.opts.workdir  # Shortcut for work directory
        run_not_path = wd / "run.not"
        if self.opts.launch != "NOLAUNCH":
            # If no sim dirs are given find them all in simulations
            if self.opts.launch == []:
                self.opts.launch = clib.find_dirs(wd / "simulations")
                # If no dirs were found return with warning
                if self.opts.launch == []:
                    print(" No sim directories were found our given. ")
                    return
            # Find run.not and delete
            try:
                run_not_path.unlink()
            except OSError:
                print("WARNING: 'run.not' was not found in workdir.",
                      " Might want to go searching for it.")
            # Create run.ing in workdir
            ChiLaunch(simdirs=self.opts.launch, opts=self.opts)
            running_path = wd / "run.ing"
            running_path.touch()

        elif self.opts.create:
            run_not_path.touch()
            # touch(os.path.join(wd, "run.not"))
            chi_root_node = ChiNode(self.opts)
            chi_root_node.Grow()

            # c = ChiCreate(self.opts, self.opts.workdir)
            # c.Create(self.opts.create)

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
            seed_lst = clib.find_seed_dirs(self.opts.workdir)
            for sd_dir in seed_lst:
                if self.opts.args_file:
                    shutil.copy(self.opts.args_file, sd_dir)
                for s in self.opts.states:
                    clib.touch(os.path.join(sd_dir, 'sim.{}'.format(s)))

        elif self.opts.remove:
            seed_lst = clib.find_seed_dirs(self.opts.workdir)
            for sd_dir in seed_lst:
                for fn in self.opts.remove:
                    path = os.path.join(sd_dir, fn)
                    if os.path.exists(path):
                        os.remove(path)


def main():
    """!Main function of chi_pet
    @return: void

    """
    opts = chi_parser()
    chi_obj = Chi(opts)


##########################################
if __name__ == "__main__":
    main()
    # x.MakeDirectoryStruct()

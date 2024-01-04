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
from pathlib import Path
# Main functions
from .chi_parse import parse_chi_options
from .chi_run import ChiRun
from .chi_node import ChiNode
from . import chi_lib as clib
# Analysis


class Chi(object):
    def __init__(self, opts):

        self.opts = opts
        self.read_opts()
        self.execute()

    def read_opts(self):
        if not self.opts.workdir:
            self.opts.workdir = Path.cwd()

        if not self.opts.states and self.opts.args_file:
            with self.opts.args_file.open('r') as af:
                yd = clib.load_yaml_in_order(af)
                self.opts.states = list(yd.keys())

    def execute(self):

        if self.opts.command == 'create':
            chi_root_node = ChiNode(self.opts.workdir, opts=self.opts)
            chi_root_node.make_subnodes()

        elif self.opts.command == 'run':
            pass
            c = ChiRun(self.opts)
            c.run(self.opts)

        elif self.opts.command == "launch":
            # # If no sim dirs are given find them all in simulations
            # if self.opts.launch == []:
            #     self.opts.launch = clib.find_dirs(wd / "simulations")
            #     # If no dirs were found return with warning
            #     if self.opts.launch == []:
            #         print(" No sim directories were found our given. ")
            #         return
            # # Find run.not and delete
            # try:
            #     run_not_path.unlink()
            # except OSError:
            #     print("WARNING: 'run.not' was not found in workdir.",
            #           " Might want to go searching for it.")
            # Create run.ing in workdir
            # ChiLaunch(simdirs=self.opts.launch, opts=self.opts)
            # running_path = wd / "run.ing"
            # running_path.touch()
            pass

        elif self.opts.prep:
            pass
        #     # leaf_lst = clib.find_leaf_dirs(self.opts.workdir)
        #     # for leaf_dir in leaf_lst:
        #     #     if self.opts.args_file:
        #     #         shutil.copy(self.opts.args_file, leaf_dir)
        #     #     for s in self.opts.states:
        #     #         clib.touch(leaf_dir / f'sim.{s}')

        # elif self.opts.remove:
        #     pass
        #     # leaf_lst = clib.find_leaf_dirs(self.opts.workdir)
        #     # for leaf_dir in leaf_lst:
        #     #     for fn in self.opts.remove:
        #     #         path = leaf_dir / fn
        #     #         if path.exists():
        #     #             path.unlink()


def main():
    """Main function of chi_pet
    """
    opts = parse_chi_options()
    chi = Chi(opts)


##########################################
if __name__ == "__main__":
    main()
    # x.MakeDirectoryStruct()

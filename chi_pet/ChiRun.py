#!/usr/bin/env python
import sys
import os
from subprocess import call, run
import shutil
import yaml
from .ChiLib import *
from collections import OrderedDict
import argparse
from pathlib import Path

'''
Name: ChiMain.py
Description: Main control program for xi(chi)-launcher. Runs all newagebob code.
Input: To view type ChiRun.py -h
Output: Runs seed (singular) simulations
'''


def run_parse_args():
    parser = argparse.ArgumentParser(prog='Chi.py')
    parser.add_argument('-d', '--workdir', type=str, required=True,
                        help='Name of the working directory where simulation will be run')
    parser.add_argument('-a', '--args_file', type=str,
                        help='Name file that holds the program argument list.')
    # parser.add_argument('-p', '--program', type=str, required=True,
    # help='Name of program that will be run')
    parser.add_argument('-s', '--states', nargs='+', type=str, required=True,
                        help='Name of all the states the simulation will run eg. start, build, analyze, etc.')

    opts = parser.parse_args()
    return opts


def run_args(workdir, state, args):
    action = state + '-ing'
    print("Started {} sim in {}".format(action, args))
    sys.stdout.flush()
    if os.path.exists(workdir):
        os.chdir(workdir)
        open('.' + action, 'a').close()
        status = run(args)
        os.remove('.' + action)
        if status.returncode:
            print(f"Run failed: State {state} did not succeed.")
        return status.returncode
    else:
        print(f"Run failed: could not find work directory {workdir}.")
        return 1


class ChiRun(object):
    def __init__(self, opts):
        self.opts = opts

    def Run(self, opts):
        workdir_path = Path(opts.workdir)
        args_file_path = workdir_path / opts.args_file
        args_dict = {}
        if not workdir_path.exists():
            raise FileNotFoundError("Run failed. Directory {} does not exists.".format(
                opts.workdir))

        elif not args_file_path.exists():
            raise FileNotFoundError(
                "Run failed. args.yaml file not found in {}.".format(
                    opts.workdir))
        else:
            args_dict = CreateDictFromYamlFile(args_file_path)

        print(OrderedYamlDump(args_dict, default_flow_style=False))
        for k, l in args_dict.items():
            print("File= {}, Dictionary= {}".format(k, " ".join(l)))

            if k in opts.states:
                if run_args(opts.workdir, k, l):
                    open('.error', 'a').close()
                elif os.path.exists('sim.{}'.format(k)):
                    os.remove('sim.{}'.format(k))


if __name__ == '__main__':

    opts = run_parse_args()

    c = ChiRun(opts)
    c.Run(opts)

#!/usr/bin/env python
import sys
import os
from subprocess import run
from .chi_lib import load_yaml_in_order, dump_yaml_in_order
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
    action_file = Path('.' + action)
    print("Started {} sim using args {}".format(action, args))
    sys.stdout.flush()
    if workdir.exists():
        os.chdir(workdir)
        action_file.touch()
        status = run(args)
        action_file.unlink()
        if status.returncode:
            print(f"Run failed: State {state} did not succeed.")
        return status.returncode
    else:
        print(
            f"Run failed: could not find work directory {workdir} to do action {state}.")
        return 1


class ChiRun(object):
    def __init__(self, opts):
        self.opts = opts

    def Run(self, opts):
        workdir_path = Path(opts.workdir)
        args_file_path = workdir_path / opts.args_file
        if not workdir_path.exists():
            raise FileNotFoundError(
                "Run failed. Directory {} does not exists.".format(
                    opts.workdir))

        elif not args_file_path.exists():
            raise FileNotFoundError(
                "Run failed. args.yaml file not found in {}.".format(
                    opts.workdir))
        else:
            with args_file_path.open('r') as f:
                args_dict = load_yaml_in_order(f)

        print(dump_yaml_in_order(args_dict, default_flow_style=False))
        for k, vals in args_dict.items():
            args = [str(a) for a in vals]
            sim_action = Path('sim.{}'.format(k))

            if k in opts.states:
                if run_args(opts.workdir, k, args):
                    (opts.workdir / '.error').touch()
                elif sim_action.exists():
                    sim_action.unlink()


if __name__ == '__main__':

    # TODO NEXT add this as a subparser to chi_pet.py
    opts = run_parse_args()

    c = ChiRun(opts)
    c.Run(opts)

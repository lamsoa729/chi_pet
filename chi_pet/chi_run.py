#!/usr/bin/env python
import sys
import os
from subprocess import run
from .chi_lib import load_yaml_in_order, dump_yaml_in_order
import argparse
from pathlib import Path
from .chi_parse import parse_chi_options

'''
Name: ChiMain.py
Description: Main control program for xi(chi)-launcher. Runs all newagebob code.
Input: To view type ChiRun.py -h
Output: Runs seed (singular) simulations
'''


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
        self._opts = opts

    def run(self):
        """Run simulation pipeline defined in the the args.yaml file defined as self.opts.args_file.

        Parameters
        ----------
        opts : _type_
            _description_

        Raises
        ------
        FileNotFoundError
            _description_
        FileNotFoundError
            _description_
        """

        # TODO NEXT Make these more useful for running simulations
        if not self._opts.workdir.exists():
            raise FileNotFoundError(
                "Run failed. Directory {} does not exists.".format(
                    self._opts.workdir))

        elif not self._opts._args_file.exists():
            raise FileNotFoundError(
                "Run failed. args.yaml file not found in {self._opts.workdir}.".format(
                ))
        else:
            with self._opts.args_file.open('r') as f:
                args_dict = load_yaml_in_order(f)

        # print(dump_yaml_in_order(args_dict, default_flow_style=False))
        # Loop through all states in args.yaml.
        # TODO Add option to see if sim_action file exists and only run those states.
        for run_state, vals in args_dict.items():
            args = [str(a) for a in vals]
            sim_action = Path('sim.{}'.format(run_state))

            # If sim action file exists then run the state
            if run_state in opts.states:
                if self.run_args(opts.workdir, run_state, args):
                    (opts.workdir / '.error').touch()
                elif sim_action.exists():
                    sim_action.unlink()

    @classmethod
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


if __name__ == '__main__':
    opts = parse_chi_options()

    c = ChiRun(opts)
    c.run(opts)

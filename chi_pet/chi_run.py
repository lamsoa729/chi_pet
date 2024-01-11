#!/usr/bin/env python
import sys
import os
from subprocess import run
from .chi_lib import load_yaml_in_order, dump_yaml_in_order
from pathlib import Path
from .chi_parse import parse_chi_options

'''
Name: chi_run.py
Description: 
'''


class ChiRun(object):
    def __init__(self, opts):
        self._opts = opts

    def run(self):
        """Run simulation pipeline defined in the the args.yaml file defined as self._opts.args_file.

        """

        # TODO Add option to see if sim_action file exists and only run those states.
        for run_state, vals in self._opts.args_dict.items():
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

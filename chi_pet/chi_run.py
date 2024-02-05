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


def run_args(workdir, state, args):
    current_dir = Path.cwd()
    try:
        action = state + '-ing'
        action_file = Path('.' + action)
        print("Started {} sim using args {}".format(action, args))
        sys.stdout.flush()
        if workdir.exists():
            os.chdir(workdir)
            action_file.touch()  # Keeps track of current pipeline state
            print("Running: ", args)
            status = run(args) #TODO capture output when an error occurs
            print("status: ", status)
            if status.returncode:
                raise OSError(f"Run failed: OSError occured at state {state}.")
            action_file.unlink()  # Remove once completed successfully
            return status.returncode
        else:
            # error for not finding directory
            raise FileNotFoundError(
                f"Run failed: Work directory {workdir} not found to do action {state} .")
    except:
        (workdir / '.error').touch()
        raise 
    finally:
        os.chdir(current_dir)


class ChiRun(object):
    def __init__(self, opts):
        self._opts = opts
        self._args_dict = opts.args_dict
        self._states = opts.states

    def run(self):
        """Run simulation pipeline defined in the the args.yaml file defined as self._opts.args_file.

        """

        for run_state, vals in self._args_dict.items():
            args = [str(a) for a in vals]
            sim_state = Path('sim.{}'.format(run_state))

            # If sim action file exists then run the state
            if run_state in self._states:
                run_args(self._opts.workdir, run_state, args)
                if sim_state.exists():
                    sim_state.unlink()

    def get_run_states(self):
        return self._states


if __name__ == '__main__':
    opts = parse_chi_options()

    c = ChiRun(opts)
    c.run(opts)

#!/usr/bin/env python

import argparse

"""@package docstring
File: chi_parser.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from pathlib import Path
from . import chi_lib as clib


def parse_chi_options():
    parent_parser = argparse.ArgumentParser(add_help=False)

    parent_parser.add_argument('-a', '--args_file', type=Path,
                               help='Name file that holds the program argument list.  (Used with --create option and --launch option)')
    parent_parser.add_argument('-d', '--workdir', type=Path,
                               help='Name of the working directory where simulation will be created or run.')
    parent_parser.add_argument('-s', '--states', nargs='+', type=str,
                               help='Name of all the states the simulation will run eg. start, build, analyze, etc.')

    parser = argparse.ArgumentParser(prog='chi.py', parents=[parent_parser])

    # TODO add prep functionality
    parser.add_argument('-P', '--prep', action='store_true',
                        help='Prepares simulationss to run with either states specified with -s or all argument states in --args_file.')

    # TODO add remove functionality
    parser.add_argument('-rm', '--remove', nargs='+', metavar='FILE(s)', type=Path,
                        help='Removes FILEs from seed directories.')

    # TODO add clean functionality
    parser.add_argument('-C', '--clean', action='store_true',
                        help='Remove subnode and data directory files from current work directory.')

    subparsers = parser.add_subparsers(dest='command')

    # CREATE options
    create_parser = subparsers.add_parser(
        'create', parents=[parent_parser], help='Create a simulation directory structure using various strategies.')

    create_parser.add_argument('param_files',
                               metavar='PARAM_FILE(S)', nargs='+', type=Path, default=[],
                               help='List of yaml files to be combined into a single yaml file and varied using Chi-Pet.')

    create_parser.add_argument('-r', '--replace', default=False, action='store_true',
                               help='Replace simulation file instead of throwing and error if file already exists.(Used with create parser only)')

    create_parser.add_argument('-ny', '--non_yaml', nargs='+', type=Path, default=[],
                               help='Will add non-yaml files to seed directories when creating directory structure. (Used with create parser only)')

    # RUN options
    run_parser = subparsers.add_parser(
        'run', parents=[parent_parser], help='Run a simulation pipeline defined in args yaml file in a singular seed directory. Requires the --args_file option defined.')

    if opts.command == 'run':
        if opts.args_file is None:
            parser.error("'run' requires the '--args_file' option.")

    # LAUNCH options
    launch_parser = subparsers.add_parser(
        'launch', parents=[parent_parser], help='Launch or create launching script to run simulations in seed directories.')

    # parser.add_argument('-PSC', '--particleswarmcreate', metavar='PARAM_FILE',
    #                     nargs='+', type=str, default=[],
    #                     help='Particle Swarm Optimization Creation. Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random population members (default=10).')

    # parser.add_argument('-GAC', '--geneticalgorithmcreate', metavar='PARAM_FILE',
    #                     nargs='+', type=str, default=[],
    #                     help='Genetic Algorithm Optimization Creation. Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random population members (default=10).')

    opts = parser.parse_args()

    if not opts.workdir:
        opts.workdir = Path.cwd()
    elif not opts.workdir.exists():
        parser.error("Work directory '{opts.workdir}' does not exists.")

    if opts.args_file:
        assert opts.args_file.exists(
        ), f"Args file {opts.args_file} does not exist."

        with opts.args_file.open('r') as f:
            opts.args_dict = clib.load_yaml_in_order(f)

        if not opts.states:
            opts.states = list(opts.args_dict.keys())

    return opts

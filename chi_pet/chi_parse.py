#!/usr/bin/env python

import argparse

"""@package docstring
File: chi_parser.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from pathlib import Path

# TODO NEXT add parser test


def chi_parse():
    parser = argparse.ArgumentParser(prog='chi_pet.py')

    parser.add_argument('-n', type=int, default=10,
                        help='Number of different parameter sets used.')
    parser.add_argument('-a', '--args_file', type=str,
                        help='Name file that holds the program argument list.  (Used with --create option and --launch option)')
    parser.add_argument('-d', '--workdir', type=str,
                        help='Name of the working directory where simulation will be run. Used with --run option only)')
    parser.add_argument('-s', '--states', nargs='+', type=str,
                        help='Name of all the states the simulation will run eg. start, build, analyze, etc.')

    # TODO add prep functionality
    parser.add_argument('-P', '--prep', action='store_true',
                        help='Prepares simulationss to run with either states specified with -s or all argument states in --args_file.')

    # TODO add remove functionality
    parser.add_argument('-rm', '--remove', nargs='+', metavar='FILE', type=str,
                        help='Removes FILEs from seed directories.')

    subparsers = parser.add_subparsers(dest='command')

    # CREATE options
    create_parser = subparsers.add_parser(
        'create', help='Create a simulation directory structure using various strategies.')

    create_parser.add_argument('files',
                               metavar='PARAM_FILE(S)', nargs='+', type=str, default=[],
                               help='List of yaml files to be combined into a single yaml file and varied using Chi-Pet.')

    # create_parser.add_argument('-A', '--algorithm', type=str, default='scan',
    #                            help='Algorithm used to vary parameters. Options are "scan", "match", "particle_swarm", "genetic_algorithm".')

    create_parser.add_argument('-r', '--replace', default=False, action='store_true',
                               help='Replace simulation file instead of throwing and error if file already exists.(Used with create parser only)')

    create_parser.add_argument('-ny', '--non_yaml', nargs='+', default=[], type=str,
                               help='Will add non-yaml files to seed directories when creating directory structure. (Used with create parser only)')

    run_parser = subparsers.add_parser(
        'run', help='Run a simulation pipeline defined in args yaml file in a singular seed directory. Requires the --args_file option defined.')

    launch_parser = subparsers.add_parser(
        'launch', help='Launch or create launching script to run simulations in seed directories.')

    # parser.add_argument('-L', '--launch', nargs='*', default='NOLAUNCH', type=str, metavar='DIRS',
    #                     help='Launches all the seed directories in DIRS list. If no list is\
    #                 given all sim directories in the "simulations" directory will be launched.')

    # parser.add_argument('-PSC', '--particleswarmcreate', metavar='PARAM_FILE',
    #                     nargs='+', type=str, default=[],
    #                     help='Particle Swarm Optimization Creation. Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random population members (default=10).')

    # parser.add_argument('-GAC', '--geneticalgorithmcreate', metavar='PARAM_FILE',
    #                     nargs='+', type=str, default=[],
    #                     help='Genetic Algorithm Optimization Creation. Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random population members (default=10).')

    # RUN options only
    parser.add_argument('-R', '--run', action="store_true",
                        help='Runs a singular seed directory. Need --args_file.')

    opts = parser.parse_args()

    if opts.command == 'run' and opts.args_file is None:
        parser.error("'run' requires the '--args_file' option.")

    # If growing a chi tree, turn param file path strings into a pathlib list
    if opts.command == 'create':
        opts.param_file_paths = [opts.files]

    return opts

#!/usr/bin/env python

import argparse

"""@package docstring
File: chi_parser.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""


def chi_parser():
    parser = argparse.ArgumentParser(prog='chi_pet.py')

    parser.add_argument('-n', type=int, default=10,
                        help='Number of different parameter sets used.')
    parser.add_argument('-a', '--args_file', type=str,
                        help='Name file that holds the program argument list.  (Used with --create option and --launch option)')
    parser.add_argument('-d', '--workdir', type=str,
                        help='Name of the working directory where simulation will be run. Used with --run option only)')
    parser.add_argument('-s', '--states', nargs='+', type=str,
                        help='Name of all the states the simulation will run eg. start, build, analyze, etc.')

    # PREP options
    parser.add_argument('-P', '--prep', action='store_true',
                        help='Prepares sims to run with either states specified with -s or all argument states in -a ARG_FILES')

    # REMOVE options
    parser.add_argument('-rm', '--remove', nargs='+', metavar='FILE', type=str,
                        help='Removes FILEs from seed directories.')

    # LAUNCH options only
    parser.add_argument('-L', '--launch', nargs='*', default='NOLAUNCH', type=str, metavar='DIRS',
                        help='Launches all the seed directories in DIRS list. If no list is\
                    given all sim directories in the "simulations" directory will be launched.')

    # CREATE options only
    parser.add_argument('-C', '--create', metavar='PARAM_FILE',
                        nargs='+', type=str,
                        help='Creates seed directories with simulation structure that can be launched with ChiLaunch.py.')
    parser.add_argument('-r', '--replace', default=False, action='store_true',
                        help='Replace simulation file instead of throwing and error if file already exists.(Used with --create option only)')
    parser.add_argument('-ny', '--non_yaml', nargs='+', default=[], type=str,
                        help='Will add non-yaml files to seed directories when creating directory structure. (Used with --create or --shotgun option only)')

    parser.add_argument('-S', '--shotgun', metavar='PARAM_FILE',
                        nargs='+', type=str,
                        help='Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random variants (default=10).')

    parser.add_argument('-PSC', '--particleswarmcreate', metavar='PARAM_FILE',
                        nargs='+', type=str,
                        help='Particle Swarm Optimization Creation. Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random population members (default=10).')

    parser.add_argument('-GAC', '--geneticalgorithmcreate', metavar='PARAM_FILE',
                        nargs='+', type=str,
                        help='Genetic Algorithm Optimization Creation. Creates seed directories with simulation structure that can be launched with ChiLaunch.py. PARAM_FILEs are copied into seed directories with ChiParams chosen according to the random distribution specified. Need -n to specify the number of random population members (default=10).')

    # RUN options only
    parser.add_argument('-R', '--run', action="store_true",
                        help='Runs a singular seed directory. Need --args_file.')

    opts = parser.parse_args()
    return opts

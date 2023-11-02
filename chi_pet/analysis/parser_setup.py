#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact alamson@flatironinstitute.org
# Basic
import sys
import os
import argparse
# Testing


"""@package docstring
File: parser_setup.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Setup up most of the arguments for args_parsers used in analysis 
code.
"""


def parser_setup(parser):
    """!Initiate parser object with standard arguments used in analysis code.

    @param parser: argsparse.ArgumentParser object with known program
    @return: p

    """
    # General options
    parser.add_argument('-sd', '--seed', action='store_true',
                        help='Run analysis on a single seed.')
    parser.add_argument('--sim', action='store_true',
                        help='Run analysis on a single sim.')
    parser.add_argument('--datadir', type=str,
                        help='Name of the data directory in which all analyzed data\
                  files will be read/written. Also the directory where all the\
                  graphs will be placed when saved. Default is set to \
                  {workdir}/data/.')
    parser.add_argument('-d', '--workdir', type=str,
                        help='Name of the working directory where simulation will be run.')
    parser.add_argument('-p', '--params', nargs='+', type=str,
                        help='List of param names that will be used in graphing.')
    parser.add_argument('-t', '--title', type=str,
                        help='Suptitle for plots if graphing is activated.')
    parser.add_argument('-s', '--save', action='store_true',
                        help='Save figures if they were made during this run.')
    parser.add_argument("-ow", "--overwrite", action='store_true',
                        help="If a state exists in a seed, reanalyze it regardless, \
                  of previous state.")

    # Different main actions taken by analysis program
    parser.add_argument('-A', '--analyze', action='store_true',
                        help='Force analysis of data for seed, sim, or run')

    # Visual actions
    parser.add_argument('-G', '--graph', action='store_true',
                        help='Graph data after analysis has been done.')
    parser.add_argument('-M', '--movie', nargs='?', type=str, default=None,
                        const='basic',
                        help=('flag that tells analysis to make a movie '
                              'of a seed (and submovies of blurred images).'))
    parser.add_argument('-W', '--write', action='store_true',
                        help='Make analyzed data files from raw data files.')
    parser.add_argument('-R', '--read', action='store_true',
                        help='Read in all analyzed data files in "simulations" directory.')

    # Special functions for graphing and visuals
    parser.add_argument('-tg', '--test_graph', type=str,
                        help="Test the graphing function defined in argument.")
    parser.add_argument('--skip', action='store_true',
                        help="Skip making new frames with movie option")
    parser.add_argument('--rmtree', action='store_true',
                        help="Delete frame directory after making movies.")
    parser.add_argument('--xlog', action='store_true',
                        help='Criteria graph option that produces graphs with \
                  a logarithmic x-axis.')
    parser.add_argument('--ylog', action='store_true',
                        help='Criteria graph option that produces graphs with a\
                    logarithmic y-axis. (not implemented yet)')

    # Testing functions
    parser.add_argument("--test", action='store_true',
                        help="Run test protocol on analysis.")


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

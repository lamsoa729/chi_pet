#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact alamson@flatironinstitute.org
# Basic
import sys
import os
import pdb
# Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import itertools
from math import *
import functools

'''
Name: graph_lib.py
Description: Library of commonly used helper functions for graphing
'''


def param_scan(_func=None, uc=None, md=None):
    def param_scan_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            run = args[0]
            ax = args[1]
            param = args[2] if 'param' not in kwargs else kwargs['param']
            xlog = False if 'xlog' not in kwargs else kwargs['xlog']
            if uc is None:
                kwargs['param_arr'] = run.run_df[param]
            else:
                kwargs['param_arr'] = run.run_df[param] * uc[param][1]
            func(*args, **kwargs)
            if md is not None:  # Modify the xlabel
                md(ax, param)
            if xlog:
                if np.amin(kwargs['param_arr']) == 0:
                    # FIXME make this a log break
                    raise ValueError(" Zero used in log-scaled graph."
                                     " Fix this or fix the code to break up graph.")
                else:
                    ax.set_xscale("log", nonposx='clip')
        return wrapper

    if _func is None:
        return param_scan_decorator
    else:
        return param_scan_decorator(_func)


def make_color_bar(ax, label=r'Number of Seeds',
                   cmap=mpl.cm.rainbow, v_min=0, v_max=1):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='5%', pad=0.1)
    cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
                                   norm=mpl.colors.Normalize(vmin=v_min, vmax=v_max))
    cb.set_label(label)


def legend_outside(ax, loc='center left', anchor=(1.0, .5), set_ax_pos=True):
    # mpl.rcParams.update({'figure.autolayout':True})
    if set_ax_pos:
        ax.set_position([0.1, 0.1, 0.7, 0.8])
    ax.legend(loc=loc, bbox_to_anchor=anchor)


def sci_notation_latex(num_str, sig_figs=4, d_range=0, **kwargs):
    """!Take a string that is in exponential notation e.g.,
    2.45E-6 and converts it to $2.45\times10^{-6}$.

    @param num_str: string of a number in exponential form
    @param sig_figs: The number of significant figures
    @param d_range: The exponent range before applying scientific notation.
    @param **kwargs: TODO
    @return: latex string

    """
    # num_str = str(num_str)
    sig_figs = int(sig_figs)
    s = '{0:0.{1:d}e}'.format(num_str, sig_figs)
    m, e = s.split('e')
    e = int(e)
    if abs(e) <= d_range:
        m = float(m) * pow(10, e)
        return r'{0:0.{1}g}'.format(m, sig_figs)
    else:
        return r'${0:s}\times 10^{{{1:d}}}$'.format(m, e)


def graph_options(ax, config):
    '''!A quick functions that sets frequently changing graph options using a
    yaml file or dictionary.

    @param ax: Matplotlib axis object
    @param config: Either a path to a yaml file or a dictionary with the listed options
    @return: The dictionary given or the dictionary created by the yaml file
    '''
    g_opt = {}
    if isinstance(config, str):
        with open(config) as f:
            g_opt = yaml.load(f)

    elif isinstance(config, dict):
        g_opt = config

    for key, value in list(g_opt.items()):
        if key == "SupTitle":
            ax.suptitle(value)
        if key == "Title":
            ax.set_title(value)
        if key == "x_label":
            ax.set_xlabel(value)
        if key == "y_label":
            ax.set_ylabel(value)
        if key == "ymin":
            ax.set_ylim(bottom=value)
        if key == "ymax":
            ax.set_ylim(top=value)
        if key == "xmin":
            ax.set_xlim(left=value)
        if key == "xmax":
            ax.set_xlim(right=value)

    return g_opt


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

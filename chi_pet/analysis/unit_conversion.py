#!/usr/bin/env python
# Basic
import sys
import os
import pdb
import re
import yaml
# Analysis
# import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
from math import *
from copy import deepcopy

'''
Name: Unit_converions.py
Description: Program to convert simulation units to dimensional units
Input: Takes in dictionary of parameters to be converted
Output: Yaml file with converted units, (TODO tex table with units)
'''

# TODO Make function to calculate diffusion coefficient from viscocity or get time from diffusion coefficient
# TODO Have a function that takes in parameter files that are used to generate simulations and have it output converted data
# TODO Make it possible for values to take in ranges that can be converted

#######################################################################
#                      Latex generation strings                       #
#######################################################################

tex_table_hdr = (
    # """\\begin {table}[t!]
    # \centering
    #   \\begin{tabular}{llllp{3.5cm}}
    #   \\textbf{Parameter} & \\textbf{Symbol} & \\textbf{Value} &
    #                           \\textbf{Sim Value} & \\textbf{Notes} \\\\
    # """
    """\\begin {table}[t!] 
\centering 
  \\begin{tabular}{lllp{3.5cm}}
  \\textbf{Parameter} & \\textbf{Symbol} & \\textbf{Value} & \\textbf{Notes}\\\\ 
"""
)
tex_table_float_entry = (
    # """  {} & {} & {:.4f}{} & {:.4f} & {} \\\\
    # """
    """  {} & {} & {:.4f}{} & {} \\\\
"""
)
tex_table_int_entry = (
    # """  {} & {} & {:d}{} & {:d} & {} \\\\
    # """
    """  {} & {} & {:d}{} & {} \\\\
"""
)
tex_table_ftr = (
    """  \\end{tabular} 
  \\caption{Unit conversion table.}
\\label{tab:units}
\\end{table}
""")

#######################################################################
#                  UnitDictionary generation strings                  #
#######################################################################

unit_dict_hdr = (
    """#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact alamson@flatironinstitute.org
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../Lib'))
from UnitConversionDict import UnitConversionDict
\"\"\"
@package docstring
File: {}
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Unit dictionary object to convert simulation units to real units
\"\"\"

unit_dict = {{
""")

unit_dict_entry = (
    """  '{}' : ('{}', {}, {}, '{}'), # {}
""")

unit_dict_ftr = (
    """  }

uc = UnitConversionDict(unit_dict)
""")

modxlabel_hdr = (
    """
def ModifyXLabel(ax, p):
"""
)

modxlabel_entry = (
    """    {} p == '{}':
        ax.set_xlabel('{} {} {}')
"""
)

modxlabel_ftr = (
    """    else:
        print "Parameter {} not set in spindle_run".format(p)
        ax.set_xlabel(p)
    return
"""
)


# %\footnotesize
#   \begin{tabular}{llllp{3.5cm}}
#     \textbf{Parameter} & \textbf{Symbol} & \textbf{Value} &
#                                                             \textbf{Range} &
#                                                                              \textbf{Notes} \\
#     Nuclear envelope radius  & R & 1.375 $\mu$m& -- & \cite{A-kalinina12} \\}"

# Code to format yaml file properly
class blockseq(list):
    pass


def blockseq_rep(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=False)


class flowseq(list):
    pass


def flowseq_rep(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)


class blockmap(dict):
    pass


def blockmap_rep(dumper, data):
    return dumper.represent_mapping('tag:yaml.org,2002:map', data, flow_style=False)


class flowmap(dict):
    pass


def flowmap_rep(dumper, data):
    return dumper.represent_mapping('tag:yaml.org,2002:map', data, flow_style=True)


def convdump(yaml_dict):
    if 'Conversions' in yaml_dict:
        yaml_dict['Conversions'] = blockmap(yaml_dict['Conversions'])
    if 'Params' in list(yaml_dict.keys()):
        yaml_dict['Params'] = blockseq(yaml_dict['Params'])
        for p in yaml_dict['Params']:
            k, prop = list(p.items())[0]
            if prop['units'] == "None":
                p[k] = blockmap(p[k])
                continue
            else:
                prop['units'] = flowseq(prop['units'])
                prop['dim'] = flowseq(prop['dim'])

    return yaml.dump(yaml_dict)


class UnitConversion(object):

    def __init__(self, yaml_file):
        with open(yaml_file) as f:
            yaml_dict = yaml.load(f)
        self._conv_dict = yaml_dict['Conversions']
        # Create both simulation and dimensional dictionaries
        self._to_dim = 1 if (yaml_dict['Type'] == 'sim') else 0
        if self._to_dim:
            self._sim_params = yaml_dict['Params']
            self._dim_params = self.ConvertUnits(self._sim_params)
        else:
            self._dim_params = yaml_dict['Params']
            self._sim_params = self.ConvertUnits(self._dim_params)

    def ConvertUnits(self, orig_params):
        conv_params = deepcopy(orig_params)
        for p in conv_params:
            k, prop = list(p.items())[0]
            if prop['units'] == "None":
                continue
            else:
                dim = prop['dim']
                units = prop['units']
                if len(units) != len(dim):
                    raise Exception(
                        'Number of units and dimensions do not match in param %s' % k)
                elif (self._to_dim):  # sim -> dim
                    for u, d in zip(units, dim):
                        prop['value'] *= (pow(float(self._conv_dict[u]), d))
                else:  # dim->sim
                    for u, d in zip(units, dim):
                        prop['value'] /= (pow(float(self._conv_dict[u]), d))
        return conv_params

    def write_yaml_file(self, name=""):
        """Write converted yaml file to current directory.
        """
        conv_yaml = {}
        if self._to_dim:
            conv_yaml["Params"] = self._dim_params
            conv_yaml["Type"] = "dim"
        else:
            conv_yaml["Params"] = self._sim_params
            conv_yaml["Type"] = "sim"
        conv_yaml["Conversions"] = self._conv_dict
        if name == "":
            name = conv_yaml["Type"] + "_units.yaml"
        else:
            name += "_" + conv_yaml["Type"] + "_units.yaml"

        with open(name, 'w') as outfile:
            outfile.write(convdump(conv_yaml))

# Write function to use conv_yaml to make latex tables
    def write_latex_table(self, f_name=""):
        """Make a tex file that contains a table of all the conversion and 
           parameters has everything filled out according to the yaml file.
        """
        tex_table = tex_table_hdr

        for dp, sp in zip(self._dim_params, self._sim_params):
            dim_units = " $"
            name, d_entry_dict = list(dp.items())[0]
            name, s_entry_dict = list(sp.items())[0]
            for d, u in zip(d_entry_dict['dim'], d_entry_dict['units']):
                dim_units += "$ $\\rm {}".format(
                    u) if d == 1 else "$ $\\rm {}^{{{}}}".format(u, int(d))
            dim_units += "$"

            if d_entry_dict['type'] == 'float':
                tex_table += tex_table_float_entry.format(name,
                                                          d_entry_dict['symbol'],
                                                          d_entry_dict['value'],
                                                          dim_units,
                                                          # s_entry_dict['value'],
                                                          d_entry_dict['notes'],
                                                          )
            elif d_entry_dict['type'] == 'int':
                tex_table += tex_table_int_entry.format(name,
                                                        d_entry_dict['symbol'],
                                                        int(d_entry_dict['value']),
                                                        dim_units,
                                                        # int(s_entry_dict['value']),
                                                        d_entry_dict['notes'],
                                                        )
        tex_table += tex_table_ftr
        if f_name == "":
            f_name = "units_tab.tex"
        else:
            f_name += "_units_tab.tex"
        with open(f_name, 'w') as outfile:
            outfile.write(tex_table)
        # print tex_table
        pass

        # print tex_table_hdr.format("Hello")
        # print tex_table_hdr

    def WriteUnitConversionDict(self, f_name=""):
        """ Write UnitConversionDict to the current directory

        @param f_name: prefix to file name 
        @return: void, writes a UnitConversionDict.py file

        """
        if f_name == "":
            f_name = "unit_dict.py"
        else:
            f_name += "_unit_dict.py"
        unit_dict_py = unit_dict_hdr.format(f_name)
        modxlabel = modxlabel_hdr
        if_str = 'if'
        # First writed out all the conversions
        for k, v in list(self._conv_dict.items()):
            unit_dict_py += unit_dict_entry.format(k,
                                                   "$\\\\rm {}$".format(k),
                                                   v,
                                                   'float',
                                                   "",
                                                   "",
                                                   )
        # Make conversion dictionary
        for p in self._sim_params:
            dim_units = ""
            dim_conv = 1.0
            name, entry_dict = list(p.items())[0]
            # Get conversions to dimensionful units if param has dimentsions
            if entry_dict['dim']:
                # Loop over units and apply power
                for d, u in zip(entry_dict['dim'], entry_dict['units']):
                    dim_units += "$\\\\rm {}$ ".format(
                        u) if d == 1 else "$\\\\rm {}^{{{}}}$ ".format(u, int(d))
                    dim_conv *= np.power(self._conv_dict[u], d)
                dim_units = dim_units[:-1]  # Get rid of trailing space
            # Add entry to unit dictionary
            unit_dict_py += unit_dict_entry.format(entry_dict['shortcut'],
                                                   dim_units,
                                                   dim_conv,
                                                   entry_dict['type'],
                                                   entry_dict['symbol'],
                                                   name,
                                                   )
            # Add parenthesis around dimensions if they exist
            if entry_dict['dim']:
                dim_units = "({})".format(dim_units)
            # Add modify label entry to modxlabel function
            modxlabel += modxlabel_entry.format(if_str,
                                                entry_dict['shortcut'],
                                                name,
                                                entry_dict['symbol'],
                                                dim_units,
                                                )
            # Change if_str after one call
            if if_str == 'if':
                if_str = 'elif'
        # Put all pieces of UnitConversionDict together
        unit_dict_py += unit_dict_ftr + modxlabel + modxlabel_ftr
        # Write out file
        with open(f_name, 'w') as outfile:
            outfile.write(unit_dict_py)
        return

    def PrintConvUnits(self):
        print(self._conv_dict)

    # def PrintConvParams(self):
        # print self.conv_params


##########################################
if __name__ == "__main__":

    yaml.add_representer(blockseq, blockseq_rep)
    yaml.add_representer(blockmap, blockmap_rep)
    yaml.add_representer(flowmap, flowmap_rep)
    yaml.add_representer(flowseq, flowseq_rep)

    a = UnitConversion(sys.argv[1])
    if len(sys.argv) == 2:
        name = ""
    elif len(sys.argv) == 3:
        name = sys.argv[2]
    else:
        print(("In proper usage of unit_conversion.py. Takes 2 arguments ",
               "arg1: file to be converted, ",
               "arg2: prefix of file names(OPTIONAL)"))
        exit(1)

    a.WriteYamlFile(name)
    a.WriteLatexTable(name)
    a.WriteUnitConversionDict(name)

    # with open(sys.argv[2], 'w') as outfile:
    # outfile.write( convdump(a.conv_yaml))

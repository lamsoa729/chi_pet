#!/usr/bin/env python


"""@package docstring
File: chi_param
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""


class ChiParam(object):

    """!Class that holds all the values of a changing parameter."""

    def __init__(self, name, format_str='{}',
                 exec_str=None, vals=None, level=0):
        """!TODO: to be defined1.

        @param name: TODO
        @param vals: TODO

        """
        self._name = name
        self._format_str = format_str
        self._exec_str = exec_str
        self._vals = vals
        self._level = level


class ChiParamVal(object):

    """!Singular value of parameters that are being varied"""

    def __init__(self, name, val):
        """!Initializes ChiParamVal with the name of the parameter and a value

        @param name: TODO
        @param val: TODO

        """
        self._name = name
        self._val = val


class ChiParamVariations(object):

    """!Docstring for ChiParamVariations. """

    def __init__(self, chi_param_list=None):
        """!Initialize a list of varied parameters to make chi_nodes

        @param chi_param_list: TODO

        """
        self._chi_param_list = chi_param_list


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

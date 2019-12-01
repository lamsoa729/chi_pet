#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
"""@package docstring
File: chi_root_node.py
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""

from operator import attrgetter

from .chi_node import ChiNode
from chi_pet import chi_lib as clib
from pathlib import Path


class ChiRootNode(ChiNode):

    """!Create the root node of the chi tree structure"""

    def __init__(self, path, opts=None):
        """!TODO: to be defined1. """
        ChiNode.__init__(self, path, None, None, level=0, opts=opts)

    def Grow(self, yaml_lst):
        """!Template pattern for creating ChiNode tree

        @param yaml_lst: TODO
        @return: TODO

        """
        # Create yaml file dictionary
        self.makeYamlDict(yaml_lst)
        chi_param_refs = self.makeChiParamRefs()
        max_level = self.makeChiParam
        self.MakeSubnodes(max_level)

        # Get a list of object references to all entries in dictionary with key
        # and value ChiParam(string) and put into a list

    def makeYamlDict(self, file_list):
        # Take input yaml files and create master dictionary from them
        for fname in file_list:
            if Path.isfile(fname):
                self.yaml_files_dict[fname] = clib.CreateDictFromYamlFile(
                    fname)

    def makeChiParams(self):
        """!TODO: Docstring for makeChiParamRef.
        @return: TODO

        """
        # Get object references to all ChiParam instances
        chi_param_refs = list(clib.find_str_values(self.yaml_files_dict))
        # Create list of ChiParams
        self._chi_params = [eval(cpr.GetValue()) for cpr in chi_param_refs]
        # Set reference to location in yaml_file_dict of ChiParams
        for cp_i, ref in zip(self._chi_params, chi_param_refs):
            cp_i.SetObjRef(ref)

        # Get the max level of the chi parameters
        max_level = max(self._chi_params, key=attrgetter('_level'))._level


##########################################
if __name__ == "__main__":
    cparams = [ChiParam('s', level=1, vals=[0, 1, 2, 3])]

#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import os
# import yaml
from shutil import rmtree
from pathlib import Path
from .chi_param import ChiParam
# import line_profiler
# Speed
# from numba import jit


"""@package docstring
File: chi_node.py
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""


class ChiNode(object):
    def __init__(self, path, chi_params, yaml_file_dict,
                 opts=None, params=None, level=0):
        # Make sure paths are accurate
        if isinstance(path, Path):
            self._path = path
        elif isinstance(path, str):
            self._path = Path(path)
        else:
            raise TypeError(
                " Path {} was not pathlib object nor string".format(path))

        self._chi_params = chi_params
        self._yaml_file_dict = yaml_file_dict
        self._params = params
        self._level = level

    def MakeSubnodes(self, max_level, subnode_dir="subnodes"):
        snode_dir = self._path / subnode_dir
        self.CreateDir(snode_dir)
        # Find chi_params that are on the same level as node
        chi_params_level = [cp_i if cp_i._level == self._level for cp_i in self._chi_params]
        # pop chi_params out of chi_param lists
        self.MakeChiParamVals()
        for cp_i in chi_params_level:
            # Get all combinations of chi_param values
            chi_param_values = cp_i.makeValues()
            # Update yaml_dictionary with this values

        # Create subnodes with updated lists

        # for cp in self._chi_params:
        #     # TODO tracer round coding
        #     snode_path = snode_dir / "{}_{}".format(cp._name, self._
        #     cnode = ChiNode(snode_path, cp, self._yaml_file_dict, cp._name, cp._format_str
        #                     self._level + 1)
        #     cnode.MakeNodeDirectory(max_level)

    def MakeNodeDirectory(self, max_level=0, overwrite=False):
        node_created = self.CreateDir(self._path, overwrite)
        if node_created:
            self.MakeDataDirectory()
            self.MakeYamlFiles()
            return
        if self._level >= max_level:
            return
        else:
            self.MakeSubnodes(max_level)

    def MakeYamlFiles(self):
        pass

    def MakeDataDirectory(self):
        self._data_dir = self._path / "data"
        self.CreateDir(self._data_dir, overwrite=True)

    def DumpData(self):
        pass

    @classmethod
    def CreateDir(self, path, overwrite=False):
        """!Create directory. If it exists it will be either overwritten or left
        alone depending on the overwrite flag

        @param path: pathlib Path to create
        @return: Bool of whether a new directory was created or not

        """
        if path.exists():
            if not overwrite:
                print("{} exists and is being left alone.".format(path))
                return False
            else:
                print("Removing {}".format(path))
                rmtree(path)
        else:
            path.mkdir()
            return True


##########################################
if __name__ == "__main__":
    # cparams = [ChiParam("s" + str(i)) for i in range(10)]
    yml_dict = {}
    cnode = ChiNode(Path(os.getcwd()), cparams, yml_dict)
    cnode.MakeNodeDirectory()

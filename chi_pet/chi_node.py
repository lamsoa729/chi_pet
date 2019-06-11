#!/usr/bin/env python
# In case of poor (Sh***y) commenting contact adam.lamson@colorado.edu
# Basic
import sys
import os
import yaml
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
    def __init__(self, path, chiparams, yml_file_dict, params=None, level=0):
        if isinstance(path, Path):
            self._path = path
        elif isinstance(path, str):
            self._path = Path(path)
        else:
            raise TypeError(
                " Path {} was neither pathlib object nor string".format(path))

        self._chiparams = chiparams
        self._yml_file_dict = yml_file_dict
        self._params = params
        self._level = level

    def MakeSubnodes(self, subnode_dir="subnodes"):
        snode_dir = self._path / subnode_dir
        self.CreateDir(snode_dir)

        for cp in self._chiparams:
            # TODO tracer round coding
            snode_path = snode_dir / cp._name
            cnode = ChiNode(snode_path, cp, self._yml_file_dict, cp._name,
                            self._level - 1)
            cnode.MakeNodeDirectory()

    def MakeYamlFiles(self):
        pass

    def MakeNodeDirectory(self, overwrite=False):
        node_created = self.CreateDir(self._path, overwrite)
        self.MakeDataDirectory()
        self.MakeYamlFiles()
        if self._level < 0:
            return
        else:
            self.MakeSubnodes()

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


##########################################
if __name__ == "__main__":
    cparams = [ChiParam("s" + str(i)) for i in range(10)]
    yml_dict = {}
    cnode = ChiNode(Path(os.getcwd()), cparams, yml_dict)
    cnode.MakeNodeDirectory()

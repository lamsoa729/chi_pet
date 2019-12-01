#!/usr/bin/env python
"""@package docstring
File: chi_node.py
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""
from shutil import rmtree
from pathlib import Path
import yaml
from .chi_param import ChiParam


class ChiNode():

    """!Node in the directory tree of parameter variations"""

    def __init__(self, path, chi_params, yaml_dict,
                 opts=None, params=None, level=0):
        """!Initialize ChiNode with path location, parameter objects to change,
        and template parameter yaml dictionary.

        @param path: TODO
        @param chi_params: TODO
        @param yaml_dict: TODO
        @param opts: TODO
        @param params: TODO
        @param level: TODO

        """
        if isinstance(path, Path):
            self._path = path
        elif isinstance(path, str):
            self._path = Path(path)
        else:
            raise TypeError(
                " Path {} was not pathlib object nor string".format(path))

        self._chi_params = chi_params
        self._yaml_dict = yaml_dict
        self._opts = opts
        self._params = params
        self._level = level

        self._data_dir = None
        self._snode_dir = None

    def make_node_dir(self, overwrite=False):
        node_created = self.create_dir(self._path, overwrite)
        if node_created:
            self.make_yaml_files(self._path)
            self.make_data_dir(self._path)
        if self._level > 0:
            self.make_subnodes(self._level - 1)
        else:
            return

    def make_yaml_files(self, path):
        """!Create parameter files to use
        @return: TODO

        """
        for yfname, yfdict in self._yaml_dict.items():
            with open(path / yfname, 'w') as yfile:
                yaml.dump(yfdict, yfile)

    def make_data_dir(self, path):
        """!Create data directory.
        @return: void

        """
        self._data_dir = path / "data"
        self.create_dir(self._data_dir, overwrite=True)

    def make_subnodes(self, sub_level, subnode_dir='subnodes'):
        """!Create subnode in directory tree structure

        @param max_level: TODO
        @param subnode_dir: TODO
        @return: TODO

        """
        if not self._path.exists():
            raise RuntimeError(
                'Node directory {} does not exist.'.format(self._path))

        self._snode_dir = self._path / subnode_dir
        self.create_dir(self._snode_dir)
    #     # Find chi_params that are on the same level as node
    #     chi_params_level = [
    #         cp_i for cp_i in self._chi_params if cp_i._level == self._level]
    #     # pop chi_params out of chi_param lists
    #     # self.MakeChiParamVals()
    #     for cp_i in chi_params_level:
    #         # Get all combinations of chi_param values
    #         chi_param_values = cp_i.makeValues()
    #         # Update yaml_dictionary with this values

        # Create subnodes with updated lists

        # for cp in self._chi_params:
        #     # TODO tracer round coding
        #     snode_path = snode_dir / "{}_{}".format(cp._name, self._
        #     cnode = ChiNode(snode_path, cp, self._yaml_file_dict, cp._name, cp._format_str
        #                     self._level + 1)
        #     cnode.MakeNodeDirectory(max_level)

    def DumpData(self):
        pass

    @classmethod
    def create_dir(cls, path, overwrite=False):
        """!Create directory. If it exists it will be either overwritten or left
        alone depending on the overwrite flag

        @param path: pathlib Path to create
        @return: Bool of whether a new directory was created or not

        """
        if path.exists():
            if overwrite:
                print("Removing {}".format(path))
                rmtree(path)
            else:
                print("{} exists and is being left alone.".format(path))
                return False
        path.mkdir()
        return True


##########################################
if __name__ == "__main__":
    cparams = [ChiParam("s" + str(i)) for i in range(10)]
    yml_dict = {}
    cnode = ChiNode(Path.cwd(), cparams, yml_dict)
    cnode.MakeNodeDirectory()

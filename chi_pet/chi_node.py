#!/usr/bin/env python
"""@package docstring
File: chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""
from shutil import rmtree
from pathlib import Path
import yaml
from .chi_param import ChiParam
from .chi_dict import ChiDict


class ChiNode():

    """!Node in the directory tree of parameter variations"""

    def __init__(self, node_path: Path,
                 chi_dict: ChiDict = None,  # TODO: remove,
                 opts=None,
                 params=None) -> None:
        """!Initialize ChiNode with path location, parameter objects to change,
        and template parameter yaml dictionary.

        @param path: TODO
        @param yaml_dict: TODO
        @param opts: TODO
        @param params: TODO
        @param level: TODO

        """
        if isinstance(node_path, Path):
            self._node_path = node_path
        elif isinstance(node_path, str):
            self._node_path = Path(node_path)
        else:
            raise TypeError(
                f" Path {node_path} was not pathlib object nor string")

        self._chi_dict = chi_dict
        self._opts = opts
        self._params = params

        self._chi_params = self._chi_dict.search_dict_for_chi_params()
        self._level = min(param._level for param in self._chi_params)

        self._data_dir = None
        self._snode_dir = None
        self._analysis_dir = None
        self._misc_dir = None

    def make_node_dir(self, node_path: Path, overwrite: bool = False) -> None:
        node_created = self.create_dir(node_path, overwrite)
        if not node_created:
            return

        self._chi_dict.write_out_yaml_files(node_path)
        # self.make_nonyaml_files(self._path)
        # self.make_analysis_dir(self._path)
        # self.make_misc_dir(self._path)
        if self._level > 0:
            self.make_subnodes(self._level - 1)
            return
        self.make_data_dir(node_path)

        self._chi_dict.write_out_yaml_files(node_path)

    def make_data_dir(self, path: Path, overwrite: bool = False) -> None:
        self._data_dir = path / "data"
        return self.create_dir(self._data_dir, overwrite)

    def make_subnodes(self, sub_level: int, overwrite: bool = False) -> None:
        if not self._node_path.exists():
            raise RuntimeError(
                f'Node directory {self._node_path} does not exist.')

        self._snode_dir = self._node_path / "subnodes"
        self.create_dir(self._snode_dir, overwrite)
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

    @classmethod
    def create_dir(cls, path: Path, overwrite: bool = False) -> bool:
        """Create directory. If it exists it will be either overwritten or left
        alone depending on the overwrite flag.

        Parameters
        ----------
        path : Path
            path to directory to create
        overwrite : bool, optional
            If path exists, should this be overwritten, by default False

        Returns
        -------
        bool
            Was directory created? If it existed and was not overwritten then
            the function will return false.
        """

        if path.exists():
            if not overwrite:
                print(f"{path} exists and is being left alone.")
                return False
            print(f"Removing {path}.")
            rmtree(path)
        path.mkdir()
        return True


##########################################
if __name__ == "__main__":
    # Testing code for things
    cparams = [ChiParam("s" + str(i)) for i in range(10)]
    print(cparams)
    yml_dict = {}
    cnode = ChiNode(Path.cwd(), cparams, yml_dict)
    cnode.make_node_dir()

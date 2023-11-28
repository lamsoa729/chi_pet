#!/usr/bin/env python
"""@package docstring
File: chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""
from shutil import rmtree
from pathlib import Path
from .chi_param import ChiParam
from .chi_dict import ChiDict
from .chi_lib import ind_recurse


"""! 

"""


class ChiNode():

    """!Node in the directory tree of parameter variations"""

    def __init__(self, node_path: Path,
                 chi_dict: ChiDict = None,
                 opts=None,
                 params=None,
                 level: int = 0) -> None:
        """Initialize ChiNode with path location or ChiDict to create a ChiNode-like directory.

        Parameters
        ----------
        node_path : Path
            Path to directory of ChiNode
        chi_dict : ChiDict, optional
            Combined dictionary of yaml/toml parameter files to create in directory, by default None
        opts : _type_, optional
            parser options, by default None
        params : _type_, optional
            _description_, by default None

        Raises
        ------
        TypeError
            _description_
        RuntimeError
            _description_
        """
        if isinstance(node_path, Path):
            self._node_path = node_path
        elif isinstance(node_path, str):
            self._node_path = Path(node_path)
        else:
            raise TypeError(
                f" Path {node_path} was not pathlib object nor string")

        self._opts = opts
        self._params = params

        if chi_dict:
            self._chi_dict = chi_dict
        else:
            if not self._opts.param_file_paths:
                raise RuntimeError(
                    "If a ChiDict is not supplied, a params_file_path list must be supplied instead.")
            self._chi_dict = ChiDict(
                file_path_list=self._opts.param_file_paths)

        self._chi_params = self._chi_dict.search_dict_for_chi_params()
        self._level = level if len(self._chi_params) == 0 else min(
            param._level for param in self._chi_params)

        # Directories in a ChiNode. If these are None, they will be created when the node is created.
        self._data_dir = None
        self._snode_store_dir = None
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
        # if len(self._chi_params):
        #     self.make_subnodes()
        self.make_data_dir(node_path)

        self._chi_dict.write_out_yaml_files(node_path)

    def make_data_dir(self, path: Path, overwrite: bool = False) -> None:
        self._data_dir = path / "data"
        return self.create_dir(self._data_dir, overwrite)

    def make_subnodes(self, overwrite: bool = False) -> None:
        assert self._opts.command == 'create', "Subnodes can only be created when creating a directory structure."

        if not self._node_path.exists():
            raise RuntimeError(
                f'Node directory {self._node_path} does not exist.')

        if len(self._chi_params) == 0:
            return

        self._snode_store_dir = self._node_path / "subnodes"
        subnode_dir_created = self.create_dir(self._snode_store_dir, overwrite)

        # Loop over lowest level of ChiParams and realize param values
        current_level_chi_params = [
            cp for cp in self._chi_params if cp._level == self._level]

        # If multiple chi-params have the same level carry out the combinatorics
        # (but only for scan options)
        if self._opts.algorithm == "scan":
            lst = [cp.get_number_of_values()
                   for cp in current_level_chi_params]
            index_combinations = ind_recurse(lst)

            # loop over indices, choosing the right chi-param value for each index
            for ind_list in index_combinations:
                for ind, cparam in zip(ind_list, current_level_chi_params):
                    cparam.set_value(ind)
                snode_dir_name = "_".join([cp.get_dir_str()
                                          for cp in current_level_chi_params])

                # Once chi-node parameters are set in chi-dict,
                # create a new chi-node and recurse
                new_node = ChiNode(self._snode_store_dir / snode_dir_name,
                                   self._chi_dict,
                                   self._opts, self._params,
                                   self._level + 1)
                new_node.make_node_dir(new_node._node_path, overwrite)
                new_node.make_subnodes(overwrite)

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
    cnode.make_node_dir()

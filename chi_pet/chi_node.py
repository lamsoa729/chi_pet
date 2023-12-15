#!/usr/bin/env python
"""@package docstring
File: chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""
from shutil import rmtree
from pathlib import Path
from copy import deepcopy
from .chi_param import ChiParam
from .chi_dict import ChiDict
from .chi_lib import ind_recurse


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
        # TODO initialize nonyaml files and test
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

        # TODO POSSIBLE make this it's own function
        # Make list of all 'matched' chi-params matched methods of varying parameters
        matched_params = [
            cp for cp in current_level_chi_params if cp._alg is 'match']

        # Separate matched parameters into resprective groups
        matched_grps = {}
        for mcp in matched_params:
            if not mcp._param_grp:
                # TODO Create test for this runtime error
                raise RuntimeError(
                    f"Matched param {mcp._name} does not have an associated group. Please set the 'param_grp' argument of this ChiParam object.")
            # If grp name does not exists, start list of parameters
            if not mcp._param_grp in matched_grps:
                matched_grps[mcp._param_grp] = [mcp]
                continue

            matched_grps[mcp._param_grp] += [mcp]

        # TODO make this it's own testable function
        val_number_lst = []
        # Get number of param variations for each group.
        for grp_name, grp_lst in matched_grps.items():
            num_vals = None
            for cp in grp_lst:
                if not num_vals:
                    num_vals = cp.get_number_of_values()
                    continue
                # make sure each chi-param in a group contains the same param variation number
                if num_vals != cp.get_number_of_values():
                    raise RuntimeError(
                        f"Not all params in matched param group {grp_name} has the same number of values. Check to make sure all values have or generate the same length parameter value lists.")
            val_number_lst += [num_vals]

        # Loop over all none matched parameters and add their parameter value list lengths to val_number_lst to carry out combinatorics.
        scanned_params = [
            cp for cp in current_level_chi_params if cp._alg == 'scan']
        for scp in scanned_params:
            val_number_lst += [scp.get_number_of_values()]

        # If multiple chi-params have the same level carry out the combinatorics
        index_combinations = ind_recurse(val_number_lst)

        # loop over indices, choosing the right chi-param value for each index
        num_grps = len(matched_grps.keys())
        for ind_list in index_combinations:

            # Set matched param values first
            for ind,  grp_lst in zip(ind_list[:num_grps],
                                     matched_grps.values()):
                for gcp in grp_lst:
                    gcp.set_value(ind)

            # Set scanned params values second
            for ind, scp in zip(ind_list[num_grps:], scanned_params):
                scp.set_value(ind)

            # Create directory name
            snode_dir_name = "_".join([cp.get_dir_str()
                                       for cp in current_level_chi_params])

            # Once chi-node parameters are set in chi-dict,
            # create a new chi-node and recurse
            new_node = ChiNode(self._snode_store_dir / snode_dir_name,
                               deepcopy(self._chi_dict),
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

#!/usr/bin/env python


"""@package docstring
File: chi_dict
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from typing import Optional, Dict, List
from pathlib import Path
from .chi_param import ChiParam
from .chi_lib import load_yaml_in_order, dump_yaml_in_order
import yaml


class ChiDict(object):

    """Compiled dictionary of all the parameters to run a simulation."""

    def __init__(self, param_dict: Optional[Dict] = None,
                 file_path_list: Optional[List[Path]] = None):
        self._param_dict = param_dict
        if self._param_dict is None:
            assert file_path_list is not None, "Must provide a dictionary or list of file paths."
            self._param_dict = self.make_param_dict(file_path_list)

    def make_param_dict(self, file_path_list):
        for file_path in file_path_list:
            with file_path.open('r') as f:
                self._param_dict[f.name] = load_yaml_in_order(f)

    def search_dict_for_chi_params(self):
        pass

    def write_out_yaml_files(self, node_path: Path):
        for file_name, file_dict in self._param_dict.items():
            with (node_path / file_name).open('w') as of:
                dump_yaml_in_order(file_dict, of, default_flow_style=False)


##########################################
if __name__ == "__main__":
    print("Not implemented yet")

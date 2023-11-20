#!/usr/bin/env python

"""@package docstring
File: test_chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from pathlib import Path
from shutil import rmtree
from mhelpers import (setup_and_teardown, mock_yaml_dict,
                      mock_root_dir, MOCK_CHI_PARAM_DICT_PATH)
from chi_pet.chi_dict import ChiDict
from test_chi_param import mock_chi_param
import pytest
import yaml


@pytest.fixture()
def mock_chi_dict(mock_yaml_dict):
    chi_dict = ChiDict(param_dict=mock_yaml_dict)
    return chi_dict


def test_make_param_dict(mock_root_dir, mock_yaml_dict):
    chi_root_dir = mock_root_dir
    yaml_file_list = list(chi_root_dir.glob('*.yaml'))
    chi_dict = ChiDict(file_path_list=yaml_file_list)
    assert chi_dict._param_dict == mock_yaml_dict


def test_search_dict_for_chi_params(mock_yaml_dict, mock_chi_param):
    chi_dict = ChiDict(param_dict=mock_yaml_dict)
    assert chi_dict._param_dict == mock_yaml_dict
    chi_param_list = chi_dict.search_dict_for_chi_params()
    assert len(chi_param_list) == 1
    assert str(chi_param_list[0]) == str(mock_chi_param)


def test_search_dict_for_chi_params_when_none_exist(mock_yaml_dict, mock_chi_param):
    chi_dict = ChiDict(param_dict={"param": "not a ChiParam"})
    chi_param_list = chi_dict.search_dict_for_chi_params()
    assert len(chi_param_list) == 0


def test_search_dict_for_chi_params_when_non_exist(mock_yaml_dict):
    # Remove the chi param string from the mock dictionary
    mock_yaml_dict[MOCK_CHI_PARAM_DICT_PATH] = 1
    chi_dict = ChiDict(param_dict=mock_yaml_dict)
    chi_param_list = chi_dict.search_dict_for_chi_params()
    assert len(chi_param_list) == 0


def test_write_out_yaml_files(mock_root_dir):
    chi_root_dir = mock_root_dir
    orig_yaml_list = list(chi_root_dir.glob('*.yaml'))
    chi_dict = ChiDict(file_path_list=orig_yaml_list)
    new_node = Path.cwd() / 'tests/mock_new_node'
    new_node.mkdir()

    chi_dict.write_out_yaml_files(new_node)
    new_yaml_list = list(new_node.glob('*.yaml'))
    for file_path in new_yaml_list:
        with file_path.open('r') as f:
            assert yaml.safe_load(f) == chi_dict._param_dict[file_path.name]

    assert len(new_yaml_list) == len(orig_yaml_list)

    orig_yaml_name_list = [file_path.name for file_path in orig_yaml_list]
    for file_path in new_yaml_list:
        # Check to see if any of the paths have the same name
        assert file_path.name in orig_yaml_name_list

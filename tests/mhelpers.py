#!/usr/bin/env python

"""@package docstring
File: mhelpers.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description: Mocking helpers for testing
"""

from pathlib import Path
from shutil import rmtree
import pytest
import yaml

MOCK_PARAM_DICT = {"param_1": 1,
                   "param_list": [1, 2, 3]}
MOCK_CHI_PARAM_STR = "ChiParam(name='pA', format_str='pA{:d}', values=[10,20,30])"
MOCK_PARAM_CHI_DICT = {"param_two": "two",
                       "param_str_list": ["one", "two", "three"],
                       "var_param": MOCK_CHI_PARAM_STR}

MOCK_NON_YAML_FILE_STR = "This is a tests."
MOCK_ARGS_FILE_DICT = {'stage1': ['arg1', 'arg2', 'arg3'],
                       'stage2': ['arg4', 'arg5', 'arg6']}

MOCK_SHELL_ARGS_FILE_DICT = {'touch1': ['touch', 'mock_output1.txt'],
                             'touch2': ['touch', 'mock_output2.txt'], }

MOCK_PARAM_DICT_PATH = 'mock_param.yaml'
MOCK_CHI_PARAM_DICT_PATH = 'mock_param_chi_param.yaml'


def clean_mocks():
    """Clean up mock directories and files before testing to make sure we are
    working from a clean slate.
    """
    for mpath in Path.cwd().glob('tests/mock*'):
        if mpath.is_file():
            mpath.unlink()
        elif mpath.is_dir():
            rmtree(mpath)


@pytest.fixture()
def clean_up(request):
    return not request.config.getoption("--no-cleanup")


@pytest.fixture(autouse=True)
def setup_and_teardown(clean_up):
    clean_mocks()  # Makes sure you start clean
    yield
    if clean_up:
        clean_mocks()  # Clean up after running tests


def mock_non_yaml_file(dir_path):
    ny_file_path = dir_path / 'mock_ny_file.txt'
    with ny_file_path.open('w') as nyf:
        nyf.write(MOCK_NON_YAML_FILE_STR)
    return ny_file_path


def mock_args_file(dir_path):
    args_file_path = dir_path / 'mock_args.yaml'
    with args_file_path.open('w') as aff:
        yaml.dump(MOCK_ARGS_FILE_DICT, aff)
    return args_file_path


@pytest.fixture()
def mock_param_yaml_dict():
    yaml_dict = {MOCK_PARAM_DICT_PATH: MOCK_PARAM_DICT,
                 MOCK_CHI_PARAM_DICT_PATH: MOCK_PARAM_CHI_DICT}
    return yaml_dict


@pytest.fixture()
def mock_leaf_dir():
    """Create a directory to use a leaf chi directory for testing 

    Returns
    -------
    Path
        Path to root directory
    """
    chi_leaf_path = Path.cwd() / 'tests/mock_leaf'
    chi_leaf_path.mkdir()
    yaml_param_path = chi_leaf_path / MOCK_PARAM_DICT_PATH

    with yaml_param_path.open('w') as ypp:
        yaml.dump(MOCK_PARAM_DICT, ypp)

    yield chi_leaf_path


@pytest.fixture()
def mock_root_dir():
    """Create a directory to use a root chi directory for testing 

    Returns
    -------
    Path
        Path to root directory
    """
    chi_root_path = Path.cwd() / 'tests/mock_root'
    chi_root_path.mkdir()
    yaml_param_path = chi_root_path / MOCK_PARAM_DICT_PATH
    yaml_chi_param_path = chi_root_path / MOCK_CHI_PARAM_DICT_PATH

    with yaml_param_path.open('w') as ypp:
        yaml.dump(MOCK_PARAM_DICT, ypp)
    with yaml_chi_param_path.open('w') as ycpp:
        yaml.dump(MOCK_PARAM_CHI_DICT, ycpp)

    yield chi_root_path


@pytest.fixture()
def mock_create_opts():
    def opts(x): return None
    opts.command = 'create'
    opts.replace = 'False'
    opts.non_yaml = []
    yield opts


@pytest.fixture()
def mock_run_opts():
    def opts(x): return None
    opts.command = 'run'
    opts.use_sim_states = 'False'
    opts.args_dict = MOCK_ARGS_FILE_DICT
    opts.states = list(opts.args_dict.keys())
    yield opts

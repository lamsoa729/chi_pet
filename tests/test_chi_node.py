#!/usr/bin/env python

"""@package docstring
File: test_chi_node.py
Author: Adam Lamson
Email: adam.lamson@colorado.edu
Description:
"""

from pathlib import Path
from shutil import rmtree
import pytest
import yaml
from chi_pet.chi_node import ChiNode

MOCK_YAML_DICT = {"mock_param.yaml": {"param": 1}}


def clean_mocks():
    """Clean up mock directories and files before testing to make sure we are
    working from a clean slate.
    """
    for mpath in Path('.').glob('tests/mock*'):
        if mpath.is_file():
            mpath.unlink()
        elif mpath.is_dir():
            rmtree(mpath)

#


@pytest.fixture(scope='session')
def mock_chi_node():
    """Create a mock of ChiNode to use in testing

    Returns
    -------
    ChiNode
        Mock of ChiNode class
    """
    cnode = ChiNode('tests/mock_node', None, MOCK_YAML_DICT)
    return cnode


@pytest.fixture(autouse=True)
def setup_and_teardown():
    clean_mocks()
    yield
    clean_mocks()


def test_chi_node_dir_creation(mock_chi_node):
    """!Test to make sure chi node make
    @return: Test to make sure chi node can create a directory with proper structure

    """
    cnode = mock_chi_node
    cnode.make_node_dir()
    assert Path('tests/mock_node').exists()
    assert Path('tests/mock_node/mock_param.yaml').exists()
    assert Path('tests/mock_node/data').exists()


def test_chi_node_yaml_file(mock_chi_node):
    """!Test to make sure mock yaml file is

    @param mock_chi_node: TODO
    @return: TODO

    """
    cnode = mock_chi_node
    cnode.make_yaml_files(Path('tests'))
    with open('tests/mock_param.yaml', 'r') as mpy:
        y_dict = yaml.safe_load(mpy)
        assert y_dict == MOCK_YAML_DICT['mock_param.yaml']


def test_chi_node_subnode_creation(mock_chi_node):
    """!Test to make sure subnodes are generated properly

    @param mock_chi_node: TODO
    @return: TODO

    """
    cnode = mock_chi_node
    cnode._level = 1
    cnode.make_node_dir()
    assert Path('tests/mock_node/subnodes').exists()

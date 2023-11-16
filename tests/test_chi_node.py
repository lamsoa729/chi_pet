#!/usr/bin/env python

"""@package docstring
File: test_chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from pathlib import Path
from shutil import rmtree
import pytest
from chi_pet.chi_node import ChiNode
from chi_pet.chi_dict import ChiDict
from test_chi_dict import mock_chi_dict
from mhelpers import setup_and_teardown, mock_non_yaml_file, mock_yaml_dict


@pytest.fixture()
def mock_chi_node(mock_chi_dict):
    """Create a mock of ChiNode to use in testing

    Returns
    -------
    ChiNode
        Mock of ChiNode class
    """

    cnode = ChiNode('tests/mock_node', mock_chi_dict)
    return cnode


def test_chi_node_dir_creation(mock_chi_node):
    """!Test to make sure chi node make
    @return: Test to make sure chi node can create a directory with proper structure

    """
    cnode = mock_chi_node
    cnode.make_node_dir()
    assert Path('tests/mock_node').exists()
    assert Path('tests/mock_node/mock_param.yaml').exists()
    assert Path('tests/mock_node/data').exists()


def test_chi_node_subnode_creation(mock_chi_node):
    """!Test to make sure subnodes are generated properly

    @param mock_chi_node: TODO
    @return: TODO

    """
    cnode = mock_chi_node
    cnode._level = 1
    cnode.make_node_dir()
    assert Path('tests/mock_node/subnodes').exists()

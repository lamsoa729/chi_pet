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
from copy import deepcopy
from chi_pet.chi_node import ChiNode
from chi_pet.chi_dict import ChiDict
from test_chi_dict import mock_chi_dict
from mhelpers import *


@pytest.fixture()
def mock_chi_node(mock_chi_dict, mock_create_opts):
    """Create a mock of ChiNode to use in testing

    Returns
    -------
    ChiNode
        Mock of ChiNode class
    """

    cnode = ChiNode('tests/mock_node', mock_chi_dict, mock_create_opts)
    return cnode


def test_chi_node_dir_creation(mock_chi_node):
    """!Test to make sure chi node make
    @return: Test to make sure chi node can create a directory with proper structure

    """

    mock_chi_node.make_node_dir(mock_chi_node._node_path)
    assert Path('tests/mock_node').exists()
    assert Path('tests/mock_node/mock_param.yaml').exists()
    assert Path('tests/mock_node/data').exists()


def test_chi_node_subnode_creation(mock_root_dir, mock_create_opts):
    """!Test to make sure subnodes are generated properly.
    """
    root_path = mock_root_dir
    mock_create_opts.param_file_paths = list(root_path.glob('*.yaml'))

    cnode = ChiNode(root_path, opts=mock_create_opts)
    cnode.make_subnodes()
    assert Path('tests/mock_root/subnodes').exists()
    for pa in [10, 20, 30]:
        pa_dir_path = Path(f'tests/mock_root/subnodes/pA{pa}')
        assert pa_dir_path.exists()
        assert (pa_dir_path / 'mock_param.yaml').exists()
        assert (yaml.safe_load(
            (pa_dir_path / 'mock_param_chi_param.yaml').open('r'))['var_param'] == pa)


def test_chi_node_multilevel_subnode_creation(mock_yaml_dict, mock_create_opts):
    root_path = Path.cwd() / 'tests/mock_root'
    # Add another ChiParam at a lower level
    yaml_dict = deepcopy(mock_yaml_dict)
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3], level=1)"
    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)
    cnode.make_node_dir(root_path)
    cnode.make_subnodes()
    for pa in [10, 20, 30]:
        pa_dir_path = Path(f'tests/mock_root/subnodes/pA{pa}')
        assert pa_dir_path.exists()

        pa_subnode_path = pa_dir_path / 'subnodes'
        assert pa_subnode_path.exists()

        for pb in [.1, .2, .3]:
            pb_dir_path = pa_subnode_path / f'pB{pb}'
            assert pb_dir_path.exists()
            assert (pb_dir_path / MOCK_PARAM_DICT_PATH).exists()
            assert (pb_dir_path / MOCK_CHI_PARAM_DICT_PATH).exists()

            assert (yaml.safe_load(
                (pb_dir_path / MOCK_CHI_PARAM_DICT_PATH).open('r'))['var_param'] == pa)
            assert (yaml.safe_load(
                (pb_dir_path / MOCK_PARAM_DICT_PATH).open('r'))['chi_param_2'] == pb)


def test_chi_node_combinatorics_subnode_creation(mock_yaml_dict, mock_create_opts):
    root_path = Path.cwd() / 'tests/mock_root'
    # Add another ChiParam at a lower level
    yaml_dict = deepcopy(mock_yaml_dict)
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3])"
    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)
    cnode.make_node_dir(root_path)
    cnode.make_subnodes()
    # TODO NEXT finish this test
    chi_dir_name_list = [ppath.name for ppath in Path(
        f'tests/mock_root/subnodes/').glob('*')]
    for pa in [10, 20, 30]:
        for pb in [.1, .2, .3]:
            assert f'pA{pa}_pB{pb}' in chi_dir_name_list
    #     assert pa_dir_path.exists()

    #     pa_subnode_path = pa_dir_path / 'subnodes'
    #     assert pa_subnode_path.exists()

    #         pb_dir_path = pa_subnode_path / f'pB{pb}'
    #         assert pb_dir_path.exists()
    #         assert (pb_dir_path / MOCK_PARAM_DICT_PATH).exists()
    #         assert (pb_dir_path / MOCK_CHI_PARAM_DICT_PATH).exists()

    #         assert (yaml.safe_load(
    #             (pb_dir_path / MOCK_CHI_PARAM_DICT_PATH).open('r'))['var_param'] == pa)
    #         assert (yaml.safe_load(
    #             (pb_dir_path / MOCK_PARAM_DICT_PATH).open('r'))['chi_param_2'] == pb)

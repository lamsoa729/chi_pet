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
    """!Test to make sure subnodes are generated properly for basic usage.
    """
    root_path = mock_root_dir
    mock_args_path = mock_args_file(root_path)

    ny_file_path = root_path / 'mock_ny_file.txt'
    mock_non_yaml_file(root_path)

    mock_create_opts.args_files = [mock_args_path]

    mock_create_opts.param_files = list(root_path.glob('*.yaml'))

    mock_create_opts.non_yaml = [ny_file_path]

    cnode = ChiNode(root_path, opts=mock_create_opts)
    cnode.make_subnodes()
    assert Path('tests/mock_root/subnodes').exists()
    for pa in [10, 20, 30]:
        pa_dir_path = Path(f'tests/mock_root/subnodes/pA{pa}')
        assert pa_dir_path.exists()
        assert (pa_dir_path / 'mock_param.yaml').exists()
        assert (yaml.safe_load(
            (pa_dir_path / 'mock_param_chi_param.yaml').open('r'))['var_param'] == pa)
        assert (pa_dir_path / 'mock_args.yaml').exists()
        assert (pa_dir_path / 'mock_ny_file.txt').exists()


def test_chi_node_multilevel_subnode_creation(mock_param_yaml_dict, mock_create_opts):
    root_path = Path.cwd() / 'tests/mock_root'
    # Add another ChiParam at a lower level
    yaml_dict = deepcopy(mock_param_yaml_dict)
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3], level=1)"
    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)
    assert len(cnode._chi_params) == 2

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


def test_chi_node_combinatorics_subnode_creation(mock_param_yaml_dict, mock_create_opts):
    root_path = Path.cwd() / 'tests/mock_root'
    # Add another ChiParam at a lower level
    yaml_dict = deepcopy(mock_param_yaml_dict)
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3])"
    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)
    cnode.make_node_dir(root_path)
    cnode.make_subnodes()
    for pa in [10, 20, 30]:
        for pb in [.1, .2, .3]:
            p_comb_dir = Path(f'tests/mock_root/subnodes/pA{pa}_pB{pb}')
            assert p_comb_dir.exists()
            assert (p_comb_dir / MOCK_PARAM_DICT_PATH).exists()
            assert (p_comb_dir / MOCK_CHI_PARAM_DICT_PATH).exists()
            assert (p_comb_dir / 'data').exists()

            assert (yaml.safe_load(
                (p_comb_dir / MOCK_CHI_PARAM_DICT_PATH).open('r'))['var_param'] == pa)
            assert (yaml.safe_load(
                (p_comb_dir / MOCK_PARAM_DICT_PATH).open('r'))['chi_param_2'] == pb)


def test_chi_node_matched_subnode_creation(mock_param_yaml_dict, mock_create_opts):
    # Set path for creating node
    root_path = Path.cwd() / 'tests/mock_root'

    # Set up yaml dictionary
    yaml_dict = deepcopy(mock_param_yaml_dict)
    # Change first chi-param to be a matched parameter
    yaml_dict[MOCK_CHI_PARAM_DICT_PATH]['var_param'] = (
        MOCK_CHI_PARAM_STR[:-1] + ", alg='match', param_grp='alpha')")
    # Make second chi-param a matched parameter
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3], alg='match', param_grp='alpha')"

    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)

    cnode.make_node_dir(root_path)
    cnode.make_subnodes()
    for pa, pb in zip([10, 20, 30], [.1, .2, .3]):
        p_comb_dir = Path(f'tests/mock_root/subnodes/pA{pa}_pB{pb}')
        assert p_comb_dir.exists()
        assert (p_comb_dir / MOCK_PARAM_DICT_PATH).exists()
        assert (p_comb_dir / MOCK_CHI_PARAM_DICT_PATH).exists()
        assert (p_comb_dir / 'data').exists()

        assert (yaml.safe_load(
            (p_comb_dir / MOCK_CHI_PARAM_DICT_PATH).open('r'))['var_param'] == pa)
        assert (yaml.safe_load(
            (p_comb_dir / MOCK_PARAM_DICT_PATH).open('r'))['chi_param_2'] == pb)


def test_chi_node_matched_scanned_subnode_creation(mock_param_yaml_dict, mock_create_opts):
    # Set path for creating node
    root_path = Path.cwd() / 'tests/mock_root'

    # Set up yaml dictionary
    yaml_dict = deepcopy(mock_param_yaml_dict)
    # Change first chi-param to be a matched parameter
    yaml_dict[MOCK_CHI_PARAM_DICT_PATH]['var_param'] = (
        MOCK_CHI_PARAM_STR[:-1] + ", alg='match', param_grp='alpha')")
    # Make second chi-param a matched parameter
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3], alg='match', param_grp='alpha')"
    # Make third chi-param a scanned parameter
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_3'] = "ChiParam(name='pC', format_str='pC{:d}', values=[11,22,33], alg='scan')"

    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)

    cnode.make_node_dir(root_path)
    cnode.make_subnodes()
    for pa, pb in zip([10, 20, 30], [.1, .2, .3]):
        for pc in [11, 22, 33]:
            p_comb_dir = Path(
                f'tests/mock_root/subnodes/pA{pa}_pB{pb}_pC{pc}')
            assert p_comb_dir.exists()
            assert (p_comb_dir / MOCK_PARAM_DICT_PATH).exists()
            assert (p_comb_dir / MOCK_CHI_PARAM_DICT_PATH).exists()
            assert (p_comb_dir / 'data').exists()

            assert (yaml.safe_load(
                (p_comb_dir / MOCK_CHI_PARAM_DICT_PATH).open('r'))['var_param'] == pa)
            assert (yaml.safe_load(
                (p_comb_dir / MOCK_PARAM_DICT_PATH).open('r'))['chi_param_2'] == pb)
            assert (yaml.safe_load(
                (p_comb_dir / MOCK_PARAM_DICT_PATH).open('r'))['chi_param_3'] == pc)


@pytest.mark.parametrize("chi_param_2_str",
                         ["ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3,.4], alg='match', param_grp='alpha')",
                          "ChiParam(name='pB', format_str='pB{:.1f}', values=[.1,.2,.3], alg='match')"])
def test_chi_node_matched_creation_runtime_error(mock_param_yaml_dict, mock_create_opts, chi_param_2_str):
    # Set path for creating node
    root_path = Path.cwd() / 'tests/mock_root'

    # Set up yaml dictionary
    yaml_dict = deepcopy(mock_param_yaml_dict)
    # Change first chi-param to be a matched parameter
    yaml_dict[MOCK_CHI_PARAM_DICT_PATH]['var_param'] = (
        MOCK_CHI_PARAM_STR[:-1] + ", alg='match', param_grp='alpha')")
    # Make second chi-param a matched parameter but with different number of values (should throw error)
    yaml_dict[MOCK_PARAM_DICT_PATH][
        'chi_param_2'] = chi_param_2_str
    # Make third chi-param a scanned parameter

    chi_dict = ChiDict(param_dict=yaml_dict)
    cnode = ChiNode(root_path, chi_dict, opts=mock_create_opts)

    cnode.make_node_dir(root_path)
    with pytest.raises(RuntimeError):
        cnode.make_subnodes()

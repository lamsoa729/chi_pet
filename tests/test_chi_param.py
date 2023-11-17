#!/usr/bin/env python

"""@package docstring
File: test_chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from pathlib import Path
from shutil import rmtree
from mhelpers import setup_and_teardown,  MOCK_CHI_PARAM_STR
from chi_pet.chi_param import ChiParam
import pytest
import yaml


@pytest.fixture()
def mock_chi_param():
    chi_param = eval(MOCK_CHI_PARAM_STR)
    return chi_param


def test_chi_param_init():
    chi_param = ChiParam(name='pA', format_str='pA{:d}', values=[10, 20, 30])
    assert chi_param._name == 'pA'
    assert chi_param._format_str == 'pA{:d}'
    assert chi_param._values == [10, 20, 30]


def test_gen_param_values(mock_chi_param):
    assert mock_chi_param._values == [10, 20, 30]
    mock_chi_param._exec_str = 'list(range(4))'
    mock_chi_param.gen_param_values()
    assert mock_chi_param._values == [10, 20, 30]
    mock_chi_param._values = None
    mock_chi_param.gen_param_values()
    assert mock_chi_param._values == [0, 1, 2, 3]


def test_realize_param():
    # TODO next
    assert False

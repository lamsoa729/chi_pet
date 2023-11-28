#!/usr/bin/env python

"""@package docstring
File: test_chi_node.py
Author: Adam Lamson
Email: alamson@flatironinstitute.org
Description:
"""

from pathlib import Path
from mhelpers import MOCK_CHI_PARAM_STR, mock_yaml_dict
from chi_pet.chi_param import ChiParam, ObjRef
import pytest


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


def test_obj_reference():
    # Create a dictionary
    test_dict = {'test': 1,
                 'test2': 2,
                 'test3_list': ['a', 'b', 'c']}
    # Create an object reference in that dictionary
    obj_ref = ObjRef(test_dict['test3_list'], 0)
    # Change the value in the dictionary using obj reference
    obj_ref.set_value('d')
    # Check value is what was given
    assert test_dict['test3_list'][0] == 'd'
    assert test_dict['test3_list'][0] == obj_ref.get_value()
    # Make sure rest of dictionary was not changed
    assert test_dict['test3_list'][1] == 'b'
    assert test_dict['test'] == 1


def test_realize_param(mock_yaml_dict):
    # Create an obj reference to chi param string
    obj_ref = ObjRef(mock_yaml_dict['mock_param_chi_param.yaml'],
                     'var_param')
    # Create a chi param object from the string
    chi_param = eval(obj_ref.get_value())
    # Set obj_ref
    chi_param.set_obj_ref(obj_ref)
    # Realize the chi param
    for i, val in enumerate(chi_param._values):
        chi_param.set_value(i)
        assert chi_param._obj_r.get_value() == val
        assert mock_yaml_dict['mock_param_chi_param.yaml']['var_param'] == val
    assert mock_yaml_dict['mock_param_chi_param.yaml']['param_two'] == 'two'

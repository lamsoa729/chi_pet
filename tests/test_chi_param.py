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


def test_chi_param_init():
    chi_param = ChiParam(name='pA', format_str='pA{:d}', values=[10, 20, 30])
    assert chi_param._name == 'pA'
    assert chi_param._format_str == 'pA{:d}'
    assert chi_param._values == [10, 20, 30]

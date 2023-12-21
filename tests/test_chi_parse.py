# -*- coding: utf-8 -*-
"""Tests for `chi_pet` package."""

import argparse
from pathlib import Path
import pytest
import sys

from unittest import mock
from chi_pet.chi_parse import parse_chi_options

# @pytest.mark.parametrize("command,arg_dict", [
#     ('create', 'value1'),
#     ('run', 'value2'),
#     # Add more tuples for more test cases
# ])


def test_chi_create_argument_parsing():
    # Setup
    sys.argv = ['chi', 'create', 'param1.yaml',
                'param2.yaml', '-a', 'args.yaml']
    # Test
    opts = parse_chi_options()
    # Assert
    assert opts.command == 'create'
    for pf in sys.argv[2:4]:
        assert Path(pf) in opts.param_files


def test_chi_run_argument_parsing():
    # Setup
    sys.argv = ['chi', 'run', '-a',  'args.yaml']
    opts = parse_chi_options()
    assert opts.args_file == Path('args.yaml')

# -*- coding: utf-8 -*-
"""Tests for `chi_run` module of `chi_pet` package."""

from pathlib import Path
from chi_pet.chi_run import ChiRun
from mhelpers import *
import pytest


def test_chi_run_states(mock_run_opts):
    """Test chi_run."""
    # Make a ChiRun object
    crun = ChiRun(mock_run_opts)

    assert crun.get_run_states() == mock_run_opts.states


def test_chi_run_touch(mock_leaf_dir, mock_run_opts):
    """Test chi_run."""
    mock_leaf_path = mock_leaf_dir
    # Create and modify run optoins
    mock_run_opts.args_dict = MOCK_SHELL_ARGS_FILE_DICT
    mock_run_opts.states = mock_run_opts.args_dict.keys()
    mock_run_opts.workdir = mock_leaf_path

    # Make a ChiRun object
    crun = ChiRun(mock_run_opts)
    # Run the pipeline
    crun.run()

    # Make sure action is carried out
    assert (mock_leaf_path / 'mock_output1.txt').exists()
    assert (mock_leaf_path / 'mock_output2.txt').exists()


def test_chi_run_only_one_touch_with_opts(mock_leaf_dir, mock_run_opts):
    """Test chi_run."""
    mock_leaf_path = mock_leaf_dir
    # Create and modify run optoins
    mock_run_opts.args_dict = MOCK_SHELL_ARGS_FILE_DICT
    mock_run_opts.states = ['touch1']
    mock_run_opts.workdir = mock_leaf_path

    # Make a ChiRun object
    crun = ChiRun(mock_run_opts)
    # Run the pipeline
    crun.run()

    # Make sure action is carried out
    assert (mock_leaf_path / 'mock_output1.txt').exists()
    assert not (mock_leaf_path / 'mock_output2.txt').exists()


# TODO NEXT TEST test run args to make sure it always returns you to the right directory

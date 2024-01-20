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


def test_chi_run_with_touch(mock_run_opts):
    """Test chi_run."""
    # Make a ChiRun object
    crun = ChiRun(mock_run_opts)

    assert crun.get_run_states() == mock_run_opts.states

    # Run the pipeline
    # Make sure action is carried out

# TODO NEXT TEST add tests for chi_run.py

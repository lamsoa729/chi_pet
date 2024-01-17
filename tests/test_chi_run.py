# -*- coding: utf-8 -*-
"""Tests for `chi_run` module of `chi_pet` package."""

from pathlib import Path
from chi_pet.chi_run import ChiRun
from mhelpers import *
import pytest


# TODO NEXT TEST add tests for chi_run.py
def test_chi_run_pipeline(mock_run_opts):
    """Test chi_run."""
    mock_run_opts.args_dict = MOCK_ARGS_FILE_DICT
    # Make a ChiRun object
    crun = ChiRun(mock_run_opts)

    assert True
    # Run the pipeline
    # Make sure action is carried out

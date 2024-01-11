# -*- coding: utf-8 -*-
"""Tests for `chi_run` module of `chi_pet` package."""

from pathlib import Path
from chi_pet.chi_run import ChiRun
import pytest


@pytest.fixture()
def mock_args_dict(mock_chi_dict, mock_create_opts):
    """Create a mock of ChiNode to use in testing

    Returns
    -------
    opts
        Mock opts object with args_dict attribute
    """
    pass


# TODO NEXT TEST add tests for chi_run.py
def test_chi_run_pipeline():
    """Test chi_run."""
    assert True
    # Mock an opts object
    # Make a ChiRun object
    # Run the pipeline
    # Make sure action is carried out

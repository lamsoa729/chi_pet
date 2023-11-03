# -*- coding: utf-8 -*-
"""Tests for `chi_pet` package."""

import pytest
import random

from chi_pet import chi


@pytest.fixture
def generate_numbers():
    """Sample pytest fixture. Generates list of random integers.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """

    return random.sample(range(100), 10)

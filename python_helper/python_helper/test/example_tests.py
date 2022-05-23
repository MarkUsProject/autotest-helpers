"""
A sample set of test cases.
"""

import unittest

import pytest
from hypothesis import given, strategies as st

from buggy_function import external_buggy


def internal_buggy(x: int) -> int:
    """A buggy function within the same directory as the tests.
    Return 2 * x instead of x.
    """
    return 2 * x


class TestPytests:
    """A class containing test cases"""

    def test_passes_external_buggy(self):
        assert external_buggy(0) == 0

    def test_passes_internal_buggy(self):
        assert internal_buggy(0) == 0

    def test_fails_external_buggy(self):
        assert external_buggy(2) == 2

    def test_fails_internal_buggy(self):
        assert internal_buggy(2) == 2


class TestUnittests(unittest.TestCase):

    def test_passes_external_buggy(self):
        self.assertEqual(external_buggy(0), 0)

    def test_passes_internal_buggy(self):
        self.assertEqual(internal_buggy(0), 0)

    def test_fails_external_buggy(self):
        self.assertEqual(external_buggy(2), 2)

    def test_fails_internal_buggy(self):
        self.assertEqual(internal_buggy(2), 2)


def test_passes_external_buggy():
    assert external_buggy(0) == 0


def test_passes_internal_buggy():
    assert internal_buggy(0) == 0


def test_fails_external_buggy():
    assert external_buggy(2) == 2


def test_fails_internal_buggy():
    assert internal_buggy(2) == 2


@pytest.mark.parametrize('x', [0])
def test_passes_external_parametrize(x: int):
    assert external_buggy(x) == x


@pytest.mark.parametrize('x', [1, 2])
def test_fails_external_parametrize(x: int):
    assert external_buggy(x) == x


@pytest.mark.parametrize('x', [0])
def test_passes_internal_parametrize(x: int):
    assert internal_buggy(x) == x


@pytest.mark.parametrize('x', [1, 2])
def test_fails_internal_parametrize(x: int):
    assert internal_buggy(x) == x


@given(st.integers(min_value=0, max_value=20))
def test_fails_external_hypothesis(x: int):
    assert external_buggy(x) == x


@given(st.integers(min_value=0, max_value=20))
def test_fails_internal_hypothesis(x: int):
    assert internal_buggy(x) == x

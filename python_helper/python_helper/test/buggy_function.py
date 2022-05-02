"""A file containing a function that is to be mocked in the tests.
"""


def external_buggy(x: int) -> int:
    """A buggy function that should return x but returns 2 * x.
    """
    return x * 2

"""A file containing a function that is to be used when mocking in the tests.
"""


def external_buggy(x: int) -> int:
    """A buggy function that returns x.
    """
    return x

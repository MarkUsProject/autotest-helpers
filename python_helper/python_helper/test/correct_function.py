"""A file containing a function that is to be used when mocking in the tests.
"""


def external_buggy(x: int) -> int:
    """A version of buggy_function.external_buggy that correctly returns
    x as opposed to 2 * x.
    """
    return x

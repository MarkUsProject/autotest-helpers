"""A test suite aimed at evaluating what scenarios a timeout decorator
works in (or doesn't).
"""
import pytest

from wrapt_timeout_decorator import timeout

TIMEOUT_LIMIT = 1

# Add additional decorators into this to test them out.
DECORATORS = {
    'wrapt_timeout_decorator': timeout,
    'pytest_timeout': pytest.mark.timeout
}

PARAMETRIZED_IDS = DECORATORS.keys()
PARAMETRIZED_DECORATORS = [DECORATORS[id_] for id_ in PARAMETRIZED_IDS]

ERROR_MESSAGE = "This is an AssertionError!"


def should_timeout():
    """A function that does not terminate and should timeout"""
    while True:
        pass


def raises_error():
    """A function that raises an AssertionError"""
    raise AssertionError(ERROR_MESSAGE)


def returns_value():
    """A function that returns a value"""
    return 10


def pytest_raises():
    """A function that uses pytest.raises"""
    with pytest.raises(AssertionError):
        raises_error()

    raise IndexError


def decorate_function(decorator, fn):
    """Return fn decorated with decorator"""
    return decorator(TIMEOUT_LIMIT)(fn)


@timeout(3)
@pytest.mark.parametrize('decorator', PARAMETRIZED_DECORATORS, ids=PARAMETRIZED_IDS)
def test_raises_timeout(decorator):
    """Test that the decorator <decorator> correctly raises a timeout error
    of some sort.
    """
    try:
        decorate_function(decorator, should_timeout)()
    except Exception as e:
        # We're just checking the 'Timeout' is mentioned in the error name to
        # some degree.
        if "Timeout" in type(e).__name__ and "test_raises_timeout" not in str(e):
            return
        else:
            raise e


@pytest.mark.parametrize('decorator', PARAMETRIZED_DECORATORS, ids=PARAMETRIZED_IDS)
def test_returns_value(decorator):
    """Test that a function with a return statement still returns the original result.
    """
    fn = decorate_function(decorator, returns_value)
    assert fn() == 10, "Calling the decorated function should return the correct value"


@pytest.mark.parametrize('decorator', PARAMETRIZED_DECORATORS, ids=PARAMETRIZED_IDS)
def test_error_raised(decorator):
    """Test to make sure the correct error was raised if a non-timeout occurs.
    """
    fn = decorate_function(decorator, raises_error)

    error_raised = None
    try:
        fn()
    except Exception as e:
        error_raised = e

        if isinstance(e, AssertionError) and str(e) == ERROR_MESSAGE:
            return

    assert False, "Either no error was raised, or the wrong error was raised:\n" \
                  f"{error_raised}"


@timeout(3)
@pytest.mark.parametrize('decorator', PARAMETRIZED_DECORATORS, ids=PARAMETRIZED_IDS)
def test_pytest_raises(decorator):
    """Test that the test cases work with pytest.raises() calls.
    """
    fn = decorate_function(decorator, pytest_raises)

    try:
        fn()
    except IndexError:
        return

    assert False, "Did not raise the correct error"


@timeout(10)
@pytest.mark.parametrize('decorator', PARAMETRIZED_DECORATORS, ids=PARAMETRIZED_IDS)
def test_timeout_error_format(decorator):
    """A test that will fail to see the error message formatting.
    """
    fn = decorate_function(decorator, should_timeout)
    fn()

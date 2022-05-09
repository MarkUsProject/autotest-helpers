"""
Timeout decorator, modified for use on MarkUs.
"""
import os
from typing import Callable
from timeout_decorator import timeout
from timeout_decorator.timeout_decorator import _Timeout, TimeoutError
from functools import wraps


def bound_timeout(seconds: int, use_signals: bool = False) -> Callable:
    """Return a decorator that will time out the test case after <seconds>
    seconds.

    If <use_signals> is True, then timeout_decorator's built in timeout is
    used instead. Note that MarkUs does not work with signals for timeouts.
    """
    error_message = f"Test timed out after {seconds} seconds."

    if use_signals:
        return timeout(seconds)
    else:
        def decorate(function):
            """A decorator that runs <function> and raises a TimeoutError
            as needed, or the original error message.
            """
            # Don't do anything for Windows machines.
            if os.name == 'nt':
                return function

            @wraps(function)
            def _inner_timeout_wrapper(*args, **kwargs):
                """Call <function> with the provided <args> and <kwargs>,
                using _Timeout to raise a timeout if <function> takes
                more than <seconds> seconds.
                """
                return _Timeout(function,
                                TimeoutError,
                                error_message,
                                seconds)(*args, **kwargs)

            @wraps(function)
            def wrapped_for_errors(*args, **kwargs):
                """Call _inner_timeout_wrapper with <args> and <kwargs>.
                If a Timeout is raised, then the decorator also raises a
                Timeout error. Otherwise, the original error message is
                produced.
                """
                rerun_for_errors = False
                timeout_error = None
                try:
                    _inner_timeout_wrapper(*args, **kwargs)
                except TimeoutError as e:
                    timeout_error = e
                except Exception:
                    # If a TimeoutError was not raised, then we have to
                    # re-run the tests to get the original error message.
                    rerun_for_errors = True

                if rerun_for_errors:
                    function(*args, **kwargs)
                elif timeout_error is not None:
                    raise TimeoutError(error_message)

            return wrapped_for_errors

        return decorate

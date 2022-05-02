"""
Helper functions for running student test cases.
"""
from typing import Callable, Union
from types import ModuleType
from unittest.mock import patch
import inspect
import unittest, sys, importlib
from traceback import format_exc

TEST_PREFIX = "test"
TEST_CLASS_PREFIX = "Test"


class _CaseWrapper:
    """A wrapper for test cases.
    """

    def __init__(self, name: str, testcase: Callable, test_module: str) -> None:
        """Initialize this _CaseWrapper with the given <name> and callable
        <testcase>.
        """
        self.name = name
        self._testcase = testcase
        self._test_module = test_module

    def _run(self) -> str:
        """Run this _CaseWrapper's test case and return a string.
        If the test passed, an empty string is returned. Otherwise, the error
        or failure message is returned.
        """
        # If allow_unittest is True, unittest test methods will be included.
        # The returned functions are TestSuite objects, for which .run() should be
        # used.
        if isinstance(self._testcase, unittest.TestSuite):
            result_container = unittest.TestResult()
            self._testcase.run(result_container)
            # Return the failure or errors if any
            if result_container.failures:
                return result_container.failures[0][-1]
            if result_container.errors:
                return result_container.errors[0][-1]
        else:
            try:
                self._testcase()
            except Exception:
                return format_exc()

        # The test case passed and we can return
        return ''

    def run(self, function_to_mock: str = '', function_to_use: Callable = None,
            module_to_replace: str = '', module_to_use: str = '') -> str:
        """Run this _CaseWrapper's test case and return a string.

        If function_to_mock is provided, calls to that function are replaced
        with function_to_use.

        If module_to_replace is provided, then module_to_use is used instead.

        If the test passed, an empty string is returned. Otherwise, the error
        or failure message is returned.

        Precondition: function_to_use is None iff function_to_mock is ''
                      module_to_use and test_module are None iff module_to_replace is ''
        """
        if module_to_replace:
            # Replace the module as needed
            del sys.modules[module_to_replace]
            sys.modules[module_to_replace] = __import__(module_to_use)
            # Re-import the file containing the module, so it uses the
            # replacement
            module_imported = importlib.import_module(self._test_module)
            importlib.reload(module_imported)

        # Run the test as needed
        if not function_to_mock:
            result = self._run()
        else:
            with patch(function_to_mock, wraps=function_to_use):
                result = self._run()

        if module_to_replace:
            # Restore the original settings
            del sys.modules[module_to_replace]
            sys.modules[module_to_replace] = __import__(module_to_replace)

            module_imported = importlib.import_module(self._test_module)
            importlib.reload(module_imported)

        return result


def get_test_cases(test_module: Union[ModuleType, Callable],
                   allow_pytest: bool = False, allow_unittest: bool = False,
                   test_module_name: str = '') -> \
        dict[str, _CaseWrapper]:
    """Return a dictionary mapping the name of test cases in <test_module>
    to a _CaseWrapper which can be used to run the tests.

    If allow_pytest is True, pytest test cases will be included.

    If allow_unittest is True, unittest test methods will be included.
    """
    discovered_tests = {}

    is_unittest = False
    if inspect.isclass(test_module):
        test_module = test_module()
        is_unittest = isinstance(test_module, unittest.TestCase)
        if is_unittest and not allow_unittest:
            return {}
    elif not test_module_name:
        test_module_name = test_module.__name__

    all_items = dir(test_module)

    # Go through all of the items in the given module
    for item_name in all_items:
        item = getattr(test_module, item_name)

        if inspect.isclass(item) and item_name.startswith(TEST_CLASS_PREFIX):
            # If it's a class: extract the relevant test cases.
            class_name = item_name
            test_methods = get_test_cases(item,
                                          allow_pytest=allow_pytest,
                                          allow_unittest=allow_unittest,
                                          test_module_name=test_module_name)

            # Add the test cases to discovered_tests and prefix it with the
            # class name.
            for method in test_methods:
                name = f"{class_name}.{method}"
                discovered_tests[name] = test_methods[method]

        elif (inspect.isfunction(item) or inspect.ismethod(item)) and \
                item_name.startswith(TEST_PREFIX):
            if allow_pytest or (allow_unittest and is_unittest):
                # If it's a method or function, add it to the discovered_tests
                discovered_tests[item_name] = _CaseWrapper(item_name, item, test_module_name)

    return discovered_tests


def get_failures(testcases: dict[str, _CaseWrapper],
                 function_to_mock: str = '', function_to_use: Callable = None,
                 module_to_replace: str = '', module_to_use: str = '') -> set:
    """
    Return a set of all tests that fail in testcases. If function_to_mock is
    provided, function_to_use is used in its place.

    testcases should be a dictionary returned by get_test_cases.

    Precondition: (function_to_mock == '' and function_to_use is None) or \
                  (function_to_mock != '' and function_to_use is not None)
    """
    failures = set()
    for test_name in testcases:
        result = testcases[test_name].run(function_to_mock=function_to_mock,
                                          function_to_use=function_to_use,
                                          module_to_replace=module_to_replace,
                                          module_to_use=module_to_use)
        if result:
            failures.add(test_name)

    return failures

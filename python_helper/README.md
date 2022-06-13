# Python Helper

Helper functions and classes for executing python unit tests.

## Installation:

```shell
pip install git+https://github.com/MarkUsProject/autotest-helpers.git#subdirectory=python_helper
```

## Functions
### bound_timeout(`seconds`)
Return a decorator that will time out the test case after `seconds` seconds. 

A MarkUs-compatible function wrapper based on `timeout_decorator` that will return the original error message if one is raised instead of a Timeout. A TimeoutError will be raised if the provided time (in seconds) is exceeded.

#### Usage
```python
@bound_timeout(10)	# This will timeout if my_function takes longer than 10 seconds to run.
def my_function() -> None:
	...
```

### get_test_cases(`test_module, allow_pytest=False, allow_unittest=False, test_module_name=''`)
Return a dictionary mapping the name of test cases in `test_module`
to a `_CaseWrapper` which can be used to run the tests. `test_module_name` is only required in the case that a module imported into `test_module` needs to be replaced for testing.

If allow_pytest is True, pytest test cases will be included. Otherwise, they will be excluded.

If allow_unittest is True, unittest test methods will be included. Otherwise, they will be excluded.

#### Usage
See [test_utils_student_test_helpers.py](./python_helper/test/test_utils_student_test_helpers.py) for more examples.

```python
test_cases = get_test_cases(example_tests, allow_pytest=True)
for test_name in test_cases:
	result = test_cases[test_name].run()
	# _CaseWrapper.run() will run the test case and return the error message
	# (or an empty string for a success)
```

#### \_CaseWrapper
\_CaseWrapper is a class used to wrap test cases, working for both unittest and pytest cases.

##### `run(self, function_to_mock='', function_to_use=None, module_to_replace='', module_to_use='') -> str` 
Return a string with the results of the test case run: this is an empty string if the test case passes, or the error message if it fails or an error is raised.

- `function_to_mock` is the name of a function to be replaced when running the test case. If this is provided, `function_to_use` must also be provided and should be the function that we want to use in place of `function_to_mock`.
- `module_to_replace` is the name of a module to be replaced when running the test case. If this is provided, `module_to_use` must also be provided and should be the *name* of the module that we want to use in place of `function_to_mock`.

`get_failures` can typically be used in lieu of calling `run` directly.

### get_failures(testcases, function_to_mock='', function_to_use=None, module_to_replace='', module_to_use='')
Return a set of the test case names in `testcases` that failed when run.

- `function_to_mock` is the name of a function to be replaced when running the test case. If this is provided, `function_to_use` must also be provided and should be the function that we want to use in place of `function_to_mock`.
- `module_to_replace` is the name of a module to be replaced when running the test case. If this is provided, `module_to_use` must also be provided and should be the *name* of the module that we want to use in place of `function_to_mock`.

#### Usage
See [test_utils_student_test_helpers.py](./python_helper/test/test_utils_student_test_helpers.py) for more examples.

```python
test_cases = get_test_cases(example_tests, allow_pytest=True)
failures = get_failures(test_cases)
```

### get_doctest_dict(`function`)
Return a dictionary mapping the doctest examples of `<function>` to their expected return value.

#### Usage
```python
doctest_examples = get_doctest_dict(function)
```

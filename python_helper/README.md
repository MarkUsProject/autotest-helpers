# Python Helper

Helper functions and classes for executing python unit tests.

## Installation:

```shell
pip install git+https://github.com/MarkUsProject/autotest-helpers.git#subdirectory=python_helper
```

## General helpers
### bound_timeout(`seconds`)
Return a decorator that will time out the test case after `seconds` seconds. 

A MarkUs-compatible function wrapper based on `timeout_decorator` that will return the original error message if one is raised instead of a Timeout. A TimeoutError will be raised if the provided time (in seconds) is exceeded.

#### Usage
```python
@bound_timeout(10)	# This will timeout if my_function takes longer than 10 seconds to run.
def my_function() -> None:
	...
```

### module_fixture(`modname`)
Return a pytest fixture to import the module modname.

If the module cannot be imported, a detailed error message is raised.

#### Usage
```python
my_module = module_fixture('my_module')

def test_student(my_module) -> None:
    my_module.blah()
```

### module_lookup(`mod`, `attr`, `attr_type`)
Return the attribute attr from module mod. If mod does not have attr, an AssertionError is raised.

attr_type is used only to format the error message. Typically 'class' or 'function'.

#### Usage
```python
@pytest.fixture(scope="module")
def MyClass(my_module):
    return module_lookup(my_module, 'MyClass', 'class')
```

## Test case validation helpers
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
See [test_test_case_validation.py](./python_helper/test/test_test_case_validation.py) for more examples.

```python
test_cases = get_test_cases(example_tests, allow_pytest=True)
failures = get_failures(test_cases)
```
### make_test_results_fixture(`module`, `function_to_mock`, `functions_to_mock`, `module_to_replace`, `modules_to_use`, `allow_pytest`, `allow_unittest`, `exclusions`)
Return a fixture that contains the results of the testcases in `module` when replacing the given functions/modules with various others.

The fixture itself returns a ResultsGrid object, composed of ResultsRow objects. These contain information about 1) each test case, and 2) whether the test case passed or failed when run on each of the mocked functions/modules.

#### Usage
See [test_test_case_validation_fixture.py](./python_helper/test/test_test_case_validation_fixture.py) for more exapmles.

```python
results_fixture = make_test_results_fixture(example_tests,
	                                        function_to_mock='fn',
	                                        functions_to_use=[fn_v1, fn_v2, fn_v3],
	                                        allow_pytest=True
	                                        )

def test_example(results_fixture):
	# len() return the number of test cases discovered
	assert len(results_fixture) > 0

	# The filter method returns the names of the tests that
	# fulfill the given criteria
	filtered_tests = results_fixture.filter(must_pass={'fn_v1'}, must_fail={'fn_v2'})
	assert len(filtered_tests) > 0

def test_example2(results_fixture):
	# __getitem__ can be used to get specific tests and mocked functions
	assert results_fixture['test_the_student_wrote']['fn_v3'] is True

	# Or you can iterate over the results
	for test_row in results_fixture:
		assert test_row['fn_v1'] is True
		assert all(test_result for test_result in test_row)
```

### get_doctest_dict(`function`)
Return a dictionary mapping the doctest examples of `<function>` to their expected return value.

#### Usage
```python
doctest_examples = get_doctest_dict(function)
```

## Coverage helpers
### get_test_coverage_dict(`test_module`, `modules_to_check`, [`modules_to_replace: Optional[dict]`)
Return a dictionary mapping modules in `modules_to_check` to a CoverageResults object generated by running the tests in `test_module`.

#### Usage
```python
cd = get_test_coverage_dict(example_tests, ['correct_function.py'],
                            modules_to_replace={'buggy_function': 'correct_function'})

assert cd['correct_function.py'].percent_covered == 100.0
```

#### CoverageResults
CoverageResults is a class with the following attributes:

- `filename`: the name of the file for which coverage was checked
- `executed_lines`: a list of the lines executed in the file
- `missing_lines`: a list of the lines missing
- `excluded_lines`: a list of the excluded lines
- `covered_lines`: the number of lines covered
- `num_statements`: the number of statements in the file
- `percent_covered`: the percentage of coverage


### make_test_coverage_fixture(`test_module`, `modules_to_check`, [`modules_to_replace: Optional[dict]`)
Return a fixture that returned a test coverage dictionary (see above.)

## Code inspection helpers
### is_unimplemented(obj_or_path, function_name) -> bool
Return True if the body of the function `function_name` in the given object
or path is not implemented (empty). This ignores all comments.

- `obj_or_path` is the name of the file to search, the module, or the function itself
- `function_name` is the name of the function to check

#### Usage
See [test_code_properties](./python_helper/test/test_code_properties.py) for more examples.

```python
assert is_unimplemented('test/example_code.py', function_name='empty_pass')
```


### get_recursive(obj_or_path, indirect = True)
Return a set of recursive functions and methods in `obj_or_path`.

- `obj_or_path` is the name of the file to search, the module, or the function itself. If obj_or_path is a list of elements, all of them are parsed before checking for recursive functions.
- `indirect` checks for direct recursion (e.g. the function must call on itself directly to be considered recursive.)

#### Usage
See [test_code_properties](./python_helper/test/test_code_properties.py) for more examples.

```python
assert 'recursive_direct' in get_recursive('test/example_code.py')
```

### get_functions_using(obj_or_path, ast_types, indirect=True)
Return a set of functions/methods defined in obj_or_path that use any of the AST types in ast_types (e.g. `ast.For`, `ast.While`).

- `obj_or_path` is the name of the file to search, the module, or the function itself. If obj_or_path is a list of elements, all of them are parsed before checking for recursive functions.
- `ast_types` is a set of AST types (e.g. `ast.For`, `ast.While`) that functions are checked for
- `indirect` checks for direct usage (e.g. the function must use the given syntax within its own body.)

#### Usage
See [test_code_properties](./python_helper/test/test_code_properties.py) for more examples.

```python
assert 'loop_for' in get_functions_using('test/example_code.py', {ast.For})
```

### get_functions_that_call(obj_or_path, function_names, indirect=True)
Return a set of functions/methods defined in obj_or_path that call any of the functions or methods in function_names.

- `obj_or_path` is the name of the file to search, the module, or the function itself. If obj_or_path is a list of elements, all of them are parsed before checking for recursive functions.
- `function_names` is a set of function names to check usage of.
- `indirect` checks for direct usage (e.g. the function must call the given function within its own body.)

#### Usage
See [test_code_properties](./python_helper/test/test_code_properties.py) for more examples.

```python
assert 'sorted_call' in get_functions_that_call('test/example_code.py', {'sorted'})
```

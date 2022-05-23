from python_helper.utils_student_test_helpers import _CaseWrapper, get_failures, get_test_cases

FAIL_IDENTIFIER = "_fails_"
PASS_IDENTIFIER = "_passes_"


def correct_function(x: int) -> int:
    """A buggy function within the same directory as the tests.
    Return x.
    """
    return x


class TestGetTestCases:
    """Tests for get_test_cases.
    """

    def verify_test_results(self, test_cases: dict[str, _CaseWrapper]):
        """Verifies that all of the tests in test_cases run correctly and
        produce the correct output (no results when a test passes, results when
        it doesn't).
        """
        checked_tests = 0
        for testname in test_cases:
            results = test_cases[testname].run()
            if PASS_IDENTIFIER in testname:
                checked_tests += 1
                assert results == '', f'{testname} should have passed but failed.'

            if FAIL_IDENTIFIER in testname:
                checked_tests += 1
                assert results, f'{testname} should have failed but passed.'

        # One last check to make sure all tests were included
        assert checked_tests == len(test_cases)

    def test_pytest_only(self):
        """Test that the correct test cases are returned when only allowing
        pytests.
        """
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True)

        assert set(test_cases) == {'TestPytests.test_passes_external_buggy',
                                   'TestPytests.test_passes_internal_buggy',
                                   'TestPytests.test_fails_external_buggy',
                                   'TestPytests.test_fails_internal_buggy',
                                   'test_passes_external_buggy',
                                   'test_passes_internal_buggy',
                                   'test_fails_external_buggy',
                                   'test_fails_internal_buggy',
                                   'test_fails_external_hypothesis',
                                   'test_fails_internal_hypothesis',
                                   'test_fails_external_parametrize[1]',
                                   'test_fails_external_parametrize[2]',
                                   'test_fails_internal_parametrize[1]',
                                   'test_fails_internal_parametrize[2]',
                                   'test_passes_external_parametrize[0]',
                                   'test_passes_internal_parametrize[0]'
                                   }

    def test_unittest_only(self):
        """Test that the correct test cases are returned when only allowing
        unittests.
        """
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_unittest=True)

        assert set(test_cases) == {'TestUnittests.test_passes_external_buggy',
                                   'TestUnittests.test_passes_internal_buggy',
                                   'TestUnittests.test_fails_external_buggy',
                                   'TestUnittests.test_fails_internal_buggy'
                                   }

    def test_pytest_and_unittest(self):
        """Test that the correct test cases are returned when allowing both
        pytests and unittests.
        """
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        assert set(test_cases) == {'TestPytests.test_passes_external_buggy',
                                   'TestPytests.test_passes_internal_buggy',
                                   'TestPytests.test_fails_external_buggy',
                                   'TestPytests.test_fails_internal_buggy',
                                   'TestUnittests.test_passes_external_buggy',
                                   'TestUnittests.test_passes_internal_buggy',
                                   'TestUnittests.test_fails_external_buggy',
                                   'TestUnittests.test_fails_internal_buggy',
                                   'test_passes_external_buggy',
                                   'test_passes_internal_buggy',
                                   'test_fails_external_buggy',
                                   'test_fails_internal_buggy',
                                   'test_fails_external_hypothesis',
                                   'test_fails_internal_hypothesis',
                                   'test_fails_external_parametrize[1]',
                                   'test_fails_external_parametrize[2]',
                                   'test_fails_internal_parametrize[1]',
                                   'test_fails_internal_parametrize[2]',
                                   'test_passes_external_parametrize[0]',
                                   'test_passes_internal_parametrize[0]'
                                   }

    def test_pytest_runs(self):
        """Test that the returned Pytest tests run correctly.
        """
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True)
        self.verify_test_results(test_cases)

    def test_unittest_runs(self):
        """Test that the returned Unittest tests run correctly.
        """
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_unittest=True)
        self.verify_test_results(test_cases)


class TestRunWithReplacements:
    def test_replace_with_correct_internal(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (internal) version."""
        from unittest.mock import patch
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        for test_name in test_cases:
            if 'internal' in test_name:
                assert test_cases[test_name].run(function_to_mock='example_tests.internal_buggy',
                                                 function_to_use=correct_function) == ''

    def test_replace_with_correct_external(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (internal) version."""
        from unittest.mock import patch
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        for test_name in test_cases:
            if 'external' in test_name:
                assert test_cases[test_name].run(module_to_replace='buggy_function',
                                                 module_to_use='correct_function') == ''

    def test_replace_both(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (internal) version."""
        from unittest.mock import patch
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        for test_name in test_cases:
            assert test_cases[test_name].run(function_to_mock='example_tests.internal_buggy',
                                             function_to_use=correct_function,
                                             module_to_replace='buggy_function',
                                             module_to_use='correct_function') == ''


class TestGetFailures:
    def test_no_replacements(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (internal) version."""
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        actual = get_failures(test_cases)
        assert actual == {'TestPytests.test_fails_external_buggy',
                          'TestPytests.test_fails_internal_buggy',
                          'TestUnittests.test_fails_external_buggy',
                          'TestUnittests.test_fails_internal_buggy',
                          'test_fails_external_buggy',
                          'test_fails_internal_buggy',
                          'test_fails_external_hypothesis',
                          'test_fails_internal_hypothesis',
                          'test_fails_external_parametrize[1]',
                          'test_fails_external_parametrize[2]',
                          'test_fails_internal_parametrize[1]',
                          'test_fails_internal_parametrize[2]'
                          }

    def test_replace_with_correct_internal(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (internal) version."""
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        actual = get_failures(test_cases,
                              function_to_mock='example_tests.internal_buggy',
                              function_to_use=correct_function)
        assert actual == {'TestPytests.test_fails_external_buggy',
                          'TestUnittests.test_fails_external_buggy',
                          'test_fails_external_buggy',
                          'test_fails_external_parametrize[1]',
                          'test_fails_external_parametrize[2]',
                          'test_fails_external_hypothesis',
                          }

    def test_replace_with_correct_external(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (external) version."""
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        actual = get_failures(test_cases,
                              module_to_replace='buggy_function',
                              module_to_use='correct_function')
        assert actual == {'TestPytests.test_fails_internal_buggy',
                          'TestUnittests.test_fails_internal_buggy',
                          'test_fails_internal_buggy',
                          'test_fails_internal_parametrize[1]',
                          'test_fails_internal_parametrize[2]',
                          'test_fails_internal_hypothesis'
                          }

    def test_replace_both(self):
        """Test that all tests pass when the buggy function is mocked and
        replaced with a working (external) version."""
        import example_tests
        test_cases = get_test_cases(example_tests,
                                    allow_pytest=True,
                                    allow_unittest=True)

        actual = get_failures(test_cases,
                              function_to_mock='example_tests.internal_buggy',
                              function_to_use=correct_function,
                              module_to_replace='buggy_function',
                              module_to_use='correct_function')
        assert actual == set()

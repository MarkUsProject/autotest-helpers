import example_tests
import pytest
from python_helper.test_case_validation_fixture import make_test_results_fixture


def internal_buggy_original(x: int) -> int:
    """A buggy function.
    Return 2 * x instead of x.
    """
    return 2 * x


def buggy_fails_0(x: int) -> int:
    """A buggy function that only fails when 0 is passed in
    """
    if x == 0:
        return 99
    return x


def correct_function(x: int) -> int:
    """A buggy function within the same directory as the tests.
    Return x.

    >>> correct_function(1)
    1
    >>> correct_function(2)
    2
    >>> correct_function(3) == 3
    True
    """
    return x


results = make_test_results_fixture(example_tests,
                                    function_to_mock='example_tests.internal_buggy',
                                    functions_to_use=[correct_function,
                                                      internal_buggy_original,
                                                      buggy_fails_0
                                                      ],
                                    allow_pytest=True,
                                    allow_unittest=True,
                                    exclusions={
                                        'TestUnittests.test_fails_external_buggy',
                                        'TestUnittests.test_passes_external_buggy',
                                        'TestPytests.test_fails_external_buggy',
                                        'TestPytests.test_passes_external_buggy',
                                        'test_passes_external_parametrize[0]',
                                        'test_fails_external_buggy',
                                        'test_passes_external_buggy',
                                        'test_fails_external_hypothesis',
                                        'test_fails_external_parametrize[2]',
                                        'test_fails_external_parametrize[1]'
                                    }
                                    )


def test_exclusions(results) -> None:
    """Test that the excluded test names are correctly excluded."""
    assert not any('external' in result.test_name for result in results)
    assert len(results) == 10


def test_correct_grid(results) -> None:
    """Test that the grid has the correct results for all test cases.
    """
    for test_row in results:
        assert test_row['correct_function'] is True

        if 'fails' in test_row.test_name:
            assert test_row['internal_buggy_original'] is False


def test_correct_filter_pass_only(results) -> None:
    """Test that the filter method filters the correct results when given
    functions that must pass.
    """
    filtered_test_names = results.filter(must_pass={'internal_buggy_original'})
    assert len(filtered_test_names) == 4
    assert all('passes' in name for name in filtered_test_names)


def test_correct_filter_fail_only(results) -> None:
    """Test that the filter method filters the correct results when given
    functions that must fail.
    """
    filtered_test_names = results.filter(must_fail={'internal_buggy_original'})
    assert len(filtered_test_names) == 6
    assert all('fails' in name for name in filtered_test_names)


def test_correct_filter(results) -> None:
    """Test that the filter method filters the correct results when given
    functions that must pass or fail.
    """
    filtered_test_names = results.filter(must_pass={'correct_function'},
                                         must_fail={'buggy_fails_0'})

    assert filtered_test_names == {'TestPytests.test_passes_internal_buggy',
                                   'TestUnittests.test_passes_internal_buggy',
                                   'test_fails_internal_hypothesis',
                                   'test_passes_internal_buggy',
                                   'test_passes_internal_parametrize[0]'}


def test_correct_filter_exclusions(results) -> None:
    """Test that the filter method filters the correct results when given
    functions that must pass or fail, and exclusions.
    """
    filtered_test_names = results.filter(must_pass={'correct_function'},
                                         must_fail={'buggy_fails_0'},
                                         exclusions={'TestUnittests.test_passes_internal_buggy',
                                                     'TestPytests.test_passes_internal_buggy'})

    assert filtered_test_names == {'test_fails_internal_hypothesis',
                                   'test_passes_internal_buggy',
                                   'test_passes_internal_parametrize[0]'}

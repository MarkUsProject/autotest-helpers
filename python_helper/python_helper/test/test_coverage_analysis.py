from coverage_analysis import get_test_coverage_dict, make_test_coverage_fixture

import example_tests

coverage_fixture = make_test_coverage_fixture(example_tests, ['buggy_function.py'])


class TestGetCoverageDict:
    def test_replacement(self):
        """Test get_coverage_dict with replacements made"""
        cd = get_test_coverage_dict(example_tests, ['correct_function.py'],
                               modules_to_replace={'buggy_function': 'correct_function'})
        assert cd['correct_function.py'].percent_covered == 100.0

    def test_no_replacement(self):
        """Test get_coverage_dict without any replacements made"""
        cd = get_test_coverage_dict(example_tests, ['buggy_function.py'])

        assert cd['buggy_function.py'].percent_covered == 100.0


def test_fixture(coverage_fixture):
    """Test the fixture created by make_coverage_fixture"""
    assert coverage_fixture['buggy_function.py'].percent_covered == 100.0

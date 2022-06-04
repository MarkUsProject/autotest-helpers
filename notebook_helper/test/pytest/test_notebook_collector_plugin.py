"""Tests for pytest plugin notebook_helper/pytest/notebook_collector_plugin.py"""
import os.path


def test_plugin(testdir):
    testdir.makeconftest(
        """
        pytest_plugins = ['notebook_helper.pytest.notebook_collector_plugin']
        """
    )

    testdir.copy_example(os.path.join(os.path.dirname(__file__), 'fixtures/test.ipynb'))
    result = testdir.runpytest('test.ipynb')

    result.assert_outcomes(
        passed=2,
        failed=4
    )

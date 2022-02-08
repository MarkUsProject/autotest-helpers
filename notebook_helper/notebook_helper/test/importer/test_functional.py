import importlib
import notebook_helper.importer as importer
import pytest

from fixtures import syntax_errors as _syntax_errors
from fixtures import runtime_errors as _runtime_errors

@pytest.fixture
def syntax_errors():
    return importlib.reload(_syntax_errors)


@pytest.fixture
def runtime_errors():
    return importlib.reload(_runtime_errors)


def test_syntax_errors_raise_on_error(syntax_errors):
    with pytest.raises(SyntaxError):
        importer.run_cells(syntax_errors)


def test_syntax_errors_no_raise_on_error(syntax_errors):
    """When raise_on_error=False, the second cell is executed (and x is defined).

    Only the first cell has a syntax error.
    """
    importer.run_cells(syntax_errors, raise_on_error=False)

    assert syntax_errors.x == 0


def test_runtime_errors_raise_on_error(runtime_errors):
    with pytest.raises(TypeError):
        importer.run_cells(runtime_errors)


def test_runtime_errors_no_raise_on_error(runtime_errors):
    """When raise_on_error=False, the second cell is executed (and x is defined).

    Only the first cell has a runtime error.
    """
    importer.run_cells(runtime_errors, raise_on_error=False)

    assert runtime_errors.x == 0

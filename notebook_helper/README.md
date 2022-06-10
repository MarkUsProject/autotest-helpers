# Notebook Helper

This package contains three modules, `importer`, `merger`, and `pytest`.


## Installation:

```shell
pip install 'git+https://github.com/MarkUsProject/autotest-helpers.git#subdirectory=notebook_helper'
```

## importer

This allows jupyter notebooks to be imported as python modules.

Import the `importer` module first and then import files with an `.ipynb` extension. For example:

```python
from notebook_helper import importer
import my_notebook # assumes a file named 'my_notebook.ipynb' in the python path
```

This will not execute the cells in the notebook right away.

To inspect the cells in the notebook:

```python
cells = importer.get_cells(my_notebook) # returns a list of notebook cells
```

To run a single cell:

```python
cells[0].run()
```

To run all cells in order:

```python
for cell in cells:
    cell.run()

# OR

importer.run_cells(my_notebook)
```

### Handling errors

The `run_cells` and `run` functions take a boolean flag `raise_on_error`, which controls their behaviour if an error is raised when executing a cell.

- If `raise_on_error` is `True` (default), the error is raised from `run_cells` and `run`.
- If `raise_on_error` is `False`, the error traceback is printed to stderr, but is not re-raised.

Passing `raise_on_error=False` allows partial execution of a notebook's cells (an error is one cell does not necessarily affect the behaviour of another), which can be useful for testing purposes.

## merger

This provides functions to merge two jupyter notebooks.

The `merge` function returns a notebook created from merging two notebooks: notebook2 into notebook1.

This new notebook will be created by selecting cells from notebook1 and notebook2 in the following way:

1. if a cell in notebook1 has the same id as a cell in notebook2:
    the cell in notebook2 and any preceding cells that have not yet been added to the new notebook
    will be appended to the new notebook.
2. if a cell occurs in notebook1 and there is no corresponding cell with the same id in notebook2:
    the cell in notebook1 will be appended to the new notebook
3. repeat steps 1 and 2 until all cells in notebook1 have been considered.
4. if there remain any cells in notebook2 that have not been added to the new notebook, these cells
   appended to the new notebook

The `check` function checks if two notebooks can be merged with the `merge` function (above). It raises an error if either:

- the two notebooks do share any cells with the same ids
- the two notebooks share cells but those cells occur in different orders.

:warning: If you are creating or editing notebooks with a jupyter-notebook prior to version 6.2, the cell ids will be randomly regenerated every time the notebook is saved and will almost certainly mean that your notebook will not be mergeable later on. See [this change](https://github.com/jupyter/notebook/pull/5928) for more details.

## pytest

The `notebook_helper.pytest.notebook_collector_plugin` module is a [Pytest plugin](https://docs.pytest.org/en/7.1.x/how-to/writing_plugins.html) that enables the collection of test cases from a Jupyter notebook file.
This enables Pytest to execute notebook cells as simple test cases.
Currently, more advanced Pytest features (such as fixtures and parameterized tests) are not supported.

Usage (on an example notebook file in this repository):

```console
$ pytest -p notebook_helper.pytest.notebook_collector_plugin test/pytest/fixtures/test.ipynb 
```

### Creating a test cell

A notebook code cell is marked as a test cell when its first line is a comment and the word `test` (case-insensitive).
For example:

```python
# test that one plus one equals two
assert 1 + 1 == 2
```

### Cell execution and handling non-test cells

During test collection using this plugin, no code is executed in the notebook.
Code cells are only executed when the tests are run.

The plugin partitions all code cells in the notebooks using the test cells, so that each Pytest test case is associated with one test cell and all of the code cells preceding it, up to the previous test cell (if any).

When a test case is run, the associated cells (zero or more non-test cells and one test cell) are executed in the order they appear in the notebook.
If any of these cells raises an error, the test fails and reports the error; however, any subsequent test cases are still executed.

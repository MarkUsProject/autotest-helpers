# Notebook Helper

This package contains two modules, `importer` and `merger`:


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

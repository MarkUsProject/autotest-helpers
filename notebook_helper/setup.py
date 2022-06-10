#!/usr/bin/env python3

import setuptools
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(dir_path, 'AUTHORS.txt')) as f:
    authors = ', '.join([a.strip() for a in f.readlines()])

setuptools.setup(
    name='notebook_helper',
    version='0.0.1',
    description='Helper functions for importing and testing jupyter notebooks.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=authors,
    author_email="mschwa@cs.toronto.edu",
    packages=['notebook_helper.importer', 'notebook_helper.merger', 'notebook_helper.pytest'],
    install_requires=['ipython==7.24.0', 'nbformat==5.1.3', 'pytest>=6.2.1,<8'],
    python_requires='>=3.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

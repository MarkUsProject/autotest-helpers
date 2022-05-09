#!/usr/bin/env python3

import setuptools
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(dir_path, 'AUTHORS.txt')) as f:
    authors = ', '.join([a.strip() for a in f.readlines()])

setuptools.setup(
    name='python_helper',
    version='0.0.1',
    description='Helper functions and classes for executing python unit tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=authors,
    author_email="sophia@cs.toronto.edu",
    packages=['python_helper'],
    install_requires=['timeout-decorator'],
    extras_require={'dev': ['hypothesis']},
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

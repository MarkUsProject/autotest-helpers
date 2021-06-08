#!/usr/bin/env python3

import setuptools
import os
import glob

dir_path = os.path.dirname(os.path.realpath(__file__))
requires = [f"{p} @ file://{os.path.join(dir_path, p)}" for p in ('c_helper', 'sql_helper', 'notebook_helper')]

with open(os.path.join(dir_path, 'README.md')) as f:
    long_description = f.read()

authors = set()
for author_file in glob.glob('*/AUTHORS.txt'):
    with open(author_file) as f:
        authors.update(line.strip() for line in f.readlines())
authors = sorted(list(authors))

setuptools.setup(
    name='autotest_helpers',
    version='0.0.1',
    description='Various python packages designed for use as helpers when writing test scripts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=authors,
    author_email="mschwa@cs.toronto.edu",
    url='https://github.com/MarkUsProject/autotest-helpers.git',
    install_requires=requires,
    python_requires='>=3.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

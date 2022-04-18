#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu April 16 23:54:31 2022

@author: johnomole
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

# The directory containing this file
here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join('smart/requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]

setup (
 name = 'smart',
 description = long_description,
 long_description_content_type='text/markdown',
 version = '1.0.0',
 author='John Omole',
 author_email='contact@johnomole.me',
 keywords='wiki, wikipedia, wikimedia',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=3.8', # any python greater than 2.7
entry_points='''
        [console_scripts]
        smart=smart.app:main
        ''',
include_package_data=True
)

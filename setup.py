#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


__version__ = '0.1.0'


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup_options = {
    'name': 'ficus',
    'version': __version__,
    'description': "file member downloader",
    'long_description': readme,
    'author': "Mark Gemmill",
    'author_email': 'mgemmill@unfi.com',
    'packages': ['ficus'],
    'package_dir': {'ficus': 'ficus'},
    'include_package_data': True,
    'install_requires': requirements,
    'zip_safe': False,
    'keywords': 'ficus'}


print 'normal set up...'
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(**setup_options)

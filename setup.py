#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__version__ = '0.1.1'


with open('README.md') as readme_file:
    readme = readme_file.read()


setup_options = {
    'name': 'ficus',
    'version': __version__,
    'description': "ini config library",
    'long_description': readme,
    'author': "Mark Gemmill",
    'author_email': 'mark@markgemmill.com',
    'packages': ['ficus'],
    'package_dir': {'ficus': 'ficus'},
    'include_package_data': True,
    'install_requires': [],
    'zip_safe': False,
    'keywords': 'ficus'}


setup(**setup_options)

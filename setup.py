# -*- coding: utf-8 -*-
"""
Filename: setup
Created on: 13/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

import sys
import subprocess
from setuptools import setup, find_packages

sys.path.insert(0, '.')
requirements = ['colorama', 'jsonschema']
packages = find_packages()

ver_file = open("version")

__version__ = ver_file.read()
__date__ = '2019/13/02 16:00:00'
__author__ = 'Carlos Colon <espacio.sideral@gmail.com>'
__build = '9385270'

with open('dynamic_hosts/_version.py', 'w+') as f:
    f.write('''\
# I will destroy any changes you make to this file.
# Sincerely,
# setup.py ;)
__version__ = '{}'
__date__ = '{}'
__author__ = '{}'
__build__ = '{}'
'''.format(__version__, __date__, __author__, __build))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ldap_test',
    version=__version__,
    packages=packages,
    install_requires=requirements,
    url='https://github.com/cppmx/dynamic_hosts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU General Public License v3.0',
    author='Carlos Colón',
    author_email='espacio.sideral@gmail.com',
    description='Dynamic Hosts Generator',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: GNU GLP V3 License",
        "Operating System :: OS Independent",
    ),
    options={
        'sdist': {
            'formats': ['gztar', 'zip'],
        },
    }
)


# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages


IS_PY3 = sys.version_info > (3,)

install_requires = (
    'pyramid',
    'PyYAML',
    )
tests_require = [
    ]
extras_require = {
    'test': tests_require,
    }

if not IS_PY3:
    tests_require.append('mock')

description = "Pyramid plugin for YAML logging configuration."
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as readme:
    README = readme.read()
with open(os.path.join(here, 'CHANGES.rst')) as changes:
    CHANGELOG = changes.read()
changelog_header = """\
Change Log
==========
"""
long_description = '\n\n'.join([README, changelog_header, CHANGELOG])


setup(
    name='pyramid_sawing',
    version='1.1.1',
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/pyramid_sawing",
    license='AGPL, See also LICENSE.txt',
    description=description,
    long_description=long_description,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'pyramid_sawing': ['*.yaml'],
        'pyramid_sawing.tests': ['*.yaml'],
        },
    test_suite='pyramid_sawing.tests',
    entry_points={},
    )

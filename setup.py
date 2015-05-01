# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


install_requires = (
    'pyramid',
    'PyYAML',
    )
tests_require = [
    ]
extras_require = {
    'test': tests_require,
    }
description = "Pyramid plugin for YAML logging configuration."


setup(
    name='pyramid_sawing',
    version='0.0.0',
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/pyramid_sawing",
    license='AGPL, See also LICENSE.txt',
    description=description,
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

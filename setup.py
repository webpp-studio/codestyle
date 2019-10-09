#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='codestyle',
    version='0.4.1',
    author=u'Sergey Levitin',
    author_email='selevit@gmail.com',
    packages=find_packages(),
    package_data={
        'codestyle': ['standards/*'],
    },
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/webpp-studio/codestyle',
    license='GPL licence, see LICENCE',
    description='Extendable codestyle checker and fixer',
    long_description=open('README.rst').read(),
    scripts=['scripts/codestyle'],
    install_requires=[
        'future',
        'pep8~=1.7.1',
        'pyflakes~=2.1.1',
        'autopep8~=1.4.4',
        'flake8~=3.7.8',
        'autoflake~=1.3.1',
    ],
    test_suite='tests',
    tests_require=[
        'mock>=2.0,<=2.0.99',
        'six>=1.9'
    ]
)


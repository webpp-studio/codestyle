#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup

setup(
    name='codestyle',
    version='0.0.5',
    author=u'Sergey Levitin',
    author_email='selevit@gmail.com',
    packages=['codestyle'],
    package_dir={'codestyle': 'src'},
    url='https://github.com/selevit/codestyle',
    license='GPL licence, see LICENCE',
    description='Extendable codestyle checker and fixer',
    long_description=open('README.md').read(),
    scripts=['scripts/codestyle'],
    install_requires=['pep8', 'pyflakes', 'autopep8']
)

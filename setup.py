#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='codestyle',
    version='0.4.3',
    author=u'Sergey Levitin',
    author_email='selevit@gmail.com',
    packages=find_packages(),
    package_data={
        'codestyle': ['standards/*'],
    },
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/webpp-studio/codestyle',
    license='GPLv3',
    description='Extendable codestyle checker and fixer',
    long_description=open('README.rst').read(),
    scripts=['scripts/codestyle'],
    install_requires=[
        'future',
        'pep8>=1.5.7,<1.6',
        'pyflakes>=0.8.1,<0.9',
        'autopep8>=1.2,<=1.2.99',
        'flake8>=3.2,<=3.2.99',
        'autoflake>=0.6,<=0.6.99',
    ],
    test_suite='tests',
    tests_require=[
        'mock>=2.0,<=2.0.99',
        'six>=1.9'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

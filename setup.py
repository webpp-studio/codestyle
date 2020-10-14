#!/usr/bin/env python3
"""Модуль установки приложения."""
from setuptools import find_packages, setup

from codestyle import (__version__ as version,
                       __description__ as short_description, __name__ as name,
                       __author__ as author, __author_email__ as author_email,
                       __url__ as url)


with open('README.rst', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', encoding='utf-8') as requirements_file:
    install_requires = requirements_file.read()

application_entrypoint = f'{name} = {name}.command_line:run_process'

setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=False,
    url=url,
    license='GPLv3',
    description=short_description,
    long_description=long_description,
    entry_points={'console_scripts': [application_entrypoint]},
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

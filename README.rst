Codestyle checker
=================

.. image:: https://travis-ci.org/webpp-studio/codestyle.svg?branch=master
    :target: https://travis-ci.org/webpp-studio/codestyle

This script checks and auto fixes codestyle for all supported languages:

1. PHP (phpcs)
2. Python (flake8)
3. Javascript (jscs and jshint)
4. CSS (csscomb)
5. HTML (htmlcs)

Installation
------------

::

    # First install the pip, npm and pear package managers
    # Example for debian
    sudo apt-get install python-pip npm php-pear

    # Install codestyle and dependencies
    pip install codestyle
    npm install -g jshint jscs-fixer csscomb htmlcs walk brace-expansion
    pear install PHP_CodeSniffer

Usage
-----

::

    usage: codestyle [-h] [-i] [-ff] [-c] [-s standard-dir]
                          [-l language name]
                          target [target ...]

    Check and fix code style

    positional arguments:
      target                files for checking

    optional arguments:
      -h, --help            show this help message and exit
      -i, --try-fix         auto fix codestyle errors
      -I --fix-only       fix possible errors without extra checking
      -c, --compact         Show compact output
      -s standard-dir, --standard standard-dir
                            path to the coding standard directory
      -l language name, --language language name
                            force set language for check

Example
-------

::

    # check all supported files in directory recursive
    codestyle /path/to/project/dir

    # check set of files
    codestyle test.js test.php test.py

    # check file and try to fix errors
    codestyle -i test.js

    # check project with compact output (no detail errors information)
    codestyle -c /path/to/project/dir

    # check all project and save full report to file
    codestyle /path/to/project &> report.txt

Dependencies
------------

1. phpcs
2. phpcbf
3. jshint (NodeJS)
4. jscs-fixer (NodeJS)
5. jscs (NodeJS)
6. flake8
7. csscomb (NodeJS)
8. htmlcs >= 0.1.4 (NodeJS)
9. walk (NodeJS)
10. brace-expansion (NodeJS)

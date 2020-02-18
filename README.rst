Codestyle checker
=================

This script checks and auto fixes codestyle for all supported languages:

1. PHP (phpcs)
2. Python (flake8)
3. Javascript (eslint)
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

  usage: codestyle [-h] [-I] [-i] [-c] [-s standard-dir] [-l language name]
                   [-e glob pattern [glob pattern ...]]
                   target [target ...]

  Check and fix a code style

  positional arguments:
    target                files for a checking

  optional arguments:
    -h, --help            show this help message and exit
    -i, --fix             auto fix codestyle errors if possible
    -c, --compact         Show a compact output
    -s standard-dir, --standard standard-dir
                          A path to a coding standard directory
    -l language name, --language language name
                          force set the language for a checking
    -x glob pattern [glob pattern ...], --exclude glob pattern [glob pattern ...]
                          Exclude paths/files from checking

Usage with docker
-----------------

::

  # building image
  docker build -t <image_name> .
  # run container
  docker run --rm --volume=`pwd`:/code --workdir=/code --tty <image_name> [-h] [-I] [-i] [-c] [-s standard-dir] [-l language name]
                                                                          [-e glob pattern [glob pattern ...]]
                                                                          target [target ...]

Save custom parametres for each project
---------------------------------------

::

  You can use file .codestyle.ini to store parametres of codestyle checking for each project.
  1. Create file .codestyle.ini in the root directory of your project
  2. In section [parameters] type needed parametres and values
  3. File format and examples see in file /.codestyle.ini of this project
  4. For --language parameter supported values are: php, js, vue, ts, coffee, py, css, less, html
     Only one value for this parameter is available. By default all the languages is enabled.

Example
-------

::

    # check all supported files in directory recursive
    codestyle /path/to/project/dir
    # check set of files
    codestyle test.js test.php test.py
    # test directory with exclude rules
    codestyle /path -x '*.html' './tests/excluded_dir'
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
3. eslint (NodeJS)
4. flake8
5. csscomb (NodeJS)
6. htmlcs >= 0.1.4 (NodeJS)
7. walk (NodeJS)
8. brace-expansion (NodeJS)

Usage from the docker container
-------------------------------

Bad practices:
    - Use --user $(id -u):$(id -g) parameter with docker run

# Codestyle checker

This script checks and auto fixes codestyle for all supported languages:

1. PHP (phpcs)
2. Python (pep8 and pylint)
3. Javascript (jscs and jshint)
4. CSS (csscomb)

## Installation

```
# First install the pip, npm and pear package managers
# Example for debian 
sudo apt-get install python-pip npm php-pear

# Install codestyle and dependencies
pip install codestyle
npm install -g jshint jscs-fixer csscomb
pear install PHP_CodeSniffer
```

## Usage

```
usage: codestyle [-h] [--fix] [--verbose] target [target ...]

Check and fix code style

positional arguments:
  target      files for the checking

optional arguments:
  -h, --help  show this help message and exit
  --try-fix       Auto fix codestyle errors
  --compact   Show compact output
```

## Example

```
# check all supported files in directory recursive
codestyle /path/to/project/dir

# check set of files
codestyle test.js test.php test.py

# check file and try to fix errors
codestyle --try-fix test.js

# check project with compact output (no detail errors information)
codestyle --compact /path/to/project/dir

# check all project and save full report to file
codestyle /path/to/project &> report.txt
```

## Dependencies

1. phpcs
2. phpcbf
3. jshint (global nodejs package)
4. jscs-fixer (global nodejs package)
5. jscs (global nodejs package)
7. pep8
8. autopep8
9. pylint
10. csscomb

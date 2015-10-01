# Codestyle checker

This script checks and auto fixes codestyle for all supported languages:

1. PHP (phpcs)
2. Python (pep8 and pylint)
3. Javascript (jscs and jshint)

## Dependenties

1. phpcs
2. phpcbf
2. jshint (global nodejs package)
2. jscs-fixer (global nodejs package)
3. jscs (global nodejs package)
4. pep8
5. pylint

## Usage

```
usage: codestyle.py [-h] [--fix] [--verbose] target [target ...]

Check and fix code style

positional arguments:
  target      files for the checking

optional arguments:
  -h, --help  show this help message and exit
  --fix       Auto fix codestyle errors
  --verbose   Show verbose output
```
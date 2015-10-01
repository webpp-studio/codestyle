# Codestyle checker

This script checks and auto fixes codestyle for all supported languages:

1. PHP (phpcs)
2. Python (pep8 and pylint)
3. Javascript (jscs and jshint)

## Dependencies

1. phpcs
2. phpcbf
3. jshint (global nodejs package)
4. jscs-fixer (global nodejs package)
5. jscs (global nodejs package)
7. pep8
8. autopep8
9. pylint

## Usage

```
usage: codestyle.py [-h] [--fix] [--verbose] target [target ...]

Check and fix code style

positional arguments:
  target      files for the checking

optional arguments:
  -h, --help  show this help message and exit
  --try-fix       Auto fix codestyle errors
  --verbose   Show verbose output
```

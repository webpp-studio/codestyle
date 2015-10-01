# Codestyle checker

This script checks and auto fixes codestyle for all supported languages:

1. PHP (phpcs)
2. Python (pep8 and pylint)
3. Javascript (jscs and jshint)

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
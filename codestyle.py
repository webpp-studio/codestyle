#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import argparse

from checkers import *  # NOQA

LANGUAGE_MAP = {
    '.php': PHPChecker(),
    '.py': PythonChecker(),
    '.js': JSChecker(),
    '.html': HTMLChecker(),
    '.css': CSSChecker(),
}


def process_file(path, verbose=False):
    file, ext = os.path.splitext(path)
    if ext in LANGUAGE_MAP:
        checker = LANGUAGE_MAP[ext]
        sys.stdout.write("Checking: " + path + "...")
        result = checker.check_file(path)
        if result.is_success():
            print(" OK")
        else:
            print(" Fail")
            if verbose:
                print(result.output, file=sys.stderr)
    else:
        result = None
    return result


def main():
    parser = argparse.ArgumentParser(description='Check and fix code style')
    parser.add_argument('target', metavar='target', type=str, nargs='+',
                        help='files for the checking')
    parser.add_argument('--fix', dest='fix', action='store_true',
                        help='Auto fix codestyle errors', default=False)
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Show verbose output', default=False)

    args = parser.parse_args()
    files = args.target

    total_ok = 0
    total_failed = 0

    for filename in files:
        if not os.path.exists(filename):
            print(
                "%s: no such file or directory: %s" %
                (sys.args[0], filename),
                file=sys.stderr
            )
            sys.exit(1)

        elif os.path.isfile(filename):
            result = process_file(filename, args.verbose)
            if result:
                if result.is_success():
                    total_ok += 1
                else:
                    total_failed += 1

        elif os.path.isdir(filename):
            for root, subdirs, files in os.walk(filename):
                for subfile in files:
                    result = process_file(os.path.join(root, subfile),
                                          args.verbose)
                    if result:
                        if result.is_success():
                            total_ok += 1
                        else:
                            total_failed += 1

    print("Total success: " + str(total_ok))
    print("Total failed: " + str(total_failed))

    if total_failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()

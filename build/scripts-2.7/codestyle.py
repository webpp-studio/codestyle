#!/usr/bin/python

from __future__ import print_function

import os
import sys
import argparse

from checkers import *  # NOQA


class Application:
    """Codestyle checker application"""

    LANGUAGE_MAP = {
        '.php': PHPChecker(),
        '.py': PythonChecker(),
        '.js': JSChecker(),
    }

    def __init__(self):
        self.args = {}
        self.files = []
        self.verbose = False

    def log(self, string, newline=True, file=sys.stdout):
        if newline:
            string += '\n'
        file.write(string)

    def log_error(self, string, newline=True):
        self.log(string, newline, sys.stderr)

    def process_file(self, path, verbose=False):
        """Process file to check or keep it"""

        file, ext = os.path.splitext(path)
        if ext in self.LANGUAGE_MAP:
            checker = self.LANGUAGE_MAP[ext]
            self.log("Checking: " + path + "...", False)
            result = checker.check_file(path)
            if result.is_success():
                self.log(" OK")
            else:
                self.log(" Fail")
                if self.verbose:
                    self.log_error(result.output)
                if self.args.fix:
                    self.log("Trying fix errors...")
                    try:
                        result = checker.fix(path)
                    except NotImplementedError:
                        self.log_error(
                            "Auto fixing is not supported for this language"
                        )
                    else:
                        if result:
                            self.log("Some errors has been fixed")
                        else:
                            self.log("No fixable errors found")
                    self.log("")
        else:
            result = None
        return result

    def parse_args(self):
        """Parse command line argument and save it"""

        parser = argparse.ArgumentParser(description='Check and fix code style')
        parser.add_argument('target', metavar='target', type=str, nargs='+',
                            help='files for the checking')
        parser.add_argument('--try-fix', dest='fix', action='store_true',
                            help='Auto fix codestyle errors', default=False)
        parser.add_argument('--verbose', dest='verbose', action='store_true',
                            help='Show verbose output', default=False)
        parser.add_argument('--standard', dest='standard', type=str, nargs='?',
                            help='Name of coding standard directory',
                            default='default')

        self.args = parser.parse_args()
        self.files = self.args.target
        self.verbose = self.args.verbose

    def run(self):
        """Run code checking"""

        self.parse_args()

        total_ok = 0
        total_failed = 0

        for filename in self.files:
            if not os.path.exists(filename):
                self.log_error(
                    "%s: no such file or directory: %s" %
                    (sys.args[0], filename),
                )
                sys.exit(1)
            elif os.path.isfile(filename):
                result = self.process_file(filename, self.args.verbose)
                if result:
                    if result.is_success():
                        total_ok += 1
                    else:
                        total_failed += 1
            elif os.path.isdir(filename):
                for root, subdirs, files in os.walk(filename):
                    for subfile in files:
                        result = self.process_file(os.path.join(root, subfile),
                                                   self.args.verbose)
                        if result:
                            if result.is_success():
                                total_ok += 1
                            else:
                                total_failed += 1
        self.log( "Total success: %d" % total_ok)
        self.log("Total failed: %s" % total_failed)
        if total_failed > 0:
            return False
        return True


if __name__ == "__main__":
    app = Application()
    is_success = app.run()
    if is_success:
        sys.exit(1)

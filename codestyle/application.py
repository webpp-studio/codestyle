#!/usr/bin/env python
"""
Code style checker application
"""
from __future__ import absolute_import
from builtins import str
from builtins import object

import os
import sys
import argparse
import fnmatch
import re
from configparser import ConfigParser

from .utils import check_external_deps, DependencyError
from . import checkers
from . import settings


class Application(object):
    """
    Codestyle checker application class
    """

    # Checker classmap
    CHECKERS = (
        ('.php', checkers.PHPChecker),
        ('.js', checkers.JSChecker),
        ('.py', checkers.PythonChecker),
        (('.css', '.less'), checkers.LessChecker),
        ('.html', checkers.HTMLChecker),
    )

    def __init__(self):
        self.settings = settings
        self.parameters_namespace = argparse.Namespace(
            standard=self.settings.DEFAULT_STANDARD_DIR)
        self.checkers = None
        self.excludes = '$.'
        self.argument_parser = argparse.ArgumentParser(
            description=str(self.__doc__))
        self.config_parser = ConfigParser()

        self._add_arguments()
        self.parse_cmd_args(self._get_config_parser_cmd_arguments())
        self.parse_cmd_args()

    def _add_arguments(self) -> None:
        self.argument_parser.add_argument(
            'target', metavar='target', type=str, nargs='+',
            help='files for a checking'
        )
        self.argument_parser.add_argument(
            '-i', '--fix', dest='fix', action='store_true',
            help='auto fix codestyle errors if possible', default=False
        )
        self.argument_parser.add_argument(
            '-c', '--compact', dest='compact', action='store_true',
            help='Show a compact output', default=False
        )
        self.argument_parser.add_argument(
            '-l', '--language', dest='language', type=str,
            help='force set the language for a checking',
            metavar='language name', default=None
        )
        self.argument_parser.add_argument(
            '-x', '--exclude', dest='exclude', type=str,
            help='Exclude paths/files from checking', metavar='glob pattern',
            nargs='+', default=tuple()
        )
        self.argument_parser.add_argument(
            '-q', '--quiet', dest='quiet', action='store_true', default=False,
            help='Quiets "Processing" message and warnings'
        )

    @staticmethod
    def _argument_parser_bool_arguments() -> tuple:
        return 'fix', 'compact', 'quiet'

    def _get_config_parser_cmd_arguments(self) -> list:
        """Parse project's .ini file with arguments and return it"""
        cmd_arguments = []
        if self.settings.PROJECT_INITIALIZATION_PATH.is_file():
            self.config_parser.read(
                str(self.settings.PROJECT_INITIALIZATION_PATH))
        if 'parameters' not in self.config_parser:
            return []
        parameters = self.config_parser['parameters']
        for parameter_name in parameters:
            if not parameters[parameter_name]:
                continue
            parameter = f'--{parameter_name}'
            parameter_value = parameters[parameter_name].strip()
            if parameter_name in Application._argument_parser_bool_arguments():
                cmd_argument = []
                if parameter_value == 'True':
                    cmd_argument.append(parameter)
            else:
                cmd_argument = [parameter_value] + parameter_value.split(' ')
            cmd_arguments += cmd_argument
        return cmd_arguments

    def create_checkers(self):
        """
        Create checker instances for extensions
        """

        self.checkers = {}
        for ext, checker_class in self.CHECKERS:
            if not issubclass(checker_class, checkers.BaseChecker):
                raise TypeError('expected BaseChecker subclass')
            checker_instance = checker_class(application=self)
            if isinstance(ext, (list, tuple)):
                for ex in ext:
                    self.checkers[ex] = checker_instance
            else:
                self.checkers[ext] = checker_instance

    def get_checkers(self):
        """
        Get all checker instances for extensions
        """

        if self.checkers is None:
            self.create_checkers()
        return self.checkers

    def get_checker(self, ext):
        """
        Get checker instance by extension
        """

        checkers_ = self.get_checkers()
        if self.parameters_namespace.language is not None:  # forced language
            return checkers_.get(
                f'.{self.parameters_namespace.language}', None)
        return checkers_.get(ext, None)

    def get_config_path(self, filename):
        """
        Get path of the config file by name
        """

        return os.path.join(self.get_standard_dir(), filename)

    def parse_cmd_args(self, args=None):
        """
        Get parsed command line arguments
        """
        return self.argument_parser.parse_args(
            args, namespace=self.parameters_namespace)

    def check_force_language(self, language):
        """
        Check for selected language
        """

        if language is None:
            return
        checker_map = self.get_checkers()
        ext = '.' + language.lower()
        if ext not in checker_map:
            self.exit_with_error(
                "Unsupported language: %s\n"
                "Supported extensions: %s" % (
                    language,
                    ', '.join([k for k in list(checker_map.keys())])
                )
            )

    def get_standard_dir(self):
        """
        Get a path of a coding standard directory
        """

        return self.parameters_namespace.standard

    def log(self, string, newline=True, buf=sys.stdout):
        """
        Log a message to the STDOUT
        """

        if newline:
            string += '\n'
        buf.write(string)

    def log_error(self, string, newline=True):
        """
        Log an error message to the STDERR
        """

        self.log(string, newline, sys.stderr)

    def exit_with_error(self, message, retcode=1):
        """
        Put an error message to the STDERR and exit
        """

        self.log_error("%s: %s" % (sys.argv[0], message))
        sys.exit(retcode)

    def process_file(self, path):
        """
        Process a file (to check or pass it)
        """

        checker = self.get_checker(os.path.splitext(path)[1])
        if checker is None:
            return None

        if self.parameters_namespace.compact:
            self.log("Processing: " + path + "...", False)
        elif not self.parameters_namespace.quiet:
            self.log("Processing: " + path + "...")

        result = None

        if self.parameters_namespace.fix:
            try:
                result = checker.fix(path)
                if self.parameters_namespace.compact:
                    if result.is_success():
                        self.log("Some errors has been fixed\n")
                    else:
                        self.log("No errors has been fixed\n")
            except NotImplementedError:
                self.log_error(
                    "Auto fixing is not supported for this language\n"
                )
        else:
            result = checker.check(path)
            if self.parameters_namespace.compact:
                if result.is_success():
                    self.log(" Done")
                else:
                    self.log(" Fail")
            else:
                if result.output and not self.parameters_namespace.quiet:
                    self.log("\n")

        return result

    def process_dir(self, path):
        """
        Check code in directory (recursive)
        """

        for root, dirs, files in os.walk(path):
            # Exclude dirs
            dirs[:] = [d for d in dirs if not re.match(
                self.excludes, os.path.join(root, d))]
            # Exclude files
            files = [os.path.join(root, f) for f in files]
            files = [f for f in files if not re.match(self.excludes, f)]
            for file in files:
                yield self.process_file(file)

    def process_path(self, path):
        """
        Check file or directory (recursive)
        """

        if not os.path.exists(path):
            self.exit_with_error("No such file or directory: " + path)
        elif os.path.isfile(path):
            if not re.match(self.excludes, path):
                yield self.process_file(path)
        elif os.path.isdir(path):
            for result in self.process_dir(path):
                yield result

    def run(self):
        """
        Run a code checking
        """

        self.parameters_namespace = self.parse_cmd_args()
        self.check_force_language(self.parameters_namespace.language)
        excludes = []
        for exclude in self.parameters_namespace.exclude:
            excludes.append(fnmatch.translate(exclude))
        self.excludes = r'|'.join(excludes) or r'$.'

        self.log("Checking external dependencies....")

        try:
            check_external_deps()
        except DependencyError as ex:
            self.log_error(str(ex))
            sys.exit(1)

        total_success = 0
        total_failed = 0

        for path in self.parameters_namespace.target:
            for result in self.process_path(path):
                if result is None:
                    continue
                if result.is_success():
                    total_success += 1
                else:
                    total_failed += 1

        self.log("Total success: %d" % total_success)
        self.log("Total failed: %s" % total_failed)

        if total_failed > 0:
            sys.exit(1)
        sys.exit()


if __name__ == "__main__":
    Application().run()

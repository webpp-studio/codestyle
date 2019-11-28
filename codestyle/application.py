#!/usr/bin/env python
# coding: utf-8
"""Code style checker application."""
from __future__ import absolute_import

import argparse
import fnmatch
import os
import re
import sys
from builtins import object, str
from configparser import ConfigParser

from codestyle.settings import DEFAULT_STANDARD_DIR  # noqa
from codestyle.settings import PROJECT_INITIALIZATION_PATH  # noqa

from . import checkers, settings
from .utils import DependencyError, check_external_deps


class Application(object):
    """Codestyle checker application class."""

    # Checker classmap
    CHECKERS = (
        ('.php', checkers.PHPChecker),
        (('.js', '.vue', '.ts', '.coffee'), checkers.JSChecker),
        ('.py', checkers.PythonChecker),
        (('.css', '.less'), checkers.LessChecker),
        ('.html', checkers.HTMLChecker),
    )

    def __init__(self):
        """Init Application with attributes."""
        self.settings = settings
        self.parameters_namespace = argparse.Namespace(
            standard=self.settings.DEFAULT_STANDARD_DIR)
        self.checkers = None
        self.excludes = '$.'
        self.argument_parser = argparse.ArgumentParser(
            description=str(self.__doc__))
        self.boolean_arguments = None
        self.config_parser = ConfigParser()

        self._add_arguments()

    def _add_arguments(self) -> None:
        """Declare ArgumentParser's arguments."""
        self.boolean_arguments = 'fix', 'compact', 'quiet'
        self.argument_parser.add_argument(
            'target', metavar='target', type=str, nargs='+',
            help='files for a checking',
        )
        self.argument_parser.add_argument(
            '-i', '--fix', dest='fix', action='store_true',
            help='auto fix codestyle errors if possible', default=False,
        )
        self.argument_parser.add_argument(
            '-c', '--compact', dest='compact', action='store_true',
            help='Show a compact output', default=False,
        )
        self.argument_parser.add_argument(
            '-s', '--standard', dest='standard', type=str,
            help='A path to a coding standard directory',
            default=DEFAULT_STANDARD_DIR, metavar='standard-dir',
        )
        self.argument_parser.add_argument(
            '-l', '--language', dest='language', type=str,
            help='force set the language for a checking',
            metavar='language name', default=None,
        )
        self.argument_parser.add_argument(
            '-x', '--exclude', dest='exclude', type=str,
            help='Exclude paths/files from checking', metavar='glob pattern',
            nargs='+', default=(),
        )
        self.argument_parser.add_argument(
            '-q', '--quiet', dest='quiet', action='store_true', default=False,
            help='Quiets "Processing" message and warnings',
        )

    def _build_config_parser_cli_arguments(self) -> list:
        """
        Iterate ConfigParser's parameters.

        return: list view as CLI arguments.
        """
        cli_arguments = []
        parameters = self.get_config_parser_parameters()
        target_arguments = parameters.pop(
            'target', str(PROJECT_INITIALIZATION_PATH.parent)).split(' ')
        for parameter_name in parameters.keys():
            if parameter_name in self.boolean_arguments:
                cli_argument = []
                if parameters[parameter_name] == 'true':
                    cli_argument.extend(f'--{parameter_name}')
            else:
                parameter_value = parameters[parameter_name]
                cli_argument = [parameter_value] + parameter_value.split(' ')
            cli_arguments.extend(cli_argument)
        cli_arguments.extend(target_arguments)
        return cli_arguments

    def _build_parameters_data(self) -> dict:
        """Extract ConfigParser's non empty parameters."""
        parameters_data = {}
        parameters = self.config_parser['parameters']
        for parameter_name in filter(None, self.config_parser['parameters']):
            parameters_data.update({
                parameter_name.lower(): parameters[parameter_name].strip(),
            })
        return parameters_data

    def get_config_parser_parameters(self) -> dict:
        """Read project's initialization file and return parameters."""
        if self.settings.PROJECT_INITIALIZATION_PATH.is_file():
            self.config_parser.read(PROJECT_INITIALIZATION_PATH)
        if 'parameters' not in self.config_parser:
            return {}
        return self._build_parameters_data()

    def create_checkers(self):
        """Create checker instances for extensions."""
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
        """Get all checker instances for extensions."""
        if self.checkers is None:
            self.create_checkers()
        return self.checkers

    def get_checker(self, extension):
        """Get checker instance by extension."""
        checkers_data = self.get_checkers()
        if self.parameters_namespace.language:  # forced language
            return checkers_data.get(
                f'.{self.parameters_namespace.language}', None)
        return checkers_data.get(extension, None)

    def get_config_path(self, filename):
        """Get path of the config file by name."""
        return os.path.join(self.get_standard_dir(), filename)

    def parse_cmd_args(self, args=None):
        """Get parsed command line arguments."""
        return self.argument_parser.parse_args(
            args, namespace=self.parameters_namespace)

    def check_force_language(self, language):
        """Check for selected language."""
        if language is None:
            return
        checker_map = self.get_checkers()
        ext = '.' + language.lower()
        if ext not in checker_map:
            self.exit_with_error(
                f'Unsupported language: {language}\n'
                'Supported extensions: '
                f'{", ".join([k for k in list(checker_map.keys())])}',
                )

    def get_standard_dir(self):
        """Get a path of a coding standard directory."""
        return self.parameters_namespace.standard

    def log(self, string, newline=True, buf=sys.stdout):
        """Log a message to the STDOUT."""
        if newline:
            string += '\n'
        buf.write(string)

    def log_error(self, string, newline=True):
        """Log an error message to the STDERR."""
        self.log(string, newline, sys.stderr)

    def exit_with_error(self, message, retcode=1):
        """Put an error message to the STDERR and exit."""
        self.log_error(f'{sys.argv[0]}: {message}')
        sys.exit(retcode)

    def process_file(self, path):
        """Process a file (to check or pass it)."""
        checker = self.get_checker(os.path.splitext(path)[1])
        if checker is None:
            return None

        if self.parameters_namespace.compact:
            self.log('Processing: ' + path + '...', False)
        elif not self.parameters_namespace.quiet:
            self.log('Processing: ' + path + '...')

        result = None

        if self.parameters_namespace.fix:
            try:
                result = checker.fix(path)
                if self.parameters_namespace.compact:
                    if result.is_success():
                        self.log('Some errors has been fixed\n')
                    else:
                        self.log('No errors has been fixed\n')
            except NotImplementedError:
                self.log_error(
                    'Auto fixing is not supported for this language\n',
                )
        else:
            result = checker.check(path)
            if self.parameters_namespace.compact:
                if result.is_success():
                    self.log(' Done')
                else:
                    self.log(' Fail')
            else:
                if result.output and not self.parameters_namespace.quiet:
                    self.log('\n')

        return result

    def process_dir(self, path):
        """Check code in directory (recursive)."""
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
        """Check file or directory (recursive)."""
        if not os.path.exists(path):
            self.exit_with_error('No such file or directory: ' + path)
        elif os.path.isfile(path):
            if not re.match(self.excludes, path):
                yield self.process_file(path)
        elif os.path.isdir(path):
            for result in self.process_dir(path):
                yield result

    def run(self):
        """Run a code checking."""
        self.params = self.parse_cmd_args()
        self.check_force_language(self.params.language)
        self.excludes = r'|'.join(
            [fnmatch.translate(x) for x in self.params.exclude]) or r'$.'
        """
        Run a code checking
        """
        self.parse_cmd_args(self._build_config_parser_cli_arguments())
        self.parse_cmd_args()
        self.check_force_language(self.parameters_namespace.language)
        excludes = []
        for exclude in self.parameters_namespace.exclude:
            excludes.append(fnmatch.translate(exclude))
        self.excludes = r'|'.join(excludes) or r'$.'

        self.log('Checking external dependencies....')

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

        self.log(f'Total success: {total_success}')
        self.log(f'Total failed: {total_failed}')

        if total_failed > 0:
            sys.exit(1)
        sys.exit()


if __name__ == '__main__':
    Application().run()

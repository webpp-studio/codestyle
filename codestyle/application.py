#!/usr/bin/env python
"""Code style checker application."""
from __future__ import absolute_import

import argparse
import fnmatch
import glob
import os
import re
import sys
from builtins import object, str
from configparser import ConfigParser

from codestyle import checkers, settings
from codestyle.settings import (DEFAULT_STANDARD_DIR,
                                PROJECT_INITIALIZATION_PATH)
from codestyle.utils import DependencyError, check_external_deps


class Application(object):  # noqa: WPS214, WPS230, WPS338 todo fix
    """Codestyle checker application class."""

    # Checker classmap
    checkers_map = (
        ('.php', checkers.PHPChecker),
        (('.js', '.vue', '.ts', '.coffee'), checkers.JSChecker),
        ('.py', checkers.PythonChecker),
        (('.css', '.less'), checkers.LessChecker),
        ('.html', checkers.HTMLChecker),
    )

    def __init__(self):
        """Init Application with attributes."""
        self.params = None
        self.settings = settings
        self.parameters_namespace = argparse.Namespace(
            standard=self.settings.DEFAULT_STANDARD_DIR
        )
        self.checkers = None
        self.excludes = '$.'
        self.argument_parser = argparse.ArgumentParser(
            description=str(self.__doc__)
        )
        self.boolean_arguments = None
        self.config_parser = ConfigParser()

        self._add_arguments()

    def _add_arguments(self):
        """Declare ArgumentParser's arguments."""
        self.boolean_arguments = ('fix', 'compact', 'quiet')
        self.argument_parser.add_argument(
            'target',
            metavar='target',
            type=str,
            nargs='*',
            help='files for checking',
            default='.',
        )
        self.argument_parser.add_argument(
            '-i',
            '--fix',
            dest='fix',
            action='store_true',
            help='auto fix codestyle errors if possible',
            default=False,
        )
        self.argument_parser.add_argument(
            '-c',
            '--compact',
            dest='compact',
            action='store_true',
            help='Show a compact output',
            default=False,
        )
        self.argument_parser.add_argument(
            '-s',
            '--standard',
            dest='standard',
            type=str,
            help='A path to a coding standard directory',
            default=DEFAULT_STANDARD_DIR,
            metavar='standard-dir',
        )
        self.argument_parser.add_argument(
            '-l',
            '--language',
            dest='language',
            type=str,
            help='force set the language for a checking',
            metavar='language name',
            default=None,
        )
        self.argument_parser.add_argument(
            '-x',
            '--exclude',
            dest='exclude',
            type=str,
            help='Exclude paths/files from checking',
            metavar='glob pattern',
            nargs='+',
            default=(),
        )
        self.argument_parser.add_argument(
            '-q',
            '--quiet',
            dest='quiet',
            action='store_true',
            default=False,
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
            'target', str(PROJECT_INITIALIZATION_PATH.parent)
        ).split(' ')
        for parameter_name in parameters.keys():
            if parameter_name in self.boolean_arguments:
                if parameters[parameter_name] == 'true':
                    cli_arguments.append(f'--{parameter_name}')
            else:
                parameter_value = parameters[parameter_name]
                cli_arguments.append(f'--{parameter_name}={parameter_value}')
        cli_arguments.extend(target_arguments)
        return cli_arguments

    def _build_parameters_data(self, parameter: str = None) -> dict:
        """Extract ConfigParser's non empty parameters."""
        parameters_data = {}
        parameters = self.config_parser['parameters']
        if parameter and parameter in self.config_parser['parameters']:
            parameters_data.update({
                parameter.lower(): parameters[parameter].strip(),
            })
            return parameters_data

        for parameter_name in filter(None, self.config_parser['parameters']):
            parameters_data.update({
                parameter_name.lower(): self.sanitize(
                    parameters[parameter_name],
                ),
            })

        return parameters_data

    @staticmethod
    def sanitize(value: str):
        """
        Clean and sanitize input data.

        :param value: parameter value
        :return: mixed
        """
        value = value.strip()

        # String covert to boolean
        if value.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        if value.lower() in ('no', 'false', 'f', 'n', '0'):
            return False

        return value

    def get_config_parser_parameters(self, argument_name: str = None) -> dict:
        """Read project's initialization file and return parameters."""
        if self.settings.PROJECT_INITIALIZATION_PATH.is_file():
            self.config_parser.read(PROJECT_INITIALIZATION_PATH)
        if 'parameters' not in self.config_parser:
            return {}
        if argument_name:
            return self._build_parameters_data(argument_name)
        return self._build_parameters_data()

    def create_checkers(self):
        """Create checker instances for extensions."""
        self.checkers = {}
        for ext, checker_class in self.checkers_map:
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
                f'.{self.parameters_namespace.language}', None,
            )
        return checkers_data.get(extension, None)

    def get_config_path(self, filename):
        """Get path of the config file by name."""
        return os.path.join(self.get_standard_dir(), filename)

    def parse_cmd_args(self, args=None):
        """Get parsed command line arguments."""
        cli_params = self.argument_parser.parse_args(
            args, namespace=self.parameters_namespace,
        )

        self.params = self.__join_with_config_params(cli_params)

    def __join_with_config_params(self, cli_params):
        """
        Replace cli params with config file based ones.

        Cli params have more priority.
        :param cli_params:
        :return: void
        """
        config_params = self.get_config_parser_parameters()
        for param in config_params:
            # Rewrite default '.' target
            if param == 'target' and cli_params.target == ['.']:
                setattr(cli_params, param, config_params[param])

            if not getattr(cli_params, param):
                setattr(cli_params, param, config_params[param])

        return cli_params

    def check_force_language(self):
        """Check for selected language."""
        if not self.params.language:
            return
        checker_map = self.get_checkers()
        ext = '.' + self.params.language.lower()
        if ext not in checker_map:
            keys = [key for key in list(checker_map.keys())]
            self.exit_with_error(
                f'Unsupported language: {self.params.language}\n'
                'Supported extensions: '
                f'{", ".join(keys)}',
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

        if not self.parameters_namespace.quiet:
            self.log('Processing: ' + path + '...')

        result = None
        if self.parameters_namespace.fix:
            try:
                result = self.__auto_fix_errors(checker, path)
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
            elif result.output and not self.parameters_namespace.quiet:
                self.log('\n')

        return result

    def __auto_fix_errors(self, checker, path):
        result = checker.fix(path)
        if self.parameters_namespace.compact:
            res = 'Some' if result.is_success() else 'No'
            self.log(res + ' errors has been fixed\n')
        return result

    def process_dir(self, path):
        """Check code in directory (recursive)."""
        for root, _folders, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                if not re.search(self.excludes, full_path):
                    yield self.process_file(full_path)

    def process_path(self, path):
        """Check file or directory (recursive)."""
        files = glob.glob(path)
        if not files:
            self.exit_with_error(f'No such file or directory: {path}')

        for file in files:
            if os.path.isfile(file):
                if not re.match(self.excludes, file):
                    yield self.process_file(file)
            elif os.path.isdir(file):
                for result in self.process_dir(file):
                    yield result

    def run(self):
        """Run a code checking."""
        self.parse_cmd_args()

        self.check_force_language()

        self.set_excludes()

        try:
            check_external_deps()
        except DependencyError as ex:
            self.log_error(str(ex))
            sys.exit(1)

        self.check_files()

        sys.exit()

    def check_files(self):
        """
        Run file checking.

        :return:
        """
        total_success = 0
        total_failed = 0
        if isinstance(self.parameters_namespace.target, list):
            target = self.parameters_namespace.target
        else:
            target = self.parameters_namespace.target.split()

        for path in target:
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

    def set_excludes(self):
        """
        Parse excludes, translate them into regexp.

        :return: void
        """
        # Exclude from config file loads as string
        if isinstance(self.params.exclude, str):
            self.params.exclude = self.params.exclude.split(' ')

        self.excludes = r'|'.join(
            [fnmatch.translate(exclude) for exclude in self.params.exclude],
        ) or r'$.'


if __name__ == '__main__':
    Application().run()

#!/usr/bin/env python2

import os
import subprocess
from subprocess import PIPE, STDOUT
from abc import ABCMeta, abstractmethod, abstractproperty


DEVNULL = open(os.devnull, 'wb')


class BaseResult:
    """
    Base checking result
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_success(self):
        return False

    @abstractproperty
    def output(self):
        return ""

    def __bool__(self):
        return self.is_success()


class Result(BaseResult):
    """
    Code checking result
    """

    _target = ""
    _is_success = False
    _status = -1
    _output = ""

    def __init__(self, target=None, output="", status=None):
        self._target = target
        self._output = output
        self._status = int(status)
        self._is_success = True if self.status == 0 else False

    def is_success(self):
        return self._is_success

    @property
    def status(self):
        return self._status

    @property
    def output(self):
        if self._output is None:
            self._output = ""
        return self._output

    @property
    def target(self):
        return self._target


class ResultSet(BaseResult):
    """
    Set of code checking results
    """

    def __init__(self):
        self._results = []

    @property
    def results(self):
        return self._results

    def add(self, result):
        assert isinstance(result, Result)
        self._results.append(result)

    def remove(self, index):
        if index in self._results:
            self._results.remove(index)

    @property
    def output(self):
        output = ""
        for result in self.results:
            output += result.output
            if not output.endswith('\n'):
                output += '\n'
        return output

    def is_success(self):
        if len(self.results) == 0:
            return False
        is_success = True
        for result in self.results:
            if not result.is_success():
                is_success = False
                break
        return is_success


class BaseChecker(object):
    """
    Base codestyle checker
    """

    __metaclass__ = ABCMeta

    def __init__(self, application, **kwargs):
        self.application = application
        self.extra = kwargs

    @abstractproperty
    def check_commands(self):
        return []

    @property
    def fix_commands(self):
        return []

    @property
    def settings(self):
        """
        Get current application settings
        """
        return self.application.settings

    def exe(self, alias):
        """
        Get checker executable name
        """
        return self.application.settings.CHECKER_EXE[alias]

    def cfg(self, checker):
        """
        Get checker config path
        """
        return self.application.get_config_path(
            self.application.settings.CHECKER_CFG[checker]
        )

    def make_result(self, command, files):
        if not isinstance(files, (list, tuple)):
            files = (files,)
        command_args = tuple(command) + tuple(files)
        kwargs = {'stderr': STDOUT}
        if self.application.params.compact:
            kwargs['stdout'] = DEVNULL
        p = subprocess.Popen(command_args, **kwargs)
        output = p.communicate()[0]
        return Result(files, output, p.returncode)

    def check(self, files):
        results = ResultSet()
        for command in self.check_commands:
            result = self.make_result(command, files)
            results.add(result)
        return results

    def fix(self, files):
        results = ResultSet()
        for command in self.fix_commands:
            results.add(self.make_result(command, files))
        return results


class JSChecker(BaseChecker):
    """
    Javascript code checker
    """

    @property
    def check_commands(self):
        return (
            (self.exe('jscs'), '--config', self.cfg('jscs')),
            (self.exe('jshint'), '--config', self.cfg('jshint')),
        )

    @property
    def fix_commands(self):
        return (
            (self.exe('jscs'), '--fix', '--config', self.cfg('jscs')),
        )


class PHPChecker(BaseChecker):
    """
    PHP code checker
    """

    @property
    def check_commands(self):
        return (
            (self.exe('phpcs'), '--standard=' + self.cfg('phpcs')),
            # TODO: phpmd
        )

    @property
    def fix_commands(self):
        return (
            (self.exe('phpcbf'), '--standard=' + self.cfg('phpcs')),
        )


class PythonChecker(BaseChecker):
    """
    Python code checker
    """

    @property
    def check_commands(self):
        return (
            (self.exe('pep8'),),
            (self.exe('pylint'), '--report=n',
                '--rcfile=' + self.cfg('pylint')),
        )

    @property
    def fix_commands(self):
        return (
            (self.exe('autopep8'), '--in-place', '--aggressive'),
        )


class LessChecker(BaseChecker):
    """
    Less and CSS checker
    """

    @property
    def check_commands(self):
        return (
            (self.exe('csscomb'), '--lint', '--verbose',
                '--config', self.cfg('csscomb')),
        )

    @property
    def fix_commands(self):
        return (
            (self.exe('csscomb'), '--lint', '--verbose',
                '--config', self.cfg('csscomb')),
        )

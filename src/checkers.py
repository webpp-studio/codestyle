#!/usr/bin/env python2

import os
import subprocess
from subprocess import PIPE, STDOUT
from abc import ABCMeta, abstractmethod, abstractproperty

from utils import get_config_path


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


class BaseChecker:
    """
    Base codestyle checker
    """
    __metaclass__ = ABCMeta

    @property
    def cmd(self):
        return None

    @property
    def args(self):
        return []

    def check_file(self, path):
        check_extra = getattr(self, "check_extra", None)
        if callable(check_extra):
            result = check_extra(path)
            if not isinstance(result, BaseResult):
                raise BaseException(
                    'check_extra method must return a BaseResult instance'
                )
        else:
            assert self.cmd is not None
            assert isinstance(self.args, list)
            result = self.make_result(self.cmd, self.args, path)
        return result

    def make_result(self, cmd, args, path):
        popen_args = [cmd] + args + [path]
        p = subprocess.Popen(popen_args, stderr=STDOUT, stdin=PIPE,
                             stdout=PIPE)
        output = p.communicate()[0]
        return Result(path, output, p.returncode)

    def fix(self, path):
        raise NotImplementedError(
            "Auto fixing is not supported for this checker"
        )


class JSChecker(BaseChecker):
    """
    Javascript code checker
    """

    def check_extra(self, path):
        # Check for JSCS
        jscs_config_path = get_config_path('.jscsrc')
        jscs_args = []
        if jscs_config_path is not None:
            jscs_args = ['--config', jscs_config_path]
        resultset = ResultSet()
        resultset.add(self.make_result('jscs', jscs_args, path))

        # Check for JSHint
        jshint_config_path = get_config_path('.jshintrc')
        jshint_args = []
        if jshint_config_path is not None:
            jshint_args = ['--config', jshint_config_path]
        resultset.add(self.make_result('jshint', jshint_args, path))
        return resultset

    def fix(self, path):
        jscs_config_path = get_config_path('.jscsrc')
        jscs_args = ['--fix']
        if jscs_config_path is not None:
            jscs_args.append('--config')
            jscs_args.append(jscs_config_path)
        return self.make_result('jscs', jscs_args, path)


class PHPChecker(BaseChecker):
    """
    PHP code checker
    """

    def check_extra(self, path):
        # Check for PHPCS
        phpcs_config_path = get_config_path('phpcs.xml')
        phpcs_args = []
        if phpcs_config_path is not None:
            phpcs_args = ['--standard=' + phpcs_config_path]
        resultset = ResultSet()
        resultset.add(self.make_result('phpcs', phpcs_args, path))
        # TODO: PHP Mass Detector
        return resultset

    def fix(self, path):
        phpcs_config_path = get_config_path('phpcs.xml')
        if phpcs_config_path is not None:
            phpcs_args = ['--standard=' + phpcs_config_path]
        result = self.make_result('phpcbf', phpcs_args, path)
        return result


class PythonChecker(BaseChecker):
    """
    Python code checker
    """

    def check_extra(self, path):
        # Check for PEP 8
        resultset = ResultSet()
        resultset.add(self.make_result('pep8', [], path))

        # Check for PyLint
        pylintrc = get_config_path('.pylintrc')
        pylint_args = ['--report=n']
        if pylintrc is not None:
            pylint_args += ['--rcfile=' + pylintrc]
        resultset.add(self.make_result('pylint', pylint_args, path))
        return resultset

    def fix(self, path):
        result = self.make_result('autopep8',
                                  ['--in-space', '--aggresive'],
                                  path)
        return result


class LessChecker(BaseChecker):
    """
    Less and CSS checker
    """

    def check_extra(self, path):
        config_path = get_config_path('.csscombrc')
        opts = ['--lint', '--verbose']
        if config_path is not None:
            opts += ['--config', config_path]
        return self.make_result('csscomb', opts, path)

    def fix(self, path):
        config_path = get_config_path('.csscombrc')
        opts = []
        if config_path is not None:
            opts += ['--config', config_path]
        return self.make_result('csscomb', opts, path)

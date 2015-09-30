#!/usr/bin/env python2
from abc import ABCMeta, abstractmethod, abstractproperty
import subprocess
from subprocess import PIPE, STDOUT


class Result:
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
            if not isinstance(result, Result):
                raise BaseException(
                    'check_extra method must return a Result instance'
                )
        else:
            assert self.cmd is not None
            assert isinstance(self.args, list)
            popen_args = [self.cmd] + self.args + [path]
            p = subprocess.Popen(popen_args, stderr=STDOUT)
            output = p.communicate()[0]
            result = Result(path, output, p.returncode)
        return result


class CSSChecker(BaseChecker):
    """
    CSS code checker
    """

    def check_extra(self, path):
        return Result(status=1)


class HTMLChecker(BaseChecker):
    """
    HTML code checker
    """

    def check_extra(self, path):
        return Result(status=1)


class JSChecker(BaseChecker):
    """
    Javascript code checker
    """

    cmd = 'jscs'


class PHPChecker(BaseChecker):
    """
    PHP code checker
    """

    cmd = 'phpcs'


class PythonChecker(BaseChecker):
    """
    Python code checker
    """

    cmd = 'pep8'

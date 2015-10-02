"""Codestyle checker utils"""

from __future__ import absolute_import
import os
import subprocess
from subprocess import PIPE


class DependencyError(BaseException):
    """
    Raises if no some dependency found
    """

    pass


def which(program):
    """
    Get path of an executable file or None
    """

    def is_exe(fpath):
        "Check file is executable"

        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def check_external_deps():
    """
    Check external dependencies
    """

    binaries = ['npm', 'jscs', 'jshint', 'phpcs', 'phpcbf', 'csscomb']
    for binary in binaries:
        if not which(binary):
            raise DependencyError('%s is not installed' % binary)
    proc = subprocess.Popen('npm view jscs-fixer version', shell=True,
                            stdout=PIPE, stderr=PIPE)
    proc.communicate()
    if proc.returncode != 0:
        raise DependencyError('jscs-fixer is not installed')


def import_class(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

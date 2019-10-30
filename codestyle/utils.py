"""Codestyle checker utils"""
import os
from subprocess import Popen, PIPE


class DependencyError(BaseException):
    """
    Raises if no some dependency found
    """


def which(program):
    """
    Get path of an executable file or None
    """
    def is_exe(fpath):
        """
        Check file is executable
        """
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
    binaries = ['npm', 'jscs', 'jshint', 'phpcs', 'phpcbf',
                'csscomb', 'htmlcs']
    for binary in binaries:
        if not which(binary):
            raise DependencyError('%s is not installed' % binary)

    nodejs_libs = ['jscs-fixer', 'walk', 'brace-expansion']

    for nodejs_lib in nodejs_libs:
        npm_process = Popen(['npm', 'view', nodejs_lib, 'version'],
                            stdout=PIPE, stderr=PIPE)
        npm_output, npm_error = npm_process.communicate()
        if npm_error:
            message = f'{nodejs_lib} is not installed\n'
            message += f'Run npm -g install {nodejs_lib}\n'
            message += f'npm errror: {npm_error}'
            raise DependencyError(message)

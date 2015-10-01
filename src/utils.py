import os
import subprocess
from subprocess import PIPE

BASE_DIR = os.path.dirname(__file__)

CONFIG_DIRS = (
    os.path.join(BASE_DIR, 'standards'),
)


class DependencyError(BaseException):
    pass


def get_config_path(relative_path):
    path = None
    for dir_ in CONFIG_DIRS:
        abspath = os.path.join(dir_, relative_path)
        if os.path.exists(abspath):
            path = abspath
    return path


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
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
    binaries = ['npm', 'jscs', 'jshint', 'phpcs', 'phpcbf']
    for binary in binaries:
        if not which(binary):
            raise DependencyError('%s is not installed' % binary)
    p = subprocess.Popen('npm view jscs-fixer version', shell=True,
                         stdout=PIPE, stderr=PIPE)
    p.communicate()
    if p.returncode != 0:
        raise DependencyError('jscs-fixer is not installed')

import os
from ConfigParser import ConfigParser
import checkers

# Base project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Default configuration file path
DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'defaults.cfg')

# Custom user configuration file path
USER_CONFIG_FILE = os.path.expanduser('~/.config/codestyle.cfg')

_parser = ConfigParser()
_parser.read([DEFAULT_CONFIG_FILE, USER_CONFIG_FILE])

# Executable names
CHECKER_EXE = {
    'jshint': _parser.get('exe', 'jshint', 'jshint'),
    'jscs': _parser.get('exe', 'jscs', 'jscs'),
    'csscomb': _parser.get('exe', 'csscomb', 'csscomb'),
    'pylint': _parser.get('exe', 'pylint', 'pylint'),
    'pep8': _parser.get('exe', 'pep8', 'pep8'),
    'autopep8': _parser.get('exe', 'autopep8', 'autopep8'),
    'phpcs': _parser.get('exe', 'phpcs', 'phpcs'),
    'phpcbf': _parser.get('exe', 'phpcbf', 'phpcbf'),
}

# Config names for checkers
CHECKER_CFG = {
    'jshint': _parser.get('checker_cfg_name', 'jshint', '.jshintrc'),
    'jscs': _parser.get('checker_cfg_name', 'jscs', '.jscsrc'),
    'csscomb': _parser.get('checker_cfg_name', 'csscomb', '.csscombrc'),
    'phpcs': _parser.get('checker_cfg_name', 'phpcs', 'phpcs.xml'),
    'pylint': _parser.get('checker_cfg_name', 'pylint', '.pylintrc'),
}

# Default coding standard directory (with checker config files)
DEFAULT_STANDARD_DIR = _parser.get('path', 'default_standard_dir', '')
if not DEFAULT_STANDARD_DIR:
    DEFAULT_STANDARD_DIR = os.path.join(BASE_DIR, 'standards')

CHECKERS = (
    ('.php', 'checkers.PHPChecker'),
    ('.js', 'checkers.JSChecker'),
    ('.py', 'checkers.PythonChecker'),
    (('.css', '.less'), 'checkers.LessChecker')
)

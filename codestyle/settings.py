import os
from ConfigParser import ConfigParser

# Base project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Default configuration file path
DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'defaults.cfg')

# Custom user configuration file path
USER_CONFIG_FILE = os.path.expanduser('~/.config/codestyle.cfg')

parser = ConfigParser()
parser.read([DEFAULT_CONFIG_FILE, USER_CONFIG_FILE])

# Executable names
CHECKER_EXE = {
    'jshint': parser.get('exe', 'jshint', 'jshint'),
    'jscs': parser.get('exe', 'jscs', 'jscs'),
    'csscomb': parser.get('exe', 'csscomb', 'csscomb'),
    'pylint': parser.get('exe', 'pylint', 'pylint'),
    'pep8': parser.get('exe', 'pep8', 'pep8'),
    'autopep8': parser.get('exe', 'autopep8', 'autopep8'),
    'phpcs': parser.get('exe', 'phpcs', 'phpcs'),
    'phpcbf': parser.get('exe', 'phpcbf', 'phpcbf'),
    'htmlcs': parser.get('exe', 'htmlcs', 'htmlcs'),
}

# Config names for checkers
CHECKER_CFG = {
    'jshint': parser.get('checker_cfg_name', 'jshint', 'jshint.json'),
    'jscs': parser.get('checker_cfg_name', 'jscs', 'jscs.json'),
    'csscomb': parser.get('checker_cfg_name', 'csscomb', 'csscomb.json'),
    'phpcs': parser.get('checker_cfg_name', 'phpcs', 'phpcs.xml'),
    'pylint': parser.get('checker_cfg_name', 'pylint', 'pylintrc'),
    'htmlcs': parser.get('checker_cfg_name', 'htmlcs', 'htmlcs.json'),
}

# Default coding standard directory (with checker config files)
DEFAULT_STANDARD_DIR = parser.get('path', 'default_standard_dir', '')
if not DEFAULT_STANDARD_DIR:
    DEFAULT_STANDARD_DIR = os.path.join(BASE_DIR, 'standards')

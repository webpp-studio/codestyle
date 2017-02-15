from future import standard_library
import os
from configparser import ConfigParser
standard_library.install_aliases()

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
    'jshint': parser.get('exe', 'jshint', fallback='jshint'),
    'jscs': parser.get('exe', 'jscs', fallback='jscs'),
    'csscomb': parser.get('exe', 'csscomb', fallback='csscomb'),
    'pep8': parser.get('exe', 'pep8', fallback='pep8'),
    'autopep8': parser.get('exe', 'autopep8', fallback='autopep8'),
    'phpcs': parser.get('exe', 'phpcs', fallback='phpcs'),
    'phpcbf': parser.get('exe', 'phpcbf', fallback='phpcbf'),
    'htmlcs': parser.get('exe', 'htmlcs', fallback='htmlcs'),
    'flake8': parser.get('exe', 'flake8', fallback='flake8'),
    'autoflake': parser.get('exe', 'autoflake', fallback='autoflake'),
}

# Config names for checkers
CHECKER_CFG = {
    'jshint': parser.get('checker_cfg_name', 'jshint', fallback='jshint.json'),
    'jscs': parser.get('checker_cfg_name', 'jscs', fallback='jscs.json'),
    'csscomb': parser.get(
        'checker_cfg_name',
        'csscomb',
        fallback='csscomb.json'
    ),
    'phpcs': parser.get('checker_cfg_name', 'phpcs', fallback='phpcs.xml'),
    'htmlcs': parser.get('checker_cfg_name', 'htmlcs', fallback='htmlcs.json'),
    'flake8': parser.get('checker_cfg_name', 'flake8', fallback='flake8.conf'),
}

# Default coding standard directory (with checker config files)
DEFAULT_STANDARD_DIR = parser.get('path', 'default_standard_dir', fallback='')
if not DEFAULT_STANDARD_DIR:
    DEFAULT_STANDARD_DIR = os.path.join(BASE_DIR, 'standards')

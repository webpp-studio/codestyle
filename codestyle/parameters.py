"""
Отдельный модуль с набором параметров для ArgumentationTool.

Подробнее о параметрах:
https://docs.python.org/3/library/argparse.html#the-add-argument-method
https://pypi.org/project/ConfigArgParse/
"""
from pathlib import Path

from codestyle import __version__ as application_version
from codestyle.tool_wrappers import (ESLint, Flake8, HTMLCS, PHPCBF, PHPCS,
                                     Stylelint, TOOL_SETTINGS_PATH)

PARAMETERS: tuple = (
    (
        ('target',),
        {
            'metavar': 'target',
            'type': Path,
            'nargs': '+',
            'help': 'Путь до проверяемых файлов или директорий',
        },
    ),
    (
        ('-f', '--fix'),
        {
            'dest': 'fix',
            'action': 'store_true',
            'help': 'Исправить ошибки по возможности',
        },
    ),
    (
        ('-c', '--compact'),
        {
            'dest': 'compact',
            'action': 'store_true',
            'help': 'Включить компактный вывод процесса работы приложения',
        },
    ),
    (
        ('-q', '--quiet'),
        {
            'dest': 'quiet',
            'action': 'store_true',
            'help': 'Включить тихий режим работы приложения '
            '(показывать только ошибки)',
        },
    ),
    (
        ('-d', '--debug'),
        {
            'dest': 'debug',
            'action': 'store_true',
            'help': 'Включить режим отладки',
        },
    ),
    (
        ('-s', '--settings'),
        {
            'dest': 'settings',
            'type': Path,
            'default': TOOL_SETTINGS_PATH,
            'help': 'Путь до директории с настройками инструментов '
            f'(по умолчанию: {TOOL_SETTINGS_PATH})',
        },
    ),
    (
        ('--file_suffix',),
        {
            'dest': 'file_suffix',
            'metavar': '<file suffix>',
            'help': 'Проверяемое расширение файлов (.py, .js и так '
            'далее; по-умолчанию: все расширения)',
        },
    ),
    (
        ('-x', '--exclude'),
        {
            'dest': 'exclude',
            'metavar': '<globbing шаблон>',
            'help': 'Исключить по указанному globbing шаблону',
            'nargs': '+',
            'default': (),
        },
    ),
    (
        ('--phpcs-encoding',),
        {
            'dest': 'phpcs_encoding',
            'default': PHPCS.encoding,
            'help': 'Указание кодировки для PHP_CodeSniffer '
            f'(по-умолчанию: {PHPCS.encoding})',
        },
    ),
    (
        ('--stylelint-configuration_name',),
        {
            'dest': 'stylelint_configuration',
            'default': Stylelint.configuration_file_name,
            'help': 'Имя файла конфигурации для stylelint утилиты '
            '(по-умолчанию: '
            f'{Stylelint.configuration_file_name})',
        },
    ),
    (
        ('--phpcbf-configuration_name',),
        {
            'dest': 'phpcbf_configuration',
            'default': PHPCBF.configuration_file_name,
            'help': 'Имя файла конфигурации для phpcbf утилиты '
            '(по-умолчанию: '
            f'{PHPCBF.configuration_file_name})',
        },
    ),
    (
        ('--phpcs-configuration_name',),
        {
            'dest': 'phpcs_configuration',
            'default': PHPCS.configuration_file_name,
            'help': 'Имя файла конфигурации для phpcs утилиты '
            '(по-умолчанию: '
            f'{PHPCS.configuration_file_name})',
        },
    ),
    (
        ('--flake8-configuration_name',),
        {
            'dest': 'flake8_configuration',
            'default': Flake8.configuration_file_name,
            'help': 'Имя файла конфигурации для flake8 утилиты '
            '(по-умолчанию: '
            f'{Flake8.configuration_file_name})',
        },
    ),
    (
        ('--htmlcs-configuration_name',),
        {
            'dest': 'htmlcs_configuration',
            'default': HTMLCS.configuration_file_name,
            'help': 'Имя файла конфигурации для htmlcs утилиты '
            '(по-умолчанию: '
            f'{HTMLCS.configuration_file_name})',
        },
    ),
    (
        ('--eslint-configuration_name',),
        {
            'dest': 'eslint_configuration',
            'default': ESLint.configuration_file_name,
            'help': 'Имя файла конфигурации для cssbomb утилиты '
            '(по-умолчанию: '
            f'{ESLint.configuration_file_name})',
        },
    ),
    (
        ('-v', '--version'),
        {'action': 'version', 'version': application_version},
    ),
)

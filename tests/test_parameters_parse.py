"""Проверки модуля parameters_parse."""
from os import linesep
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, call, patch

from codestyle import __version__ as application_version
from codestyle.parameters_parse import ArgumentationTool, ParametersStorage
from codestyle.tool_wrappers import (ESLint, Flake8, HTMLCS, PHPCBF, PHPCS,
                                     Stylelint, TOOL_SETTINGS_PATH,
                                     MyPy, Black)


class TestParametersStorage(TestCase):
    """Проверка ParametersStorage."""

    def setUp(self):
        """Создание проверяемого объекта."""
        self.storage = ParametersStorage()

    def test_line_separator_with_compact(self):
        """Проверка line_separator если включен compact режим."""
        self.storage.compact = True
        self.assertEqual('', self.storage.line_separator)

    def test_line_separator_without_compact(self):
        """Проверка line_separator если выключен compact режим."""
        self.storage.compact = False
        self.assertEqual(linesep, self.storage.line_separator)

    def test_logging_level_with_debug(self):
        """Проверка logging_level с debug=True."""
        self.storage.debug = True
        self.assertEqual('DEBUG', self.storage.logging_level)

    def test_logging_level_with_quiet(self):
        """Проверка logging_level с quiet=True."""
        self.storage.quiet = True
        self.assertEqual('WARNING', self.storage.logging_level)

    def test_logging_level(self):
        """Проверка logging_level без debug и quiet."""
        self.assertEqual('INFO', self.storage.logging_level)


class TestArgumentationTool(TestCase):
    """Проверки ArgumentationTool."""

    @patch('codestyle.parameters_parse.DefaultConfigFileParser',
           new_callable=Mock)
    @patch('codestyle.parameters_parse.ParametersStorage', new_callable=Mock)
    @patch.object(
        ArgumentationTool,
        '_ArgumentationTool__define_parameters',
        new_callable=Mock,
    )
    @patch(
        'codestyle.parameters_parse.application_description', new_callable=Mock
    )
    @patch('codestyle.parameters_parse.application_name', new_callable=Mock)
    @patch.object(ArgumentationTool, 'DEFAULT_CONFIG_FILES', new_callable=Mock)
    @patch('codestyle.parameters_parse.ArgumentParser', new_callable=Mock)
    def test_init(
            self,
            mocked_parser: Mock,
            mocked_config_files: Mock,
            mocked_application_name: Mock,
            mocked_application_description: Mock,
            mocked_define_parameters: Mock,
            mocked_storage: Mock,
            mocked_config_file_parser_class: Mock,
    ):
        """Проверка инициализации."""
        mock_parse = Mock(return_value=('storage', 'unknown arguments'))
        mocked_parser.return_value = Mock(parse_known_args=mock_parse)

        ArgumentationTool()

        self.assertEqual(True, mocked_parser.called)
        self.assertEqual(1, mocked_parser.call_count)
        args, kwargs = mocked_parser.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual(
            {
                'add_env_var_help': False,
                'default_config_files': mocked_config_files,
                'prog': mocked_application_name,
                'description': mocked_application_description,
                'config_file_parser_class': mocked_config_file_parser_class,
            },
            kwargs,
        )

        self.assertEqual(True, mocked_define_parameters.called)
        self.assertEqual(1, mocked_define_parameters.call_count)
        args, kwargs = mocked_define_parameters.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mock_parse.called)
        self.assertEqual(1, mock_parse.call_count)
        args, kwargs = mock_parse.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual(
            {'namespace': mocked_storage.return_value}, kwargs
        )

    @patch('codestyle.parameters_parse.ParametersStorage', new=Mock())
    @patch('codestyle.parameters_parse.ArgumentParser', new_callable=Mock)
    def test_define_parameters(self, mocked_parser: Mock):
        """Проверка добавления параметров."""
        mock_add_argument = Mock()
        mocked_parser.return_value = Mock(
            add_argument=mock_add_argument,
            parse_known_args=Mock(return_value=(Mock(), Mock())),
        )

        ArgumentationTool()

        self.assertEqual(True, mock_add_argument.called)
        self.assertEqual(18, mock_add_argument.call_count)
        parameter_calls = [
            call(
                'target',
                help='Путь до проверяемых файлов или директорий',
                metavar='target',
                nargs='+',
                type=Path,
            ),
            call(
                '-f',
                '--fix',
                action='store_true',
                dest='fix',
                help='Исправить ошибки по возможности',
            ),
            call(
                '-c',
                '--compact',
                action='store_true',
                dest='compact',
                help='Включить компактный вывод процесса работы приложения',
            ),
            call(
                '-q',
                '--quiet',
                action='store_true',
                dest='quiet',
                help='Включить тихий режим работы приложения '
                     '(показывать только ошибки)',
            ),
            call(
                '-d',
                '--debug',
                action='store_true',
                dest='debug',
                help='Включить режим отладки',
            ),
            call(
                '-s',
                '--settings',
                default=TOOL_SETTINGS_PATH,
                dest='settings',
                help=f'Путь до директории с настройками инструментов '
                     f'(по умолчанию: {TOOL_SETTINGS_PATH})',
                type=Path,
            ),
            call(
                '--file_suffix',
                dest='file_suffix',
                help='Проверяемое расширение файлов (.py, .js и так '
                     'далее; по-умолчанию: все расширения)',
                metavar='<file suffix>',
            ),
            call(
                '-x',
                '--exclude',
                default=(),
                dest='exclude',
                help='Исключить по указанному globbing шаблону',
                metavar='<globbing шаблон>',
                nargs='+',
            ),
            call(
                '--phpcs-encoding',
                default=PHPCS.encoding,
                dest='phpcs_encoding',
                help=f'Указание кодировки для PHP_CodeSniffer '
                     f'(по-умолчанию: {PHPCS.encoding})',
            ),
            call(
                '--stylelint-configuration_name',
                default=Stylelint.configuration_file_name,
                dest='stylelint_configuration',
                help=f'Имя файла конфигурации для stylelint утилиты '
                     f'(по-умолчанию: {Stylelint.configuration_file_name})',
            ),
            call(
                '--phpcbf-configuration_name',
                default=PHPCBF.configuration_file_name,
                dest='phpcbf_configuration',
                help=f'Имя файла конфигурации для phpcbf утилиты '
                     f'(по-умолчанию: {PHPCBF.configuration_file_name})',
            ),
            call(
                '--phpcs-configuration_name',
                default=PHPCS.configuration_file_name,
                dest='phpcs_configuration',
                help=f'Имя файла конфигурации для phpcs утилиты '
                     f'(по-умолчанию: {PHPCS.configuration_file_name})',
            ),
            call(
                '--flake8-configuration_name',
                default=Flake8.configuration_file_name,
                dest='flake8_configuration',
                help=f'Имя файла конфигурации для flake8 утилиты '
                     f'(по-умолчанию: {Flake8.configuration_file_name})',
            ),
            call(
                '-m',
                '--mypy',
                action='store_true',
                dest=MyPy.optional_flag,
                help='Имя файла конфигурации для mypy утилиты '
                     '(по-умолчанию: '
                     f'{MyPy.configuration_file_name})',
            ),
            call(
                '-b',
                '--black',
                action='store_true',
                dest=Black.optional_flag,
                help='Имя файла конфигурации для mypy утилиты '
                     '(по-умолчанию: '
                     f'{Black.configuration_file_name})',
            ),

            call(
                '--htmlcs-configuration_name',
                default=HTMLCS.configuration_file_name,
                dest='htmlcs_configuration',
                help=f'Имя файла конфигурации для htmlcs утилиты '
                     f'(по-умолчанию: {HTMLCS.configuration_file_name})',
            ),
            call(
                '--eslint-configuration_name',
                default=ESLint.configuration_file_name,
                dest='eslint_configuration',
                help=f'Имя файла конфигурации для cssbomb утилиты '
                     f'(по-умолчанию: {ESLint.configuration_file_name})',
            ),
            call(
                '-v',
                '--version',
                action='version',
                version=application_version,
            ),
        ]

        for parameter_call in parameter_calls:
            self.assertIn(parameter_call, mock_add_argument.mock_calls)

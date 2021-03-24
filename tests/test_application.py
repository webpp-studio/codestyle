"""Проверки модуля application."""
from logging import ERROR, INFO
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, call, patch

from codestyle.application import ConsoleApplication
from codestyle.system_wrappers import ExitCodes


MOCK_TEST_FILE = '/code/test_dir/test_file.py'


class TestConsoleApplication(TestCase):
    """Проверки консольного приложения."""

    @patch.object(ConsoleApplication, 'logger', new_callable=Mock)
    @patch('codestyle.application.MESSAGES', new_callable=Mock)
    @patch('codestyle.application.ExpandedPathTree', new_callable=Mock)
    @patch.object(
        ConsoleApplication, 'get_file_suffix_tools', new_callable=Mock
    )
    def test_init_with_fix__method(
        self,
        mocked_file_suffix_tools_getter: Mock,
        mocked_tree: Mock,
        mocked_messages: Mock,
        mocked_logger: Mock,
    ):
        """Проверка инициализации с fix методом."""
        mock_parameters_storage = Mock(
            target=(MOCK_TEST_FILE,),
            fix=True,
            exclude=('/code/test_dir/test_exclude.py',),
        )

        mock_get_item = Mock()
        mocked_messages.__getitem__ = mock_get_item

        mock_debug_logger = Mock()
        mocked_logger.debug = mock_debug_logger

        ConsoleApplication(mock_parameters_storage)

        self.assertEqual(True, mocked_file_suffix_tools_getter.called)
        self.assertEqual(1, mocked_file_suffix_tools_getter.call_count)
        args, kwargs = mocked_file_suffix_tools_getter.call_args
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mock_debug_logger.called)
        self.assertEqual(2, mock_debug_logger.call_count)
        self.assertIn(
            call('Разворачивание дерева файлов и директорий...'),
            mock_debug_logger.mock_calls,
        )
        self.assertIn(
            call('Определение метода обработки файлов...'),
            mock_debug_logger.mock_calls,
        )

        self.assertEqual(True, mocked_tree.called)
        self.assertEqual(1, mocked_tree.call_count)
        args, kwargs = mocked_tree.call_args
        self.assertTupleEqual((MOCK_TEST_FILE,), args)
        self.assertDictEqual(
            {'excludes': ('/code/test_dir/test_exclude.py',)}, kwargs
        )

        self.assertEqual(True, mock_get_item.called)
        self.assertEqual(1, mock_get_item.call_count)
        args, kwargs = mock_get_item.call_args
        self.assertTupleEqual(('fix',), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(ConsoleApplication, 'logger', new=Mock(autospec=True))
    @patch('codestyle.application.MESSAGES', new_callable=Mock)
    @patch('codestyle.application.ExpandedPathTree', new=Mock(autospec=True))
    @patch.object(ConsoleApplication, 'get_file_suffix_tools', new=Mock)
    def test_init_with_check_method(self, mocked_messages: Mock):
        """Проверка инициализации с check методом."""
        mock_get_item = Mock()
        mocked_messages.__getitem__ = mock_get_item

        mock_parameters_storage = Mock(
            target=(MOCK_TEST_FILE,),
            fix=False,
            exclude=('/code/test_dir/test_exclude.py',),
        )

        ConsoleApplication(mock_parameters_storage)

        self.assertEqual(True, mock_get_item.called)
        self.assertEqual(1, mock_get_item.call_count)
        args, kwargs = mock_get_item.call_args
        self.assertTupleEqual(('check',), args)
        self.assertDictEqual({}, kwargs)

    @patch('codestyle.application.interrupt_program_flow', new_callable=Mock)
    @patch.object(
        ConsoleApplication,
        '_ConsoleApplication__process_file',
        new_callable=Mock,
    )
    @patch('codestyle.application.getattr', new_callable=Mock)
    @patch('codestyle.application.ExpandedPathTree', new_callable=Mock)
    @patch.object(ConsoleApplication, 'logger', new_callable=Mock)
    @patch.object(ConsoleApplication, 'get_tool', new_callable=Mock)
    @patch.object(ConsoleApplication, 'get_file_suffix_tools', new=Mock)
    def test_process_files_with_unsuccessful(
        self,
        mocked_tool: Mock,
        mocked_logger: Mock,
        mocked_tree: Mock,
        mocked_getattr: Mock,
        mocked_process_file: Mock,
        mocked_interrupt_program_flow: Mock,
    ):
        """Проверка process_files в случае неуспешной обработки."""
        mock_info_logger = Mock()
        mocked_logger.info = mock_info_logger

        test_path = Path('test.py')
        mock_iter = Mock(return_value=(path for path in [test_path]))
        mocked_tree.return_value = Mock(
            path_gen=Mock(
                return_value=Mock(__iter__=mock_iter))
        )

        mocked_process_file.return_value = Mock(is_success=False)

        mock_tool = Mock(autospec=True)
        mocked_tool.return_value = mock_tool
        mock_get = Mock(return_value=[mock_tool])
        application = ConsoleApplication(
            Mock(fix=False, target=(), exclude=())
        )
        application._ConsoleApplication__file_suffix_tools = Mock(get=mock_get)

        application.process_files()

        self.assertEqual(True, mock_info_logger.called)
        self.assertIn(
            call('Запуск обработки файлов...'), mock_info_logger.mock_calls
        )

        self.assertEqual(True, mock_iter.called)
        self.assertEqual(1, mock_iter.call_count)
        args, kwargs = mock_iter.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mock_get.called)
        self.assertEqual(1, mock_get.call_count)
        args, kwargs = mock_get.call_args
        self.assertTupleEqual(('.py', []), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_getattr.called)
        self.assertEqual(1, mocked_getattr.call_count)
        args, kwargs = mocked_getattr.call_args
        self.assertTupleEqual((mock_tool, 'check'), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_process_file.called)
        self.assertEqual(1, mocked_process_file.call_count)
        args, kwargs = mocked_process_file.call_args
        self.assertTupleEqual((test_path, mocked_getattr.return_value), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_interrupt_program_flow.called)
        self.assertEqual(1, mocked_interrupt_program_flow.call_count)
        args, kwargs = mocked_interrupt_program_flow.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual(
            {
                'status': ExitCodes.UNSUCCESSFUL,
                'log_message': '💔 Так-так-таак... Коллегам не стыдно в '
                'глаза смотреть? Необходимо поправить '
                'файлов: 1.',
                'log_level': ERROR,
            },
            kwargs,
        )

    @patch('codestyle.application.interrupt_program_flow', new_callable=Mock)
    @patch.object(
        ConsoleApplication,
        '_ConsoleApplication__process_file',
        new=Mock(return_value=Mock(is_success=True)),
    )
    @patch('codestyle.application.getattr', new=Mock(autospec=True))
    @patch.object(
        ConsoleApplication,
        'get_file_suffix_tools',
        new=Mock(return_value={'.py': [Mock(autospec=True)]}),
    )
    @patch('codestyle.application.ExpandedPathTree', new_callable=Mock)
    @patch.object(ConsoleApplication, 'logger', new=Mock(autospec=True))
    @patch.object(ConsoleApplication, 'get_tool', new=Mock)
    def test_process_files_with_success(
        self,
        mocked_tree: Mock,
        mocked_interrupt_program_flow: Mock,
    ):
        """Проверка process_files с успешным сценарием проверки."""
        mocked_tree.return_value = Mock(
            path_gen=Mock(
                return_value=Mock(
                    __iter__=Mock(
                        return_value=(path for path in [Path('test.py')])
                    )
                )
            )
        )
        ConsoleApplication(
            Mock(fix=False, target=(), exclude=())
        ).process_files()

        self.assertEqual(True, mocked_interrupt_program_flow.called)
        self.assertEqual(1, mocked_interrupt_program_flow.call_count)
        args, kwargs = mocked_interrupt_program_flow.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual(
            {
                'status': ExitCodes.SUCCESS,
                'log_message': 'Я проверил твои файлы (1 шт.), можешь '
                'не беспокоиться об их качестве. ✨ 💥',
                'log_level': INFO,
            },
            kwargs,
        )

    @patch('codestyle.application.ExpandedPathTree', new=Mock())
    @patch('codestyle.application.getLogger', new=Mock())
    @patch.object(ConsoleApplication, 'get_file_suffix_tools', new=Mock())
    def test_tool_can_process(self):
        """Проверки __tool_can_process метода в разных вариациях."""
        application = ConsoleApplication(
            Mock(autospec=True, fix=False, target=iter([]))
        )

        false_result = application._ConsoleApplication__tool_can_process(
            Mock(for_check=False, optional_flag='')
        )
        self.assertEqual(False, false_result)

        true_result = application._ConsoleApplication__tool_can_process(
            Mock(for_check=True, optional_flag='')
        )
        self.assertEqual(True, true_result)

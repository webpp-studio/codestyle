"""Проверки модуля command_line."""
from logging import WARNING
from unittest import TestCase
from unittest.mock import Mock, patch

from codestyle.command_line import run_process


class Test(TestCase):
    """Проверки функций модуля."""

    @patch('codestyle.command_line.ArgumentationTool', new_callable=Mock)
    @patch('codestyle.command_line.ConsoleApplication', new_callable=Mock)
    @patch('codestyle.command_line.get_logging_config', new_callable=Mock)
    @patch('codestyle.command_line.dictConfig', new_callable=Mock)
    def test_run_process_calls_application(
        self,
        mocked_config: Mock,
        mocked_logging_config_getter: Mock,
        mocked_application: Mock,
        mocked_argumentation_tool: Mock,
    ):
        """Проверка run_process без исключения."""
        mock_parameters_storage = Mock(
            line_separator='\n', logging_level='WARNING'
        )
        mocked_argumentation_tool.return_value = Mock(
            parameters_storage=mock_parameters_storage
        )
        mock_process_files = Mock()
        mocked_application.return_value = Mock(
            process_files=mock_process_files
        )

        result = run_process()

        self.assertEqual(None, result)

        self.assertEqual(True, mocked_argumentation_tool.called)
        self.assertEqual(1, mocked_argumentation_tool.call_count)
        args, kwargs = mocked_argumentation_tool.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_config.called)
        self.assertEqual(1, mocked_config.call_count)
        args, kwargs = mocked_config.call_args
        self.assertTupleEqual(
            (mocked_logging_config_getter.return_value,), args
        )
        self.assertDictEqual(
            {},
            kwargs,
        )

        self.assertEqual(True, mocked_logging_config_getter.called)
        self.assertEqual(1, mocked_logging_config_getter.call_count)
        args, kwargs = mocked_logging_config_getter.call_args
        self.assertTupleEqual(('\n', 'WARNING'), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_application.called)
        self.assertEqual(1, mocked_application.call_count)
        args, kwargs = mocked_application.call_args
        self.assertTupleEqual((mock_parameters_storage,), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mock_process_files.called)
        self.assertEqual(1, mock_process_files.call_count)
        args, kwargs = mock_process_files.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

    @patch('codestyle.command_line.interrupt_program_flow', new_callable=Mock)
    @patch('codestyle.command_line.ArgumentationTool', new_callable=Mock)
    @patch('codestyle.command_line.ConsoleApplication', new_callable=Mock)
    @patch('codestyle.command_line.get_logging_config', new=Mock)
    @patch('codestyle.command_line.dictConfig', new=Mock)
    def test_run_process_excepts_keyboard_interrupt(
        self,
        mocked_application: Mock,
        mocked_argumentation_tool: Mock,
        mocked_interrupt_program_flow: Mock,
    ):
        """Проверка обработки KeyboardInterrupt исключения."""
        mocked_argumentation_tool.return_value = Mock(
            parameters_storage=Mock(line_separator='\n')
        )
        mocked_application.return_value = Mock(
            process_files=Mock(side_effect=KeyboardInterrupt)
        )

        run_process()

        self.assertEqual(True, mocked_interrupt_program_flow.called)
        self.assertEqual(1, mocked_interrupt_program_flow.call_count)
        args, kwargs = mocked_interrupt_program_flow.call_args
        self.assertEqual((), args)
        self.assertDictEqual(
            {
                'status': 1,
                'log_message': 'Проверка прервана.',
                'log_level': WARNING,
            },
            kwargs,
        )

    @patch('codestyle.command_line.interrupt_program_flow', new_callable=Mock)
    @patch('codestyle.command_line.ConsoleApplication', new_callable=Mock)
    @patch('codestyle.command_line.get_logging_config', new=Mock)
    @patch('codestyle.command_line.dictConfig', new=Mock)
    @patch('codestyle.command_line.ArgumentationTool', new_callable=Mock)
    def test_run_process_does_not_excepts_any_error(
        self,
        mocked_argumentation_tool: Mock,
        mocked_application: Mock,
        mocked_interrupt_program_flow: Mock,
    ):
        """Проверка отсутствия обработки других исключений в run_process."""
        mocked_argumentation_tool.return_value = Mock(
            parameters_storage=Mock(line_separator='\n')
        )
        mocked_application.return_value = Mock(
            process_files=Mock(side_effect=KeyError)
        )

        with self.assertRaises(KeyError):
            run_process()

        self.assertEqual(False, mocked_interrupt_program_flow.called)

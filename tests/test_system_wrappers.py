"""Проверки модуля system_wrappers."""
from logging import INFO
from unittest import TestCase
from unittest.mock import Mock, call, patch

from codestyle import system_wrappers
from codestyle.system_wrappers import (
    ExitCodes,
    check_output,
    interrupt_program_flow,
)


class Test(TestCase):
    """Проверка функций модуля."""

    @patch('codestyle.system_wrappers.sys', new_callable=Mock)
    @patch.object(system_wrappers, '_logger', new_callable=Mock)
    def test_interrupt_program_flow(
        self, mocked_logger: Mock, mocked_sys: Mock
    ):
        """Проверка interrupt_program_flow."""
        mock_log = Mock()
        mocked_logger.log = mock_log

        mock_exit = Mock()
        mocked_sys.exit = mock_exit

        interrupt_program_flow(log_message='Проверка вызова функции.')

        self.assertEqual(True, mock_log.called)
        self.assertEqual(1, mock_log.call_count)
        args, kwargs = mock_log.call_args
        self.assertTupleEqual((INFO, 'Проверка вызова функции.'), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mock_exit.called)
        self.assertEqual(1, mock_exit.call_count)
        args, kwargs = mock_exit.call_args
        self.assertTupleEqual((ExitCodes.SUCCESS,), args)
        self.assertDictEqual({}, kwargs)

    @patch('codestyle.system_wrappers.check_process_output', new_callable=Mock)
    @patch.object(system_wrappers, '_logger', new_callable=Mock)
    def test_check_output(
        self, mocked_logger: Mock, mocked_process_output_checker: Mock
    ):
        """Проверка check_output."""
        mock_debug = Mock()
        mocked_logger.debug = mock_debug

        mock_rstrip = Mock()
        mock_decode = Mock(return_value=Mock(rstrip=mock_rstrip))
        mocked_process_output_checker.return_value = Mock(decode=mock_decode)

        check_output(('application', 'run'))

        self.assertEqual(True, mock_debug.called)
        self.assertEqual(1, mock_debug.call_count)
        args, kwargs = mock_debug.call_args
        self.assertTupleEqual(
            ('Проверка наличия application в системе...',), args
        )
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_process_output_checker.called)
        self.assertEqual(1, mocked_process_output_checker.call_count)
        args, kwargs = mocked_process_output_checker.call_args
        self.assertTupleEqual((('application', 'run'),), args)
        self.assertDictEqual({'timeout': 10}, kwargs)

        self.assertEqual(True, mock_decode.called)
        self.assertEqual(1, mock_decode.call_count)
        args, kwargs = mock_decode.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mock_rstrip.called)
        self.assertEqual(1, mock_rstrip.call_count)
        args, kwargs = mock_rstrip.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

    @patch(
        'codestyle.system_wrappers.interrupt_program_flow', new_callable=Mock
    )
    @patch('codestyle.system_wrappers.check_process_output', new_callable=Mock)
    @patch.object(system_wrappers, '_logger', new_callable=Mock)
    def test_check_output_with_error(
        self,
        mocked_logger: Mock,
        mocked_process_output_checker: Mock,
        mocked_interrupt_program_flow: Mock,
    ):
        """Проверка check_output с ошибкой внутри."""
        mock_debug = Mock()
        mocked_logger.debug = mock_debug

        mocked_process_output_checker.side_effect = FileNotFoundError(
            'Исполняемый файл application не найден.'
        )

        check_output(('application', 'run'))

        self.assertEqual(True, mock_debug.called)
        self.assertEqual(3, mock_debug.call_count)
        self.assertIn(
            call('Проверка наличия application в системе...'),
            mock_debug.mock_calls,
        )
        self.assertIn(
            call('Инструмент application не найден.'), mock_debug.mock_calls
        )
        self.assertIn(
            call('Исполняемый файл application не найден.'),
            mock_debug.mock_calls,
        )

        self.assertEqual(True, mocked_interrupt_program_flow.called)
        self.assertEqual(1, mocked_interrupt_program_flow.call_count)
        args, kwargs = mocked_interrupt_program_flow.call_args
        self.assertTupleEqual((ExitCodes.UNSUCCESSFUL,), args)
        self.assertDictEqual({}, kwargs)

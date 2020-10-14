"""Проверки модуля tool_wrappers."""
from os import linesep
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from codestyle.tool_wrappers import ConsoleTool, Result


class TestResult(TestCase):
    """Проверки Result."""

    def test_whole_output_without_output(self):
        """Проверка whole_output с пустым результатом."""
        result = Result(0, output='', error='error')
        self.assertEqual('error', result.whole_output)

    def test_whole_output_with_output(self):
        """Проверка whole_output с передачей результата."""
        result = Result(0, output='result', error='')
        self.assertEqual('result' + linesep, result.whole_output)


class TestConsoleTool(TestCase):
    """Проверки ConsoleTool."""

    @patch.object(ConsoleTool, 'get_name', new_callable=Mock)
    @patch('codestyle.tool_wrappers.check_output', new_callable=Mock)
    def test_init(self, mocked_check_output: Mock, mocked_get_name: Mock):
        """Проверка инициализации инструмента."""
        mocked_get_name.return_value = 'application'

        mock_path = Path('test.py')
        tool = ConsoleTool(mock_path)

        self.assertEqual(True, mocked_check_output.called)
        self.assertEqual(1, mocked_check_output.call_count)
        args, kwargs = mocked_check_output.call_args
        self.assertTupleEqual((('application', '--help'),), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_get_name.called)
        self.assertEqual(1, mocked_get_name.call_count)
        args, kwargs = mocked_get_name.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(mock_path, tool.configuration_path)

    @patch.object(ConsoleTool, 'cli_tool_name', new='tool')
    def test_get_name(self):
        """Проверка get_name."""
        self.assertEqual('tool', ConsoleTool.get_name())

    def test_get_name_without_name(self):
        """Проверка get_name без заданного имени."""
        self.assertEqual('consoletool', ConsoleTool.get_name())

    @patch.object(ConsoleTool, '_process_file', new_callable=Mock)
    @patch('codestyle.tool_wrappers.check_output', new=Mock)
    def test_check(self, mocked__process_file: Mock):
        """Проверка check."""
        path = Mock()
        ConsoleTool().check(path)

        self.assertEqual(True, mocked__process_file.called)
        self.assertEqual(1, mocked__process_file.call_count)
        args, kwargs = mocked__process_file.call_args
        self.assertTupleEqual((path, ()), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(ConsoleTool, '_process_file', new_callable=Mock)
    @patch('codestyle.tool_wrappers.check_output', new=Mock)
    def test_fix(self, mocked__process_file: Mock):
        """Проверка fix."""
        path = Mock()
        ConsoleTool().check(path)

        self.assertEqual(True, mocked__process_file.called)
        self.assertEqual(1, mocked__process_file.call_count)
        args, kwargs = mocked__process_file.call_args
        self.assertTupleEqual((path, ()), args)
        self.assertDictEqual({}, kwargs)

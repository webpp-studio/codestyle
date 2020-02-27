"""Test application."""
import argparse
import os
import unittest

import mock
# noqa
from codestyle import application, checkers, settings  # noqa


class TestApplication(unittest.TestCase):
    """Tests for codestyle.application class."""

    def setUp(self):
        """Setups for initial data."""
        self.application = application.Application()
        self.application.parameters_namespace = argparse.Namespace(
            language=None,
            standard=settings.DEFAULT_STANDARD_DIR,
        )

    def test_create_checkers(self):
        """Create checkers."""
        self.assertIsNone(self.application.checkers)
        self.application.create_checkers()
        self.assertIsInstance(self.application.checkers, dict)

        for val in list(self.application.checkers.values()):
            self.assertIsInstance(val, checkers.BaseChecker)

        self.assertGreater(len(self.application.checkers), 0)

    def test_get_checkers(self):
        """Test get_checkers."""
        self.assertIsInstance(self.application.get_checkers(), dict)

    def test_get_checker(self):
        """Test get_checker."""
        self.assertIsInstance(self.application.get_checker('.php'),
                              checkers.PHPChecker)
        self.assertIsInstance(self.application.get_checker('.js'),
                              checkers.JSChecker)

    def test_get_checker_forced_language(self):
        """Test get_checker_forced_language."""
        self.application.parameters_namespace.language = 'php'
        # force language check
        self.assertIsInstance(self.application.get_checker('.js'),
                              checkers.PHPChecker)
        self.assertIsInstance(self.application.get_checker('.php'),
                              checkers.PHPChecker)

    @mock.patch('codestyle.application.os')
    def test_get_config_path(self, mock_os):
        """Test get_config_path."""
        self.application.get_config_path('file1')
        standard_dir = self.application.get_standard_dir()
        mock_os.path.join.assert_called_with(standard_dir, 'file1')

    def test_parse_cmd_default_args(self):
        """Test parse_cmd_args with default args."""
        self.application.parse_cmd_args(['test.py'])
        self.assertEqual(
            self.application.parameters_namespace.target, ['test.py']
        )
        self.assertIsInstance(
            self.application.parameters_namespace, argparse.Namespace
        )
        self.assertFalse(self.application.parameters_namespace.compact)
        self.assertIsInstance(
            self.application.parameters_namespace.exclude, tuple
        )
        self.assertEqual(
            len(self.application.parameters_namespace.exclude), 0
        )
        self.assertIsNone(self.application.parameters_namespace.language)
        self.assertTrue(
            os.path.isdir(self.application.parameters_namespace.standard)
        )

    def test_parse_cmd_args(self):
        """Test parse_cmd_args."""
        self.application.parse_cmd_args([
            'test1.js', 'test2.html',
        ])
        self.assertEqual(self.application.parameters_namespace.target,
                         ['test1.js', 'test2.html'])

        self.application.parse_cmd_args(
            ['-i', 'test.js']
        )
        self.assertTrue(self.application.parameters_namespace.fix)
        self.application.parse_cmd_args(
            ['--fix', 'test.js'])

        self.application.parse_cmd_args(
            ['-c', 'test.js'])
        self.assertTrue(self.application.parameters_namespace.compact)
        self.application.parse_cmd_args(
            ['--compact', 'test.js'])
        self.assertTrue(self.application.parameters_namespace.compact)

        self.application.parse_cmd_args(
            ['-l', 'html', 'test.xml'])
        self.assertEqual(
            self.application.parameters_namespace.language, 'html'
        )
        self.application.parse_cmd_args(
            ['--language', 'html', 'test.xml'])
        self.assertEqual(
            self.application.parameters_namespace.language, 'html'
        )

        self.application.parse_cmd_args([
            'test.php', '-x', '/test/dir/', '*.html'],
        )
        self.assertEqual(self.application.parameters_namespace.exclude,
                         ['/test/dir/', '*.html'])
        self.application.parse_cmd_args(
            ['--exclude=/test/dir/', 'test.php'],
        )
        self.assertEqual(
            self.application.parameters_namespace.exclude, ['/test/dir/']
        )

        self.application.parse_cmd_args(
            ['-q', 'test.php']
        )
        self.assertTrue(self.application.parameters_namespace.quiet)

    def test_get_standard_dir(self):
        """Check if default standard dir exists."""
        self.assertTrue(
            os.path.exists(self.application.get_standard_dir()),
        )

    def test_log(self):
        """Test log."""
        buf_mock = mock.Mock()
        self.application.log('Hello', buf=buf_mock)
        buf_mock.write.assert_called_with('Hello\n')
        buf_mock = mock.Mock()
        self.application.log('Hello', newline=True,
                             buf=buf_mock)
        buf_mock.write.assert_called_with('Hello\n')

    @mock.patch('codestyle.application.sys.stderr')
    def test_log_error(self, stderr_mock):
        """Test log_error."""
        self.application.log_error('Hello')
        stderr_mock.write.assert_called_with('Hello\n')
        self.application.log_error('Hello', False)
        stderr_mock.write.assert_called_with('Hello')

    @mock.patch('codestyle.application.sys')
    def test_exit_with_error(self, sys_mock):
        """Test exit_with_error."""
        self.application.exit_with_error(
            'Test message',
        )
        sys_mock.exit.assert_called_with(1)
        self.application.exit_with_error(
            'Test message', 2,
        )
        sys_mock.stderr.write.assert_called_with(
            f'{sys_mock.argv[0]}: Test message\n',
        )
        sys_mock.exit.assert_called_with(2)

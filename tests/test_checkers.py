# coding: utf-8
"""Test checkers."""
import argparse
import unittest

from codestyle import application, checkers


class TestJSChecker(unittest.TestCase):
    """Test javascript code style checker."""

    def setUp(self):
        """Setups test js checker."""
        self.application = application.Application()
        self.application.parameters_namespace = argparse.Namespace(
            standard=application.settings.DEFAULT_STANDARD_DIR,
            compact=False,
            quiet=False,
        )
        self.checker = checkers.JSChecker(self.application)

    def test_get_check_commands(self):
        """Tests get_check_commands."""
        commands = self.checker.get_check_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

    def test_get_fix_commands(self):
        """Tests get_fix_commands."""
        commands = self.checker.get_fix_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))


class TestPHPChecker(unittest.TestCase):
    """Test php code style checker."""

    def setUp(self):
        """Setups test php checker."""
        self.application = application.Application()
        self.application.parameters_namespace = argparse.Namespace(
            standard=application.settings.DEFAULT_STANDARD_DIR,
            compact=False,
            quiet=False,
        )
        self.checker = checkers.PHPChecker(self.application)

    def test_get_check_commands(self):
        """Tests get_check_commands."""
        commands = self.checker.get_check_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

    def test_get_fix_commands(self):
        """Tests get_fix_commands."""
        commands = self.checker.get_fix_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))


class TestPythonChecker(unittest.TestCase):
    """Test python code style checker."""

    def setUp(self):
        """Setups python checker."""
        self.application = application.Application()
        self.application.parameters_namespace = argparse.Namespace(
            standard=application.settings.DEFAULT_STANDARD_DIR,
            compact=False,
            quiet=False,
        )
        self.checker = checkers.PythonChecker(self.application)

    def test_get_check_commands(self):
        """Tests get_check_commands."""
        commands = self.checker.get_check_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

    def test_get_fix_commands(self):
        """Tests get_fix_commands."""
        commands = self.checker.get_fix_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))


class TestCSSChecker(unittest.TestCase):
    """Test css code style checker."""

    def setUp(self):
        """Setups test css checker."""
        self.application = application.Application()
        self.application.parameters_namespace = argparse.Namespace(
            standard=application.settings.DEFAULT_STANDARD_DIR,
            compact=False,
            quiet=False,
        )
        self.checker = checkers.LessChecker(self.application)

    def test_get_check_commands(self):
        """Tests get_check_commands."""
        commands = self.checker.get_check_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

    def test_get_fix_commands(self):
        """Tests get_fix_commands."""
        commands = self.checker.get_fix_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))


class TestHTMLChecker(unittest.TestCase):
    """Test html code style checker."""

    def setUp(self):
        """Setups test html checker."""
        self.application = application.Application()
        self.application.parameters_namespace = argparse.Namespace(
            standard=application.settings.DEFAULT_STANDARD_DIR,
            compact=False,
            quiet=False,
        )
        self.checker = checkers.HTMLChecker(self.application)

    def test_get_check_commands(self):
        """Tests get_check_commands."""
        commands = self.checker.get_check_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

    def test_get_fix_commands(self):
        """Tests get_fix_commands."""
        commands = self.checker.get_fix_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

import unittest
import argparse

from codestyle import application
from codestyle import checkers
from codestyle.result import BaseResult


class TestJSChecker(unittest.TestCase):
    """
    Test javascript code style checker
    """

    def setUp(self):
        self.application = application.Application()
        self.application.params = argparse.Namespace(
            standard=application.settings.DEFAULT_STANDARD_DIR,
            compact=False
        )
        self.checker = checkers.JSChecker(self.application)

    def test_get_check_commands(self):
        commands = self.checker.get_check_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))

    def test_get_fix_commands(self):
        commands = self.checker.get_fix_commands()
        self.assertIsInstance(commands, (list, tuple))
        for command in commands:
            self.assertIsInstance(command, (list, tuple))




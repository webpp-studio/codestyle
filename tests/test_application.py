import unittest
import argparse

from codestyle import application
from codestyle import checkers


class TestApplication(unittest.TestCase):
    """
    Tests for codestyle.application class
    """

    def setUp(self):
        """
        Setup initial data
        """

        self.application = application.Application()
        self.application.params = argparse.Namespace(
            language=None
        )

    def test_create_checkers(self):
        self.assertIsNone(self.application.checkers)
        self.application.create_checkers()
        self.assertIsInstance(self.application.checkers, dict)

        for val in self.application.checkers.values():
            self.assertIsInstance(val, checkers.BaseChecker)

        self.assertGreater(len(self.application.checkers), 0)

    def test_get_checkers(self):
        self.assertIsInstance(self.application.get_checkers(), dict)

    def test_get_checker(self):
        self.assertIsInstance(self.application.get_checker('.php'),
                              checkers.PHPChecker)
        self.assertIsInstance(self.application.get_checker('.js'),
                              checkers.JSChecker)

    def test_get_checker_forced_language(self):
        setattr(self.application.params, 'language', 'php')
        # force language check
        self.assertIsInstance(self.application.get_checker('.js'),
                              checkers.PHPChecker)
        self.assertIsInstance(self.application.get_checker('.php'),
                              checkers.PHPChecker)


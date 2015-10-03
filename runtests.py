#!/usr/bin/env python
import os
import unittest

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'tests'))

if __name__ == "__main__":
    suite = unittest.TestLoader().discover(PROJECT_DIR)
    unittest.TextTestRunner(verbosity=2).run(suite)

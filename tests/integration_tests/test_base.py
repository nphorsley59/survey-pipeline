"""
This is the base for all unit tests. Any function inheriting from
unittest.TestCase or BaseCase will be run as a test.
"""


import unittest
import warnings


import pandas as pd


from app.run import run


class BaseCase(unittest.TestCase):
    """Use this class to build fixtures for the setUp and tearDown of all tests."""

    def setUp(self):
        warnings.simplefilter("ignore")

    def tearDown(self):
        pass


class SanityCheckCase(BaseCase):
    """Ensure that the OS is working correctly."""

    def test_run(self):
        self.assertIsInstance(run(), pd.DataFrame)
        self.assertTrue(run().shape[0] > 0)


if __name__ == '__main__':
    unittest.main()

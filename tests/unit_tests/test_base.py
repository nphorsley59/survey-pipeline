"""
This is the base for all unit tests. Any function inheriting from
unittest.TestCase or BaseCase will be run as a test.
"""


import os
import unittest
import warnings


import numpy as np
import pandas as pd


from app.adapters.storage import get_storage
from app.utils import (replace_substrings, subset_by_substring, split_strings,
                       get_index_for_upper_str, delete_file)
from config import Config


class BaseCase(unittest.TestCase):
    """Use this class to build fixtures for the setUp and tearDown of all tests."""

    def setUp(self):
        warnings.simplefilter("ignore")

    def tearDown(self):
        pass


class SanityCheckCase(BaseCase):
    """Ensure that the OS is working correctly."""
    def test_config(self):
        self.assertIsNotNone(Config.PROJECT_DIR)
        self.assertIsNotNone(Config.DEFAULT_STORAGE)


class UtilsTestCase(BaseCase):

    def setUp(self):
        self.df = pd.DataFrame(
            np.array([['b**ir*d', 'bird'], [2, 3]]),
            columns=['a', 'b'])
        self.test_list = ['a', 'Bb', 'CC']

    def test_replace_substrings(self):
        df = replace_substrings(self.df, 'a', '*', '')
        self.assertTrue(df['a'][0] == 'bird')

    def test_subset_by_substring(self):
        df = subset_by_substring(self.df, 'b', 'bird', keep=True)
        self.assertTrue(df.shape[0] == 1)

    def test_split_strings(self):
        df = split_strings(self.df, 'a', on='*')
        self.assertIsInstance(df['a'][0], list)

    def test_get_index_for_upper_str(self):
        i = get_index_for_upper_str(self.test_list)
        self.assertTrue(i == 2)

    def delete_file(self):
        storage = get_storage()
        path = 'data/test_assets/test_delete_file.csv'
        storage.write_file(self.df, 'data/test_assets/test_delete_file.csv')
        self.assertTrue(os.path.isfile(storage.get_path_attrs(path)[0]))
        delete_file(path)
        self.assertFalse(os.path.isfile(storage.get_path_attrs(path)[0]))


if __name__ == '__main__':
    unittest.main()

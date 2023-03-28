"""
This is the base for all unit tests. Any function inheriting from
unittest.TestCase or BaseCase will be run as a test.
"""


from datetime import date
import os
import unittest
import warnings


import numpy as np
import pandas as pd


from src.adapters.storage import get_storage
from src.utils import (replace_substrings, subset_by_substring, split_strings,
                       get_index_for_upper_str, delete_file, get_dated_fname,
                       get_path_attrs)
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
        self.test_list = ['a', 'Bb', 'CC']
        i = get_index_for_upper_str(self.test_list)
        self.assertTrue(i == 2)

    def test_delete_file(self):
        storage = get_storage()
        path = 'data/test_assets/test_delete_file.csv'
        storage.write_file(self.df, 'data/test_assets/test_delete_file.csv')
        abs_path = get_path_attrs(path)[0]
        self.assertTrue(os.path.isfile(abs_path))
        delete_file(abs_path)
        self.assertFalse(os.path.isfile(abs_path))

    def test_get_dated_fname(self):
        fname = 'example_file.txt'
        today = date.today().strftime(Config.DATETIME_FORMAT)
        dated_fname = get_dated_fname(fname)
        self.assertTrue(dated_fname == f'example_file--{today}.txt')

    def test_get_path_attrs(self):
        fname = 'example_file.txt'
        path_attrs = get_path_attrs(fname)
        self.assertTrue(Config.PROJECT_DIR in path_attrs[0])
        self.assertTrue(path_attrs[1] == '.txt')


if __name__ == '__main__':
    unittest.main()

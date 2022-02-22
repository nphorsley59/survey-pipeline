"""
Test adapters.
"""


import os
import unittest


import numpy as np
import pandas as pd


from app.adapters.storage import get_storage, LocalDirectory
from app.utils import delete_file
from tests.unit_tests import BaseCase


class GetStorageTestCase(BaseCase):
    """File path being tested: app/adapters/storage/init.py."""

    def setUp(self):
        self.adapters = {'local': LocalDirectory}

    def test_get_storage_returns_correct_adapter(self):
        for key, adapter in self.adapters.items():
            result = get_storage(storage_type=key)
            self.assertIsInstance(result, adapter)

    def test_invalid_storage_type(self):
        with self.assertRaises(ValueError):
            get_storage(storage_type='invalid')


class LocalDirectoryTestCase(BaseCase):
    """File path being tested: app/adapters/storage/local_directory.py."""

    def setUp(self):
        self.storage = LocalDirectory()
        self.path = 'data/test_assets/test_read_write'
        self.extensions = ['.csv', '.pkl', '.json', '.invalid']
        self.df = pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])

    def test_create_instance(self):
        self.assertIsInstance(self.storage, LocalDirectory)

    def test_read_file_returns_a_df(self):
        for extension in self.extensions:
            path = self.path + extension
            if extension == '.invalid':
                with self.assertRaises(KeyError):
                    self.storage.read_file(path)
            else:
                df = self.storage.read_file(path)
                self.assertIsInstance(df, pd.DataFrame)
                self.assertTrue(df.shape[0] > 0)

    def test_write_file_writes_to_folder(self):
        for extension in self.extensions:
            path = self.path + extension
            delete_file(path)
            self.assertFalse(os.path.isfile(path))
            if extension == '.invalid':
                with self.assertRaises(KeyError):
                    self.storage.write_file(self.df, path)
            else:
                self.storage.write_file(self.df, path)
                self.assertTrue(os.path.isfile(self.storage.get_path_attrs(path)[0]))


if __name__ == '__main__':
    unittest.main()

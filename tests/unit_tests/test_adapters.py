"""
Test adapters.
"""


import os
import unittest


import numpy as np
import pandas as pd


from app.adapters.storage import get_storage, LocalDirectory
from app.utils import delete_file, get_path_attrs
from tests.unit_tests import BaseCase


class GetStorageTestCase(BaseCase):
    """File path being tested: app/adapters/storage/init.py."""

    def test_get_storage_local_returns_local_directory_adapter(self):
        result = get_storage(storage_type='local')
        self.assertIsInstance(result, LocalDirectory)

    def test_invalid_storage_type(self):
        with self.assertRaises(ValueError):
            get_storage(storage_type='invalid')


class LocalDirectoryTestCase(BaseCase):
    """File path being tested: app/adapters/storage/local_directory.py."""

    def setUp(self):
        self.path = 'data/test_assets/test_read_write'
        self.df = pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])

    def test_create_instance(self):
        storage = LocalDirectory()
        self.assertIsInstance(storage, LocalDirectory)

    def read_file(self, storage, extension):
        path = self.path + extension
        if extension == '.invalid':
            with self.assertRaises(KeyError):
                storage.read_file(path)
        else:
            df = storage.read_file(path)
            self.assertIsInstance(df, pd.DataFrame)
            self.assertTrue(df.shape[0] > 0)

    def test_read_csv_returns_a_df(self):
        storage = LocalDirectory()
        self.read_file(storage=storage, extension='.csv')

    def test_read_pkl_returns_a_df(self):
        storage = LocalDirectory()
        self.read_file(storage=storage, extension='.pkl')

    def test_read_json_returns_a_df(self):
        storage = LocalDirectory()
        self.read_file(storage=storage, extension='.json')

    def test_read_invalid_extension_raises_error(self):
        storage = LocalDirectory()
        self.read_file(storage=storage, extension='.invalid')

    def write_file(self, storage, extension):
        path = self.path + extension
        delete_file(path)
        self.assertFalse(os.path.isfile(path))
        if extension == '.invalid':
            with self.assertRaises(KeyError):
                storage.write_file(self.df, path)
        else:
            storage.write_file(self.df, path)
            self.assertTrue(os.path.isfile(get_path_attrs(path)[0]))

    def test_write_csv_writes_to_path(self):
        storage = LocalDirectory()
        self.write_file(storage=storage, extension='.csv')

    def test_write_pkl_writes_to_path(self):
        storage = LocalDirectory()
        self.write_file(storage=storage, extension='.pkl')

    def test_write_json_writes_to_path(self):
        storage = LocalDirectory()
        self.write_file(storage=storage, extension='.json')

    def test_write_invalid_extension_raises_error(self):
        storage = LocalDirectory()
        self.write_file(storage=storage, extension='.invalid')


if __name__ == '__main__':
    unittest.main()

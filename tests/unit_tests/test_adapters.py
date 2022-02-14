"""
Test adapters.
"""


import os
import pandas as pd


from app.adapters.storage import get_storage, LocalDirectory
from tests.unit_tests import BaseCase


class StorageCase(BaseCase):

    def setUp(self):
        self.storage = get_storage()

    @staticmethod
    def remove_file(write_path):
        if os.path.isfile(write_path):
            os.remove(write_path)

    def test_get_storage(self):
        self.assertIsInstance(self.storage, LocalDirectory)

    def test_read_write_local_csv(self):
        # Paths
        read_path = './data/test_assets/test_read_write.csv'
        write_path = './data/test_assets/test_read_write.csv'
        # Read from storage
        df = self.storage.read_file(read_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)
        # Remove existing file
        self.remove_file(write_path)
        self.assertFalse(os.path.isfile(write_path))
        # Write to storage
        self.storage.write_file(df, write_path)
        self.assertTrue(os.path.isfile(self.storage.get_path_attrs(write_path)[0]))

    def test_read_write_local_pickle(self):
        # Paths
        read_path = './data/test_assets/test_read_write.pkl'
        write_path = './data/test_assets/test_read_write.pkl'
        # Read from storage
        df = self.storage.read_file(read_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)
        # Remove existing file
        self.remove_file(write_path)
        self.assertFalse(os.path.isfile(write_path))
        # Write to storage
        self.storage.write_file(df, write_path)
        self.assertTrue(os.path.isfile(self.storage.get_path_attrs(write_path)[0]))

    def test_read_write_local_json(self):
        # Set storage option
        storage = get_storage()
        # Paths
        read_path = './data/test_assets/test_read_write.json'
        write_path = './data/test_assets/test_read_write.json'
        # Read from storage
        json = storage.read_file(read_path)
        self.assertIsNotNone(json)
        # Remove existing file
        self.remove_file(write_path)
        self.assertFalse(os.path.isfile(write_path))
        # Write to storage
        storage.write_file(json, write_path)
        self.assertTrue(os.path.isfile(self.storage.get_path_attrs(write_path)[0]))

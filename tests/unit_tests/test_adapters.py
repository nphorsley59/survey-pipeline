

import os
import pandas as pd


from tests.unit_tests import BaseCase
from app.adapters.storage import LocalDirectory


class StorageCase(BaseCase):
    def test_read_write_local_csv(self):
        # Set storage option
        local = LocalDirectory()
        # Paths
        read_path = './data/test_assets/read_file.csv'
        write_path = './data/test_assets/write_file.csv'
        # Read from storage
        df = local.read_file(read_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)
        # Remove existing file
        if os.path.isfile(write_path):
            os.remove(write_path)
        self.assertFalse(os.path.isfile(write_path))
        # Write to storage
        local.write_file(df, write_path)
        self.assertTrue(os.path.isfile(write_path))

    def test_read_write_local_pickle(self):
        pass

    def test_read_write_local_json(self):
        pass

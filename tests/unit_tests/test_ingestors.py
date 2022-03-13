"""
Test ingestors.
"""


import unittest


import numpy as np
import pandas as pd


from app.ingestors.point_count_ingestor import PointCountIngestor
from app.ingestors.species_names_ingestor import SpeciesNamesIngestor
from tests.unit_tests import BaseCase


class PointCountIngestorTestCase(BaseCase):
    """File path being tested: app.ingestors.point_count_ingestor.py."""

    def setUp(self):
        df = pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])
        path = 'path'
        self.point_count_ingestor = PointCountIngestor(df=df, path=path)

    def test_init_instance(self):
        self.assertIsInstance(self.point_count_ingestor, PointCountIngestor)


class SpeciesNameIngestorTestCase(BaseCase):
    """File path being tested: app.ingestors.species_names_ingestor.py."""

    def setUp(self):
        df = pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])
        self.species_names_ingestor = SpeciesNamesIngestor(df=df)

    def test_init_instance(self):
        self.assertIsInstance(self.species_names_ingestor, SpeciesNamesIngestor)


if __name__ == '__main__':
    unittest.main()

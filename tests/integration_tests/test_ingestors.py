"""
Test ingestors integration.
"""


import unittest


import pandas as pd


from app.ingestors.point_count_ingestor import (
    factory_ingest_point_counts, PointCountIngestor)
from app.ingestors.species_names_ingestor import (
    factory_ingest_species_names, SpeciesNamesIngestor)
from config import Config
from tests.integration_tests import BaseCase


class PointCountIngestorTestCase(BaseCase):
    """File path being tested: app.ingestors.point_count_ingestor.py."""

    def setUp(self):
        self.all_point_count_ingestors = factory_ingest_point_counts()
        self.single_point_count_ingestor = self.all_point_count_ingestors[0]

    def test_init_instance(self):
        self.assertIsInstance(self.all_point_count_ingestors, list)
        self.assertIsInstance(self.single_point_count_ingestor, PointCountIngestor)
        self.assertIsInstance(self.single_point_count_ingestor.df, pd.DataFrame)
        self.assertTrue(
            self.single_point_count_ingestor.path in Config.POINT_COUNT_SOURCES)
        self.assertIsNone(self.single_point_count_ingestor.storage)

    def test_ingest_returns_df(self):
        df = self.single_point_count_ingestor.ingest()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)


class SpeciesNamesIngestorTestCase(BaseCase):
    """File path being tested: app.ingestors.species_names_ingestor.py."""

    def setUp(self):
        self.species_names_ingestor = factory_ingest_species_names()

    def test_init_instance(self):
        self.assertIsInstance(self.species_names_ingestor, SpeciesNamesIngestor)
        self.assertIsInstance(self.species_names_ingestor.df, pd.DataFrame)
        self.assertIsNone(self.species_names_ingestor.storage)

    def test_ingest_returns_df(self):
        df = self.species_names_ingestor.ingest()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)


if __name__ == '__main__':
    unittest.main()

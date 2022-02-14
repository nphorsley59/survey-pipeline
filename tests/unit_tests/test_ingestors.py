"""
Test ingestors.
"""


import pandas as pd

from app.ingestors.point_count_ingestor import (factory_ingest_point_counts,
                                                PointCountIngestor)
from app.ingestors.species_map_ingestor import (factory_ingest_species_map,
                                                SpeciesMapIngestor)
from tests.unit_tests import BaseCase


class IngestorCase(BaseCase):

    def setUp(self):
        self.species_map_ingestor = factory_ingest_species_map()
        self.point_count_ingestor = factory_ingest_point_counts()

    def test_instance_of_ingest_species_map(self):
        self.assertIsNotNone(self.species_map_ingestor)
        self.assertIsInstance(self.species_map_ingestor, SpeciesMapIngestor)

    def test_df_from_ingest_species_map(self):
        df = self.species_map_ingestor.ingest()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)

    def test_instance_of_ingest_point_counts(self):
        self.assertIsNotNone(self.point_count_ingestor)
        self.assertIsInstance(self.point_count_ingestor, list)

    def test_df_from_ingest_point_counts(self):
        df = self.point_count_ingestor[0].ingest()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)

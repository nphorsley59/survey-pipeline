"""
Test transformers integration.
"""


import unittest


import pandas as pd


from app.transformers import factory_transform_point_counts, PointCountTransformer
from tests.integration_tests import BaseCase


class PointCountTransformerTestCase(BaseCase):
    """File path being tested: app/transformers/point_count_transformer.py."""

    def setUp(self):
        self.point_count_transformer = factory_transform_point_counts()

    def test_init_instance(self):
        self.assertIsInstance(self.point_count_transformer, PointCountTransformer)
        self.assertIsInstance(self.point_count_transformer.df, pd.DataFrame)
        self.assertIsInstance(self.point_count_transformer.species_map, dict)
        self.assertIsNone(self.point_count_transformer.storage)

    def test_transform_returns_df(self):
        df = self.point_count_transformer.transform()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0] > 0)


if __name__ == '__main__':
    unittest.main()

"""
Test transformers.
"""


import unittest


import numpy as np
import pandas as pd


from src.transformers import PointCountTransformer
from tests.unit_tests import BaseCase


class PointCountTransformerTestCase(BaseCase):
    """File path being tested: app/transformers/point_count_transformer.py."""

    def setUp(self):
        df = pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])
        species_map = {'a': 'b'}
        self.point_count_transformer = PointCountTransformer(
            df=df, species_map=species_map)

    def test_init_instance(self):
        self.assertIsInstance(self.point_count_transformer, PointCountTransformer)


if __name__ == '__main__':
    unittest.main()

"""
Test features.
"""


import unittest


import numpy as np
import pandas as pd


from app.features import SpeciesNames
from tests.unit_tests import BaseCase


class SpeciesNamesTestCase(BaseCase):
    """File path being tested: app/features/species_names.py."""

    def setUp(self):
        df = pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])
        self.species_names = SpeciesNames(df=df)

    def test_init_instance(self):
        self.assertIsInstance(self.species_names, SpeciesNames)


if __name__ == '__main__':
    unittest.main()

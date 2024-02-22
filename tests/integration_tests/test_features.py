"""
Test features integration.
"""


import unittest


import pandas as pd


from src.features import species_names_factory, SpeciesNames
from tests.integration_tests import BaseCase


class SpeciesNamesTestCase(BaseCase):
    """File path being tested: app.features.species_names.py."""

    def setUp(self):
        self.species_names = species_names_factory()

    def test_factory_returns_a_species_names_instance(self):
        self.assertIsInstance(self.species_names, SpeciesNames)

    def test_factory_assigns_default_attributes(self):
        self.assertIsInstance(self.species_names.df, pd.DataFrame)
        self.assertIsNone(self.species_names.storage)

    def test_code_to_common_name_dict(self):
        self.assertIsInstance(self.species_names.code_to_common_name_dict(), dict)


if __name__ == '__main__':
    unittest.main()

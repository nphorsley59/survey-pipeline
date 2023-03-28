"""
Test adapters integration.
"""


import unittest


from src.adapters.storage import factory_local_directory, LocalDirectory
from tests.unit_tests import BaseCase


class LocalDirectoryTestCase(BaseCase):
    """File path being tested: app/adapters/storage/local_directory.py."""

    def test_factory_returns_a_local_directory(self):
        result = factory_local_directory()
        self.assertIsInstance(result, LocalDirectory)


if __name__ == '__main__':
    unittest.main()

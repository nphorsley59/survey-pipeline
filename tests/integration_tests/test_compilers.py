"""
Test compilers integration.
"""


import unittest


import pandas as pd


from app.compilers import factory_compile_point_counts, PointCountCompiler
from config import Config
from tests.integration_tests import BaseCase


class PointCountCompilerTestCase(BaseCase):
    """File path being tested: app.compilers.point_count_compiler."""

    def setUp(self):
        self.compiler = factory_compile_point_counts()

    def test_factory_returns_a_point_count_compiler(self):
        self.assertIsInstance(self.compiler, PointCountCompiler)

    def test_factory_assigns_default_attributes(self):
        self.assertIsInstance(self.compiler.dfs, list)
        self.assertIsNone(self.compiler.storage)


if __name__ == '__main__':
    unittest.main()

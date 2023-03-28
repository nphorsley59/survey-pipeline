"""
Test compilers integration.
"""


import unittest


from src.compilers import factory_compile_point_counts, PointCountCompiler
from tests.integration_tests import BaseCase


class PointCountCompilerTestCase(BaseCase):
    """File path being tested: app.compilers.point_count_compiler."""

    def test_factory_returns_a_point_count_compiler(self):
        compiler = factory_compile_point_counts()
        self.assertIsInstance(compiler, PointCountCompiler)

    def test_factory_assigns_default_attributes(self):
        compiler = factory_compile_point_counts()
        self.assertIsInstance(compiler.dfs, list)
        self.assertIsNone(compiler.storage)


if __name__ == '__main__':
    unittest.main()

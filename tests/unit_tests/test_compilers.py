"""
Test compilers.
"""


import unittest


import numpy as np
import pandas as pd


from src.compilers import PointCountCompiler
from tests.integration_tests import BaseCase


class PointCountCompilerTestCase(BaseCase):
    """File path being tested: app.compilers.point_count_compiler."""

    def setUp(self):
        self.dfs = [pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])]

    def test_init_instance(self):
        compiler = PointCountCompiler(dfs=self.dfs)
        self.assertIsInstance(compiler, PointCountCompiler)

    def test_compile_returns_df(self):
        compiler = PointCountCompiler(dfs=self.dfs)
        self.assertIsNone(compiler.storage)
        self.assertIsInstance(compiler.compile(), pd.DataFrame)


if __name__ == '__main__':
    unittest.main()

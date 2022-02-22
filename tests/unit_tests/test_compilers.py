"""
Test compilers.
"""


import unittest


import numpy as np
import pandas as pd


from app.compilers import PointCountCompiler
from tests.integration_tests import BaseCase


class PointCountCompilerTestCase(BaseCase):
    """File path being tested: app.compilers.point_count_compiler."""

    def setUp(self):
        dfs = [pd.DataFrame(np.array([[1, 2], [2, 3]]), columns=['a', 'b'])]
        self.compiler = PointCountCompiler(dfs=dfs)

    def test_init_instance(self):
        self.assertIsInstance(self.compiler, PointCountCompiler)

    def test_compile_returns_df(self):
        self.assertIsNone(self.compiler.storage)
        self.assertIsInstance(self.compiler.compile(), pd.DataFrame)


if __name__ == '__main__':
    unittest.main()

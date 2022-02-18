"""
Ingested point count data needs to be compiled before transformation or analysis.
"""


from typing import Optional


import pandas as pd


from app.adapters.storage import get_storage
from config import Config, logger


class PointCountCompiler:
    """Class to compile ingested point count data into a single dataframe."""
    def __init__(self, dfs: list[pd.DataFrame], storage: Optional = None):
        """Initialize PointCountCompiler instance.

        Args:
            dfs (pd.DataFrame): Standardized point count data.
            storage: Storage adapter used to write data.
        """
        self.dfs = dfs
        self.storage = storage
        self.df = None

    def concat(self):
        """Concatenate ingested data sources into single dataframe."""
        self.df = pd.concat(self.dfs)

    def export(self):
        """Export dataframe."""
        if self.storage:
            self.storage.write_file(self.df, 'data/compiled/point_counts.pkl')

    def compile(self):
        """Compile ingested dataframes."""
        self.concat()
        self.export()
        logger.info('[DONE] compile_point_counts()')
        return self.df


def factory_compile_point_counts(dfs: Optional[list[pd.DataFrame]] = None,
                                 storage: Optional = None):
    """Factory to compile ingested point count data into a single dataframe.

    Args:
        dfs (pd.DataFrame): Standardized point count data.
        storage: Storage adapter used to write data.
    """
    logger.info('[INIT] compile_point_counts()')
    read_storage = storage or get_storage()
    paths = Config.POINT_COUNTS_INGESTED
    dfs = dfs or [read_storage.read_file(path) for path in paths]
    compiler = PointCountCompiler(dfs=dfs, storage=storage)
    logger.info('[PRIMED] compile_point_counts()')
    return compiler


if __name__ == '__main__':
    test = factory_compile_point_counts().compile()
    print(test.sample(5))

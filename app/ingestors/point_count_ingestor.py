"""
This script ingests, standardizes, and validates a dataframe of point count data.
Problems with the dataframe that cannot be coerced automatically will be raised and
must be fixed manually.
"""


from itertools import zip_longest
from typing import Optional


import pandas as pd


from app.adapters.storage import get_storage
from app.validators import DataFrameValidator
from config import Config, logger


class PointCountIngestor:
    """Class to ingest and standardize a point count dataframe."""

    def __init__(self, df: pd.DataFrame, path: str, storage: Optional = None):
        """Initiate PointCountIngestor instance.

        Args:
            df (pd.DataFrame): Raw point count data.
            path (str): Read path; used to create write path.
            storage: Storage adapter used to write data.
        """
        self.df = df
        self.path = path
        self.storage = storage
        self.incomplete_records = None

    def set_header(self):
        """Validate header against template and set column order."""
        schema_columns = set(Config.SCHEMA_POINT_COUNT_INGEST.keys())
        ingested_columns = set(self.df.columns)
        print(ingested_columns)
        print(schema_columns)
        if ingested_columns != schema_columns:
            raise ValueError('Header does not match template.')
        self.df = self.df[Config.SCHEMA_POINT_COUNT_INGEST.keys()]

    def set_dtypes(self):
        """Set data types for each column."""
        for column, attrs in Config.SCHEMA_POINT_COUNT_INGEST.items():
            try:
                self.df[column] = self.df[column].astype(attrs['type'])
            except ValueError:
                logger.critical(f"Could not assign type ({attrs['type']}) "
                                f"to column ({column}).")

    def fill_nulls(self):
        """Fill null values with defaults or logic, when possible."""
        # With most common value
        for column in ['observer_id']:
            self.df[column] = self.df[column].fillna(self.df[column].mode()[0])
        # With default value
        for column, attrs in Config.SCHEMA_POINT_COUNT_INGEST.items():
            if attrs['default'] is not None:
                self.df[column] = self.df[column].fillna(attrs['default'], axis=0)
                logger.info(f"[STATUS] Auto-filled column ({column}) "
                            f"nulls with default ({attrs['default']}).")

    def drop_incomplete_records(self):
        """Drop records with null values in required columns.

        Note:
            Dropped records are stored as self.incomplete_records.
        """
        # Get incomplete records
        required_columns = [column for column, attrs
                            in Config.SCHEMA_POINT_COUNT_INGEST.items()
                            if attrs['required']]
        self.incomplete_records = self.df[self.df[required_columns]
                                          .isnull().any(axis='columns')]
        # Drop by index
        ir_index = self.incomplete_records.index
        ir_count = len(ir_index)
        self.df = self.df.drop(index=ir_index)
        # Log results
        if ir_count > 0:
            logger.warning(f'Null values could not be coerced '
                           f'for {ir_count} records.')

    def validate(self):
        """Validate dataframe against 'point count' schema."""
        validator = DataFrameValidator(
            df=self.df, schema='ingested point count')
        validator.validate()

    def export(self):
        """Export dataframe."""
        write_path = self.path \
            .replace('/source/', '/ingested/') \
            .replace('.csv', '.pkl')
        if self.storage:
            self.storage.write_file(self.df, write_path)

    def ingest(self):
        """Ingest dataframe."""
        self.set_header()
        self.set_dtypes()
        self.fill_nulls()
        self.drop_incomplete_records()
        self.validate()
        self.export()
        logger.info('[DONE] ingest_point_counts()')
        return self.df


def factory_ingest_point_counts(dfs: Optional[list[pd.DataFrame]] = None,
                                paths: Optional[list[str]] = None,
                                storage: Optional = None):
    """Factory to ingest raw point count dataframes.

    Args:
        dfs (pd.DataFrame): Raw point count data.
        paths (str): Read paths, required if sources are provided.
        storage: Storage adapter used to read/write data.

    Notes:
        Defaults to read-only if adapter is not provided for storage.
        Pass data to df to run pipeline in memory.
    """
    logger.info('[INIT] ingest_point_counts()')
    read_storage = storage or get_storage()
    paths = paths or Config.POINT_COUNT_SOURCES
    dfs = dfs or [None]
    sources = zip_longest(dfs, paths)
    ingested_sources = []
    for df, path in sources:
        if df is None:
            df = read_storage.read_file(path)
        ingestor = PointCountIngestor(df=df, path=path, storage=storage)
        ingested_sources.append(ingestor)
    logger.info('[PRIMED] ingest_point_counts()')
    return ingested_sources


if __name__ == '__main__':
    for source in factory_ingest_point_counts(storage=None):
        source.ingest()

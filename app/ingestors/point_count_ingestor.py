"""
Raw point count data must be ingested and validated before transformation or analysis.

This class ingests, standardizes, and validates a dataframe of point count data.
Problems with the dataframe that cannot be coerced automatically will be raised and
must be fixed manually.
"""


from itertools import zip_longest
from typing import Optional


import pandas as pd


from app.adapters.storage import get_storage
from app import validators
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
        # Validate
        template = set(Config.POINT_COUNT_COLS_INGEST.keys())
        df_columns = set(self.df.columns)
        if df_columns != template:
            raise ValueError('Header does not match template.')
        # Reorder
        self.df = self.df[Config.POINT_COUNT_COLS_INGEST.keys()]

    def set_dtypes(self):
        """Set data types for each column."""
        type_dict = Config.POINT_COUNT_COLS_INGEST
        for column, dtype in type_dict.items():
            try:
                self.df[column] = self.df[column].astype(dtype)
            except ValueError:
                logger.critical(f'Could not assign type "{dtype}" '
                                f'to column "{column}".')

    @staticmethod
    def fill_most_common(df: pd.DataFrame = None) -> pd.DataFrame:
        """Fill null values with most common value, when applicable.

        Args:
            df (pd.DataFrame): Raw point count data.

        Returns:
            Point count data with nulls filled for certain categories.
        """
        for column in Config.AUTO_FILL_CAT_COLS:
            df[column] = df[column].fillna(df[column].mode()[0])
        return df

    def fill_nulls(self):
        """Fill null values with defaults or logic, when possible."""
        # Most common value
        self.df = self.fill_most_common(self.df)
        # Default value
        for column, value in Config.NULL_DEFAULTS.items():
            self.df[column] = self.df[column].fillna(value, axis=0)
            logger.info(f'[STATUS] Auto-filled "{column}" '
                        f'nulls with "{value}".')

    def drop_missing(self):
        """Drop records with null values in required columns.

        Note:
            Dropped records are stored in self.incomplete_records
            for reference.
        """
        # Get incomplete records
        req_cols = Config.REQUIRED_COLS
        missing_req = self.df[req_cols].isnull().any(axis='columns')
        self.incomplete_records = self.df[missing_req]
        ir_index = self.incomplete_records.index
        ir_count = len(ir_index)
        # Drop by index
        self.df = self.df.drop(index=ir_index)
        # Log action
        if ir_count > 0:
            logger.warning(f'Null values could not be coerced '
                           f'for {ir_count} records.')

    def validate(self):
        """Validate dataframe against 'point count' schema."""
        validator = validators.DataFrameValidator(
            df=self.df, schema='point count')
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
        self.drop_missing()
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
    for source in factory_ingest_point_counts(storage=get_storage()):
        source.ingest()

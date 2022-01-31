

from typing import Optional


import pandas as pd


from app.adapters import storage
from app import validators
import config


class PointCountIngestor:
    """Class to ingest and standardize a point count dataframe."""
    def __init__(self, df: pd.DataFrame, write_storage=None):
        """Initiate PointCountIngestor instance.

        Args:
            df (pd.DataFrame): Raw point count data.
            write_storage: Storage adapter used to write data.
        """
        self.df = df
        self.storage_adapter = write_storage
        self.incomplete_records = None

    def set_header(self):
        """Validate header against template and set column order."""
        # Validate
        template = set(config.Config.POINT_COUNT_COLS_INGEST.keys())
        df_columns = set(self.df.columns)
        if df_columns != template:
            raise ValueError('Header does not match template.')
        # Reorder
        self.df = self.df[config.Config.POINT_COUNT_COLS_INGEST.keys()]

    def set_dtypes(self):
        """Set data types for each column."""
        type_dict = config.Config.POINT_COUNT_COLS_INGEST
        for column, dtype in type_dict.items():
            try:
                self.df[column] = self.df[column].astype(dtype)
            except ValueError:
                config.logger.critical(f'Could not assign type "{dtype}" '
                                       f'to column "{column}".')

    @staticmethod
    def fill_most_common(df: pd.DataFrame = None) -> pd.DataFrame:
        """Fill null values with most common value, when applicable.

        Args:
            df (pd.DataFrame): Raw point count data.

        Returns:
            Point count data with nulls filled for certain categories.
        """
        for column in config.Config.AUTO_FILL_CAT_COLS:
            df[column] = df[column].fillna(df[column].mode()[0])
        return df

    def fill_nulls(self):
        """Fill null values with defaults or logic, when possible."""
        # Most common value
        self.df = self.fill_most_common(self.df)
        # Default value
        for column, value in config.Config.NULL_DEFAULTS.items():
            self.df[column] = self.df[column].fillna(value, axis=0)
            config.logger.info(f'[STATUS] Auto-filled "{column}" '
                               f'nulls with "{value}".')

    def drop_missing(self):
        """Drop records with null values in required columns.

        Note:
            Dropped records are stored in self.incomplete_records
            for reference.
        """
        # Get incomplete records
        req_cols = config.Config.REQUIRED_COLS
        missing_req = self.df[req_cols].isnull().any(axis='columns')
        self.incomplete_records = self.df[missing_req]
        ir_index = self.incomplete_records.index
        ir_count = len(ir_index)
        # Drop by index
        self.df = self.df.drop(index=ir_index)
        # Log action
        if ir_count > 0:
            config.logger.warning(f'Null values could not be coerced '
                                  f'for {ir_count} records.')

    def validate(self):
        """Validate dataframe against 'point count' schema."""
        validator = validators.DataFrameValidator(
            df=self.df, schema='point count')
        validator.validate()

    def export(self):
        """Export dataframe."""
        if self.storage_adapter:
            self.storage_adapter.write_file(
                self.df, 'data/ingested/point_counts_2021-07-02.pkl')

    def ingest(self):
        """Ingest dataframe."""
        self.set_header()
        self.set_dtypes()
        self.fill_nulls()
        self.drop_missing()
        self.validate()
        self.export()
        config.logger.info('[DONE] ingest_point_counts()')
        return self.df


def ingest_point_counts(storage_adapter: Optional = None,
                        sources: Optional[list[pd.DataFrame]] = None):
    """Factory to ingest raw point count dataframes.

    Args:
        storage_adapter: Storage adapter used to read/write data.
        sources (pd.DataFrame): Raw point count data.

    Notes:
        Defaults to read-only if adapter is not provided for storage.
        Pass data to df to run pipeline in memory.
    """
    config.logger.info('[INIT] ingest_point_counts()')
    read_storage = storage_adapter or storage.get_storage()
    sources = sources or config.Config.POINT_COUNT_SOURCES
    ingested_sources = []
    for src in sources:
        if isinstance(src, str):
            src = read_storage.read_file(src)
        ingestor = PointCountIngestor(df=src, write_storage=storage_adapter)
        ingested_sources.append(ingestor)
    config.logger.info('[PRIMED] ingest_point_counts()')
    return ingested_sources


if __name__ == '__main__':
    for source in ingest_point_counts(storage_adapter=storage.get_storage()):
        source.ingest()

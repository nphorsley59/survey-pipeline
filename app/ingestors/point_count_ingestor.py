

import pandas as pd


from config import Config, logger
from app.validators import DataFrameValidator
from app.utils import local_path


class PointCountIngestor:
    """Ingest and standardize a point count dataframe."""
    def __init__(self, df: pd.DataFrame = None):
        """Initiate PointCountIngestor instance."""
        self.df = df
        self.incomplete_records = None

    def validate_header(self):
        template = list(Config.POINT_COUNT_COLS_INGEST.keys())
        if len(self.df.columns.intersection(template)) != len(template):
            logger.critical(f'Header does not match template')
            raise ValueError

    def set_dtypes(self):
        type_dict = Config.POINT_COUNT_COLS_INGEST
        for column, dtype in type_dict.items():
            try:
                self.df[column] = self.df[column].astype(dtype)
            except ValueError:
                logger.critical(f'Could not assign type "{dtype}" to column "{column}"')

    @staticmethod
    def fill_most_common(df: pd.DataFrame = None) -> pd.DataFrame:
        """Fill null values with most common category."""
        for column in Config.AUTO_FILL_CAT_COLS:
            df[column] = df[column].fillna(df[column].mode()[0])
        return df

    def auto_fill(self):
        """Fill null values with defaults or using logic, when possible."""
        self.df = self.fill_most_common(self.df)
        for column, value in Config.NULL_DEFAULTS.items():
            self.df[column] = self.df[column].fillna(value, axis=0)
            logger.info(f'[STATUS] Auto-filled "{column}" nulls with "{value}"')

    def drop_missing(self):
        """Drop records with null values in required columns.

        Note:
            Dropped records are stored in self.incomplete_records for reference
        """
        # get incomplete records
        self.incomplete_records = self.df[self.df[Config.REQUIRED_COLS].isnull().any(axis='columns')]
        ir_index = self.incomplete_records.index
        ir_count = len(ir_index)
        # drop by index
        self.df = self.df.drop(index=ir_index)
        # log action
        if ir_count > 0:
            logger.warning(f'Null values could not be coerced for {ir_count} records')

    def order_columns(self):
        """Set column order."""
        self.df = self.df[Config.POINT_COUNT_COLS_INGEST]

    def validate_dataframe(self):
        """Validate dataframe against 'point count' schema."""
        # TODO - Missing date range validation
        validator = DataFrameValidator(df=self.df, schema='point count')
        validator.validate()

    def export(self):
        """Docstring"""
        pass

    def ingest(self):
        """Ingest the dataframe."""
        self.validate_header()
        self.set_dtypes()
        self.auto_fill()
        self.drop_missing()
        self.order_columns()
        self.validate_dataframe()


def ingest_point_counts():
    """Factory to ingest and standardize a point count dataframe."""
    logger.info('[START ] ingest_point_counts()')
    # read csv
    path = local_path(path=r'data/raw/point_counts_2021-07-02.csv')
    df = pd.read_csv(path)
    # ingest
    ingestor = PointCountIngestor(df)
    ingestor.ingest()
    logger.info('[FINISH] ingest_point_counts()')


if __name__ == '__main__':
    ingest_point_counts()

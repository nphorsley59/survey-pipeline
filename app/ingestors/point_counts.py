# TODO - First pass at ingestion and validation, missing casing prep, checks for invalid
#  values in numeric columns ('a' for 'point', for example), date range validation, etc.
#  Some of this work is low impact and can wait for a refactor after ingestion has been
#  tested on more data. Next step is to prepare (transform) the data for use in analytics
#  dashboards. Consider breaking feature engineering functionality out of ingestor and
#  putting it in the next step.

# TODO - Also missing forced typing during ingestion.


import datetime as dt
import numpy as np
import pandas as pd


from config import Config, logger
from app.validators import DataFrameValidator
from app.utils import local_path


class PointCountIngestor:
    """Docstring"""
    def __init__(self, df: pd.DataFrame = None):
        """Initiate PointCountIngestor instance."""
        self.df = df
        self.incomplete_records = None

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

    @staticmethod
    def x_to_bool(df: pd.DataFrame = None) -> pd.DataFrame:
        """Convert T/F columns to bool."""
        for column in Config.BOOL_COLS:
            df[column] = np.where(df[column].notnull(), True, False)
        return df

    @staticmethod
    def merge_date(df: pd.DataFrame = None) -> pd.DataFrame:
        """Merge year, month, and day into a single variable, date (YYYY-MM-DD)."""
        df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
        return df

    @staticmethod
    def start_time_to_seconds(df: pd.DataFrame = None) -> pd.DataFrame:
        """Convert start time (HH:MM) to seconds elapsed since the start of the day."""
        date_const = dt.datetime(1900, 1, 1)
        df['start_time'] = df['start_time']\
            .apply(lambda x: (dt.datetime.strptime(x, "%H:%M") - date_const).total_seconds())
        return df

    def engineer_features(self):
        """Groups feature manipulation tasks into a single function."""
        self.df = self.x_to_bool(self.df)
        self.df = self.merge_date(self.df)
        self.df = self.start_time_to_seconds(self.df)

    def order_columns(self):
        """Set column order."""
        self.df = self.df[Config.POINT_COUNT_COLUMNS]

    def validate(self):
        """Validate dataframe against 'point count' schema."""
        validator = DataFrameValidator(df=self.df, schema='point count')
        validator.validate()

    def ingest(self):
        """Ingest a point count dataframe."""
        self.auto_fill()
        self.drop_missing()
        self.engineer_features()
        self.order_columns()
        self.validate()


def ingest_point_counts():
    """Docstring"""
    logger.info('[START ] ingest_point_counts()')
    path = local_path(path=r'data\raw\test_df.csv')
    df = pd.read_csv(path)
    ingestor = PointCountIngestor(df)
    ingestor.ingest()
    logger.info('[FINISH] ingest_point_counts()')
    print(ingestor.df.sample(10))


if __name__ == '__main__':
    ingest_point_counts()

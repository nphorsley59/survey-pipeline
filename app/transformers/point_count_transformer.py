"""
Docstring
"""


import datetime as dt
from typing import Optional


import numpy as np
import pandas as pd


from app.adapters.storage import get_storage
from config import Config, logger


class PointCountPreprocessingTransformer:
    """Docstring"""
    def __init__(self, df: pd.DataFrame = None, storage: Optional = None):
        """Docstring"""
        self.df = df
        self.storage = storage

    def x_to_bool(self):
        """Convert X/None columns to bool."""
        for column in Config.BOOL_COLS:
            self.df[column] = np.where(self.df[column].notnull(), True, False)

    def merge_date(self):
        """Merge year, month, and day into a single variable, date (YYYY-MM-DD)."""
        self.df['date'] = pd.to_datetime(self.df[['year', 'month', 'day']])

    def start_time_to_seconds(self):
        """Convert start time (HH:MM) to seconds elapsed since start of the day."""
        date_const = dt.datetime(1900, 1, 1)
        self.df['start_time'] = self.df['start_time']\
            .apply(lambda x: (dt.datetime.strptime(x, "%H:%M") - date_const)
                   .total_seconds())

    def abbr_to_full(self):
        """Docstring"""
        self.df['sex'] = self.df['sex'].replace(Config.SEX)
        self.df['how'] = self.df['how'].replace(Config.HOW)

    def clean(self):
        """Docstring"""
        self.df = self.df[Config.PROCESSED_POINT_COUNTS_COLUMNS]

    def transform(self):
        """Groups feature manipulation tasks into a single function."""
        self.x_to_bool()
        self.merge_date()
        self.start_time_to_seconds()
        self.abbr_to_full()
        self.clean()
        logger.info('[DONE] preprocess_transform_point_counts()')
        return self.df


def factory_preprocess_point_counts(storage: Optional = None):
    """Docstring"""
    logger.info('[INIT] preprocess_transform_point_counts()')
    read_storage = storage or get_storage()
    df = read_storage.read_file('data/compiled/point_counts.pkl')
    transformer = PointCountPreprocessingTransformer(df=df, storage=storage)
    logger.info('[PRIMED] preprocess_transform_point_counts()')
    return transformer


if __name__ == '__main__':
    test = factory_preprocess_point_counts().transform()
    print(test.head(5))

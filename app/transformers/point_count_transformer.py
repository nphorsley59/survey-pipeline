

import datetime as dt
import numpy as np
import pandas as pd


from config import Config


class PointCountTransformer:
    """Docstring"""
    def __init__(self, df: pd.DataFrame = None):
        """Docstring"""
        self.df = df

    def x_to_bool(self):
        """Convert T/F columns to bool."""
        for column in Config.BOOL_COLS:
            self.df[column] = np.where(self.df[column].notnull(), True, False)

    def merge_date(self):
        """Merge year, month, and day into a single variable, date (YYYY-MM-DD)."""
        self.df['date'] = pd.to_datetime(self.df[['year', 'month', 'day']])

    def start_time_to_seconds(self):
        """Convert start time (HH:MM) to seconds elapsed since the start of the day."""
        date_const = dt.datetime(1900, 1, 1)
        self.df['start_time'] = self.df['start_time']\
            .apply(lambda x: (dt.datetime.strptime(x, "%H:%M") - date_const).total_seconds())

    def engineer_features(self):
        """Groups feature manipulation tasks into a single function."""
        self.x_to_bool()
        self.merge_date()
        self.start_time_to_seconds()

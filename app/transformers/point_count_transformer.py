"""
This script handles transformations and mapping to minimize the amount of data
manipulation required during analysis.
"""


import datetime as dt
from typing import Optional


import numpy as np
import pandas as pd


from app.adapters.storage import get_storage
from app.features import species_names_factory
from app.validators import DataFrameValidator
from config import Config, logger


class PointCountTransformer:
    """Class to prepare point count data for analysis."""

    def __init__(self, df: pd.DataFrame, species_map: dict,
                 storage: Optional = None):
        """Initialize PointCountTransformer instance.

        Args:
            df (pd.DataFrame): Compiled point count data.
            species_map (dict): Dictionary to map 4-letter codes to common names.
            storage: Storage adapter used to write data.
        """
        self.df = df
        self.species_map = species_map
        self.storage = storage

    def x_to_bool(self):
        """Convert X/None columns to bool."""
        for column in ['visual', 'migrating']:
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
        """Add columns with full names of abbreviations."""
        self.df['observer'] = self.df['observer_id'].replace(Config.OBSERVERS)
        self.df['site'] = self.df['site_id'].replace(Config.SITES)
        self.df['sex'] = self.df['sex'].replace(Config.SEX)
        self.df['how'] = self.df['how'].replace(Config.HOW)
        self.df['species'] = self.df['species_code'].replace(self.species_map)

    def clean(self):
        """Re-order columns and set data types."""
        self.df = self.df[Config.SCHEMA_POINT_COUNT_TRANSFORM.keys()]
        for column, attrs in Config.SCHEMA_POINT_COUNT_TRANSFORM.items():
            try:
                self.df[column] = self.df[column].astype(attrs['type'])
            except ValueError:
                logger.critical(f"Could not assign type ({attrs['type']}) "
                                f"to column ({column}).")

    def validate(self):
        """Validate dataframe."""
        validator = DataFrameValidator(self.df, schema='transformed point count')
        validator.validate()

    def transform(self):
        """Groups feature manipulation tasks into a single function."""
        self.x_to_bool()
        self.merge_date()
        self.start_time_to_seconds()
        self.abbr_to_full()
        self.clean()
        logger.info('[DONE] preprocess_transform_point_counts()')
        return self.df


def factory_transform_point_counts(df: Optional[pd.DataFrame] = None,
                                   species_map: Optional[dict] = None,
                                   storage: Optional = None):
    """Factory to prepare point count data for analysis.

    Args:
        df (pd.DataFrame): Compiled point count data.
        species_map (dict): Dictionary to map 4-letter codes to common names.
        storage: Storage adapter used to write data.

    Notes:
        Defaults to read-only if adapter is not provided for storage.
        Pass data to df to run pipeline in memory.
    """
    logger.info('[INIT] preprocess_transform_point_counts()')
    read_storage = storage or get_storage()
    df = df or read_storage.read_file('data/compiled/point_counts.pkl')
    species_map = species_map or species_names_factory().code_to_common_name_dict()
    transformer = PointCountTransformer(df=df, species_map=species_map,
                                        storage=storage)
    logger.info('[PRIMED] preprocess_transform_point_counts()')
    return transformer


if __name__ == '__main__':
    test = factory_transform_point_counts().transform()

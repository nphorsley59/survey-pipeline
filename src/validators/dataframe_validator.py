"""
This script stores validation schemas built using Pandera to improve the
reliability of data returned by the pipeline. It complements the work of the test
suite.
"""


from typing import Optional


import pandas as pd
import pandera as pa


from src.adapters.storage import get_storage
from src.features import species_names_factory
from config import Config, logger


class DataFrameValidator:
    """Validate contents of a dataframe based on a pre-defined schema."""
    SPECIES_CODES = list(species_names_factory().df['4_letter_code'])
    SPECIES_NAMES = list(species_names_factory().df['common_name'])

    def __init__(self, df: pd.DataFrame, schema: str):
        """Initiate DataFrameValidator instance.

        Args:
            df (pd.DataFrame): Dataframe to validate
            schema (str): Pre-defined schema to use; possible values:
                ['ingested point count', 'transformed point count']
        """
        self.df = df
        self.schema = schema

    def ingested_point_count_schema(self):
        """Schema for ingested point count data."""
        schema = pa.DataFrameSchema({
            'observer_id': pa.Column(
                str, pa.Check.isin(Config.OBSERVERS.keys())),
            'year': pa.Column(
                float, pa.Check.in_range(
                    Config.YEAR_RANGE['min'],
                    Config.YEAR_RANGE['max'])),
            'month': pa.Column(
                float, pa.Check.in_range(
                    Config.MONTH_RANGE['min'],
                    Config.MONTH_RANGE['max'])),
            'day': pa.Column(
                float, pa.Check.in_range(
                    Config.DAY_RANGE['min'],
                    Config.DAY_RANGE['max'])),
            'site_id': pa.Column(str, pa.Check.isin(Config.SITES.keys())),
            'start_time': pa.Column(object, nullable=True),
            'point': pa.Column(
                float, pa.Check.in_range(
                    Config.POINTS_RANGE['min'],
                    Config.POINTS_RANGE['max'])),
            'minute': pa.Column(
                float, pa.Check.in_range(
                    Config.MINUTES_RANGE['min'],
                    Config.MINUTES_RANGE['max']),
                nullable=True),
            'species_code': pa.Column(
                str, pa.Check.isin(self.SPECIES_CODES)),
            'distance': pa.Column(
                float, pa.Check.in_range(
                    Config.DISTANCE_RANGE['min'],
                    Config.DISTANCE_RANGE['max']),
                nullable=True),
            'how': pa.Column(
                str, pa.Check.isin(Config.HOW.keys()),
                nullable=True),
            'visual': pa.Column(str, nullable=True),
            'sex': pa.Column(str, pa.Check.isin(Config.SEX.keys())),
            'migrating': pa.Column(str, nullable=True),
            'cluster_size': pa.Column(
                float, pa.Check.in_range(
                    Config.CLUSTER_SIZE['min'],
                    Config.CLUSTER_SIZE['max'])),
            'cluster_code': pa.Column(str, nullable=True),
            'notes': pa.Column(str, nullable=True),
        })
        return schema

    def transformed_point_count_schema(self):
        """Schema for transformed point count data."""
        schema = pa.DataFrameSchema({
            'observer_id': pa.Column(str, pa.Check.isin(Config.OBSERVERS.keys())),
            'observer': pa.Column(str, pa.Check.isin(Config.OBSERVERS.values())),
            'site_id': pa.Column(str, pa.Check.isin(Config.SITES.keys())),
            'site': pa.Column(str, pa.Check.isin(Config.SITES.values())),
            'date': pa.Column(pa.typing.DateTime),
            'start_time': pa.Column(float, nullable=True),
            'point': pa.Column(
                float, pa.Check.in_range(
                    Config.POINTS_RANGE['min'],
                    Config.POINTS_RANGE['max'])),
            'minute': pa.Column(
                float, pa.Check.in_range(
                    Config.MINUTES_RANGE['min'],
                    Config.MINUTES_RANGE['max']),
                nullable=True),
            'species_code': pa.Column(str, pa.Check.isin(self.SPECIES_CODES)),
            'species': pa.Column(str, pa.Check.isin(self.SPECIES_NAMES)),
            'distance': pa.Column(
                float, pa.Check.in_range(
                    Config.DISTANCE_RANGE['min'],
                    Config.DISTANCE_RANGE['max']),
                nullable=True),
            'how': pa.Column(
                str, pa.Check.isin(Config.HOW.values()), nullable=True),
            'visual': pa.Column(bool),
            'sex': pa.Column(str, pa.Check.isin(Config.SEX.values())),
            'migrating': pa.Column(bool),
            'cluster_size': pa.Column(
                float, pa.Check.in_range(
                    Config.CLUSTER_SIZE['min'],
                    Config.CLUSTER_SIZE['max'])),
            'cluster_code': pa.Column(str, nullable=True),
            'notes': pa.Column(str, nullable=True)
        })
        return schema

    def validate(self):
        """Validate the dataframe."""
        match self.schema:
            case 'ingested point count':
                schema = self.ingested_point_count_schema()
                schema(self.df)
            case 'transformed point count':
                schema = self.transformed_point_count_schema()
                schema(self.df)
            case _:
                raise KeyError(f"Invalid schema ({self.schema}) provided.")
        logger.info('[STATUS] Validated dataframe.')


def validate_dataframe(storage: Optional = None):
    """Sandbox to test dataframe validation.

    Args:
        storage: Storage adapter used to read/write data.
    """
    storage = storage or get_storage()
    df = storage.read_file('data/source/point_counts_2020-06-21.csv')
    validator = DataFrameValidator(df=df, schema='point count')
    return validator


if __name__ == '__main__':
    test = validate_dataframe()

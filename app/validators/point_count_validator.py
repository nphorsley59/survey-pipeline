

from typing import Optional


import pandas as pd
import pandera as pa


from app.adapters import storage
import config


class DataFrameValidator:
    """Validate contents of a dataframe based on a pre-defined schema."""
    SPECIES_LETTER_CODES = storage.get_storage().read_file(
        'data/reference/species_codes.json')['4_letter_code'].to_list()

    def __init__(self, df: pd.DataFrame, schema: str):
        """Initiate DataFrameValidator instance.

        Args:
            df (pd.DataFrame): Dataframe to validate
            schema (str): Pre-defined schema to use; possible values:
            'point count'
        """
        self.df = df
        self.schema = schema

    def point_count_schema(self):
        """Schema for ingested point count data."""
        schema = pa.DataFrameSchema({
            'observer_id': pa.Column(
                str, pa.Check.isin(config.Config.OBSERVERS)),
            'year': pa.Column(
                float, pa.Check.in_range(
                    config.Config.YEAR_RANGE['min'],
                    config.Config.YEAR_RANGE['max'])),
            'month': pa.Column(
                float, pa.Check.in_range(
                    config.Config.MONTH_RANGE['min'],
                    config.Config.MONTH_RANGE['max'])),
            'day': pa.Column(
                float, pa.Check.in_range(
                    config.Config.DAY_RANGE['min'],
                    config.Config.DAY_RANGE['max'])),
            'site_id': pa.Column(str, pa.Check.isin(config.Config.SITES)),
            'start_time': pa.Column(object, nullable=True),
            'point': pa.Column(
                float, pa.Check.in_range(
                    config.Config.POINTS_RANGE['min'],
                    config.Config.POINTS_RANGE['max'])),
            'minute': pa.Column(
                float, pa.Check.in_range(
                    config.Config.MINUTES_RANGE['min'],
                    config.Config.MINUTES_RANGE['max']),
                nullable=True),
            'species_code': pa.Column(
                str, pa.Check.isin(self.SPECIES_LETTER_CODES)),
            'distance': pa.Column(
                float, pa.Check.in_range(
                    config.Config.DISTANCE_RANGE['min'],
                    config.Config.DISTANCE_RANGE['max']),
                nullable=True),
            'how': pa.Column(
                str, pa.Check.isin(config.Config.HOW),
                nullable=True),
            'visual': pa.Column(str, nullable=True),
            'sex': pa.Column(str, pa.Check.isin(config.Config.SEX)),
            'migrating': pa.Column(str, nullable=True),
            'cluster_size': pa.Column(
                float, pa.Check.in_range(
                    config.Config.CLUSTER_SIZE['min'],
                    config.Config.CLUSTER_SIZE['max'])),
            'cluster_code': pa.Column(str, nullable=True),
            'notes': pa.Column(str, nullable=True),
        })
        return schema

    @staticmethod
    def point_count_transformed_schema():
        """Schema for transformed point count data."""
        schema = pa.DataFrameSchema({
            'site_id': pa.Column(str, pa.Check.isin(config.Config.SITES)),
            'date': pa.Column(pa.typing.DateTime),
            'start_time': pa.Column(float, nullable=True),
            'point': pa.Column(
                float, pa.Check.in_range(
                    config.Config.POINTS_RANGE['min'],
                    config.Config.POINTS_RANGE['max'])),
            'minute': pa.Column(
                float, pa.Check.in_range(
                    config.Config.MINUTES_RANGE['min'],
                    config.Config.MINUTES_RANGE['max']),
                nullable=True),
            'distance': pa.Column(
                float, pa.Check.in_range(
                    config.Config.DISTANCE_RANGE['min'],
                    config.Config.DISTANCE_RANGE['max']),
                nullable=True),
            'how': pa.Column(
                str, pa.Check.isin(config.Config.HOW.keys()), nullable=True),
            'visual': pa.Column(bool),
            'sex': pa.Column(str, pa.Check.isin(config.Config.SEX.keys())),
            'migrating': pa.Column(bool),
            'cluster_size': pa.Column(
                float, pa.Check.in_range(
                    config.Config.CLUSTER_SIZE['min'],
                    config.Config.CLUSTER_SIZE['max'])),
            'cluster_code': pa.Column(str, nullable=True),
            'notes': pa.Column(str, nullable=True),
            'observer_id': pa.Column(
                str, pa.Check.isin(config.Config.OBSERVERS))
        })
        return schema

    def validate(self):
        """Validate the dataframe."""
        if self.schema == 'point count':
            point_count_schema = self.point_count_schema()
            point_count_schema(self.df)
            config.logger.info('[STATUS] Validated dataframe.')
        else:
            raise KeyError(f'Invalid schema "{self.schema}".')


def validate_dataframe(storage_adapter: Optional = None):
    """Sandbox to test dataframe validation.

    Args:
        storage_adapter: Storage adapter used to read/write data.
    """
    storage_adapter = storage_adapter or storage.get_storage()
    df = storage_adapter.read_file('data/source/point_counts_2020-06-21.csv')
    DataFrameValidator(df=df, schema='point count')


if __name__ == '__main__':
    validate_dataframe()

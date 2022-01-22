

import pandas as pd
import pandera as pa
from pandera.typing import DateTime


from config import Config


class DataFrameValidator:
    """Validate the contents of a dataframe based on a pre-defined schema."""
    def __init__(self, df: pd.DataFrame, schema: str):
        """Initiate DataFrameValidator instance.

        Args:
            df (pd.DataFrame): Dataframe to validate
            schema (str): Pre-defined schema to use; possible values: 'point count'
        """
        self.df = df
        self.schema = schema

    @staticmethod
    def point_count_schema():
        """Schema for ingested point count data."""
        schema = pa.DataFrameSchema({
            'observer_id': pa.Column(str, pa.Check.isin(Config.OBSERVERS)),
            'year': pa.Column(float, pa.Check.in_range(Config.YEAR_RANGE['min'], Config.YEAR_RANGE['max'])),
            'month': pa.Column(float, pa.Check.in_range(Config.MONTH_RANGE['min'], Config.MONTH_RANGE['max'])),
            'day': pa.Column(float, pa.Check.in_range(Config.DAY_RANGE['min'], Config.DAY_RANGE['max'])),
            'site_id': pa.Column(str, pa.Check.isin(Config.SITES)),
            'start_time': pa.Column(object, nullable=True),
            'point': pa.Column(float, pa.Check.in_range(Config.POINTS_RANGE['min'], Config.POINTS_RANGE['max'])),
            'minute': pa.Column(float,
                                pa.Check.in_range(Config.MINUTES_RANGE['min'], Config.MINUTES_RANGE['max']),
                                nullable=True),
            'species_code': pa.Column(str),
            'distance': pa.Column(float,
                                  pa.Check.in_range(Config.DISTANCE_RANGE['min'], Config.DISTANCE_RANGE['max']),
                                  nullable=True),
            'how': pa.Column(str, pa.Check.isin(Config.HOW), nullable=True),
            'visual': pa.Column(str, nullable=True),
            'sex': pa.Column(str, pa.Check.isin(Config.SEX)),
            'migrating': pa.Column(str, nullable=True),
            'cluster_size': pa.Column(float, pa.Check.in_range(Config.CLUSTER_SIZE['min'], Config.CLUSTER_SIZE['max'])),
            'cluster_code': pa.Column(str, nullable=True),
            'notes': pa.Column(str, nullable=True),

        })
        return schema

    @staticmethod
    def point_count_transformed_schema():
        """Schema for transformed point count data."""
        schema = pa.DataFrameSchema({
            'site_id': pa.Column(str, pa.Check.isin(Config.SITES)),
            'date': pa.Column(DateTime),
            'start_time': pa.Column(float, nullable=True),
            'point': pa.Column(float, pa.Check.in_range(Config.POINTS_RANGE['min'], Config.POINTS_RANGE['max'])),
            'minute': pa.Column(float,
                                pa.Check.in_range(Config.MINUTES_RANGE['min'], Config.MINUTES_RANGE['max']),
                                nullable=True),
            'distance': pa.Column(float,
                                  pa.Check.in_range(Config.DISTANCE_RANGE['min'], Config.DISTANCE_RANGE['max']),
                                  nullable=True),
            'how': pa.Column(str, pa.Check.isin(Config.HOW), nullable=True),
            'visual': pa.Column(bool),
            'sex': pa.Column(str, pa.Check.isin(Config.SEX)),
            'migrating': pa.Column(bool),
            'cluster_size': pa.Column(float, pa.Check.in_range(Config.CLUSTER_SIZE['min'], Config.CLUSTER_SIZE['max'])),
            'cluster_code': pa.Column(str, nullable=True),
            'notes': pa.Column(str, nullable=True),
            'observer_id': pa.Column(str, pa.Check.isin(Config.OBSERVERS))
        })
        return schema

    def validate(self):
        """Validate the dataframe."""
        if self.schema == 'point count':
            point_count_schema = self.point_count_schema()
            point_count_schema(self.df)
        else:
            raise KeyError(f'Invalid schema "{self.schema}"')


def validate_dataframe():
    """Factory to validate the contents of a dataframe based on a pre-defined schema."""
    pass


if __name__ == '__main__':
    validate_dataframe()

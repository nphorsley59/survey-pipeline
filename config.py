"""
Stores setup configurations for tools such as logging and pandas, as well as a
Config class, which contains codebase-level constants.
"""


import os
import pandas as pd
import yaml


import logging.config


# Logging setup
with open(os.path.join(
        os.path.dirname(__file__), './logging.yaml'), 'r') as stream:
    logging_config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(logging_config)
logger = logging.getLogger('MAIN')


# Pandas setup
pd.options.display.max_columns = None
pd.options.display.max_rows = 300
pd.options.mode.chained_assignment = None
pd.set_option('display.width', 500)


# Configs
class Config:
    # Settings
    PROJECT_DIR = os.path.dirname(__file__)
    DEFAULT_STORAGE = 'local'
    # Source file paths
    POINT_COUNT_SOURCES = ['data/source/point_counts_2021-07-02.csv',
                           'data/source/point_counts_2020-06-21.csv']
    POINT_COUNTS_INGESTED = ['data/ingested/point_counts_2021-07-02.pkl',
                             'data/ingested/point_counts_2020-06-21.pkl']
    # Validation constants and mapping
    OBSERVERS = {
        'CKD': 'Colin Dobson',
        'NPH': 'Noah Horsley'
    }
    SITES = {
        'CC': 'Cow Creek Ranch',
        'CT': 'Craver Trust',
        'RW': 'R Wildflower & Fields',
        'JW': 'J&W Ranch',
        'DQ': 'D&Q Ranch'
    }
    HOW = {
        'V': 'Visual',
        'S': 'Singing',
        'C': 'Calling',
        'O': 'Other'
    }
    SEX = {
        'M': 'Male',
        'F': 'Female',
        'J': 'Juvenile',
        'U': 'Unknown'
    }
    YEAR_RANGE = {'min': 2020, 'max': 2022}
    MONTH_RANGE = {'min': 1, 'max': 12}
    DAY_RANGE = {'min': 1, 'max': 31}
    POINTS_RANGE = {'min': 1, 'max': 88}
    MINUTES_RANGE = {'min': 1, 'max': 6}
    DISTANCE_RANGE = {'min': 0, 'max': 1000}
    CLUSTER_SIZE = {'min': 1, 'max': 1000}
    # Schemas
    SCHEMA_POINT_COUNT_INGEST = {
        'observer_id': {
            'type': object,
            'required': False,
            'default': None},
        'year': {
            'type': float,
            'required': True,
            'default': None},
        'month': {
            'type': float,
            'required': True,
            'default': None},
        'day': {
            'type': float,
            'required': True,
            'default': None},
        'site_id': {
            'type': object,
            'required': True,
            'default': None},
        'start_time': {
            'type': object,
            'required': False,
            'default': '00:00'},
        'point': {
            'type': float,
            'required': True,
            'default': None},
        'minute': {
            'type': float,
            'required': False,
            'default': None},
        'species_code': {
            'type': object,
            'required': True,
            'default': None},
        'distance': {
            'type': float,
            'required': False,
            'default': None},
        'how': {
            'type': object,
            'required': False,
            'default': None},
        'visual': {
            'type': object,
            'required': False,
            'default': None},
        'sex': {
            'type': object,
            'required': False,
            'default': 'U'},
        'migrating': {
            'type': object,
            'required': False,
            'default': None},
        'cluster_size': {
            'type': float,
            'required': False,
            'default': 1},
        'cluster_code': {
            'type': object,
            'required': False,
            'default': None},
        'notes': {
            'type': object,
            'required': False,
            'default': None}
    }
    SCHEMA_POINT_COUNT_TRANSFORM = {
        'observer_id': {
            'type': object},
        'observer': {
            'type': object},
        'site_id': {
            'type': object},
        'site': {
            'type': object},
        'date': {
            'type': 'datetime64[ns]'},
        'start_time': {
            'type': float},
        'point': {
            'type': float},
        'minute': {
            'type': float},
        'species_code': {
            'type': object},
        'species': {
            'type': object},
        'distance': {
            'type': float},
        'how': {
            'type': object},
        'visual': {
            'type': bool},
        'sex': {
            'type': object},
        'migrating': {
            'type': bool},
        'cluster_size': {
            'type': float},
        'cluster_code': {
            'type': object},
        'notes': {
            'type': object}
    }


if __name__ == '__main__':
    pass

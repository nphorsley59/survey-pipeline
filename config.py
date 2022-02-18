"""Docstring"""


import logging.config
import os
import pandas as pd
import yaml


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
    PROJECT_DIR = os.path.dirname(__file__)
    COLUMN_NAMES = [
        'observer_id', 'year', 'month', 'day', 'site_id', 'start_time', 'point',
        'minute', 'species_code', 'distance', 'how', 'visual', 'sex', 'migrating',
        'cluster_size', 'cluster_code', 'notes'
    ]
    PROCESSED_POINT_COUNTS_COLUMNS = [
        'observer_id', 'site_id', 'date', 'start_time', 'point', 'minute',
        'species_code', 'distance', 'how', 'visual', 'sex', 'migrating',
        'cluster_size', 'cluster_code', 'notes'
    ]
    POINT_COUNT_COLS_INGEST = {
        'observer_id': object,
        'year': float,
        'month': float,
        'day': float,
        'site_id': object,
        'start_time': object,
        'point': float,
        'minute': float,
        'species_code': object,
        'distance': float,
        'how': object,
        'visual': object,
        'sex': object,
        'migrating': object,
        'cluster_size': float,
        'cluster_code': object,
        'notes': object
    }
    POINT_COUNT_COLUMNS_OUT = {'site_id',
                               'date',
                               'start_time',
                               'point',
                               'minute',
                               'species_code',
                               'distance',
                               'how',
                               'visual',
                               'sex',
                               'migrating',
                               'cluster_size',
                               'cluster_code',
                               'notes',
                               'observer_id'}
    OBSERVERS = {'CKD'}
    SITES = {'CC', 'CT', 'RW', 'JW', 'DQ'}
    HOW = {'V': 'Visual', 'S': 'Singing', 'C': 'Calling', 'O': 'Other'}
    SEX = {'M': 'Male', 'F': 'Female', 'J': 'Juvenile', 'U': 'Unknown'}
    AUTO_FILL_CAT_COLS = {'observer_id'}
    CAT_COLS = {'observer_id', 'site_id', 'species_code', 'how', 'sex'}
    BOOL_COLS = {'visual', 'migrating'}
    YEAR_RANGE = {'min': 2020, 'max': 2022}
    MONTH_RANGE = {'min': 1, 'max': 12}
    DAY_RANGE = {'min': 1, 'max': 31}
    POINTS_RANGE = {'min': 1, 'max': 88}
    MINUTES_RANGE = {'min': 1, 'max': 6}
    DISTANCE_RANGE = {'min': 0, 'max': 1000}
    CLUSTER_SIZE = {'min': 1, 'max': 1000}
    NUM_COLS = ['point', 'minute', 'distance', 'cluster_size']
    REQUIRED_COLS = ['year', 'month', 'day', 'site_id',
                     'point', 'species_code']
    NULL_DEFAULTS = {'cluster_size': 1,
                     'start_time': '00:00',
                     'sex': 'U'}
    POINT_COUNT_SOURCES = ['data/source/point_counts_2021-07-02.csv',
                           'data/source/point_counts_2020-06-21.csv']
    POINT_COUNTS_INGESTED = ['data/ingested/point_counts_2021-07-02.pkl',
                             'data/ingested/point_counts_2020-06-21.pkl']
    DEFAULT_STORAGE = 'local'

    # SPECIES_CODE_PATH = './data/cleaned/species_codes.json'
    # SPECIES_CODES = list(pd.DataFrame \
    #         .from_dict(load_json(SPECIES_CODE_PATH), orient='index') \
    #         .reset_index()['index'].unique())


if __name__ == '__main__':
    pass

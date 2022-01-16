

import logging.config
import os
import pandas as pd
import yaml


# Logging
with open(os.path.join(os.path.dirname(__file__), './logging.yaml'), 'r') as stream:
    logging_config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(logging_config)
logger = logging.getLogger('MAIN')


# Pandas
pd.options.display.max_columns = None
pd.options.display.max_rows = 300
pd.options.mode.chained_assignment = None
pd.set_option('display.width', 500)


class Config:
    PROJECT_DIR = os.path.dirname(__file__)
    COLUMN_NAMES = ['observer_id', 'year', 'month', 'day', 'site_id',
                    'start_time', 'point', 'minute', 'species_code', 'distance',
                    'how', 'visual', 'sex', 'migrating', 'cluster_size',
                    'cluster_code', 'notes']
    POINT_COUNT_COLUMNS = ['site_id', 'date', 'start_time', 'point', 'minute', 'species_code', 'distance', 'how',
                           'visual', 'sex', 'migrating', 'cluster_size', 'cluster_code', 'notes', 'observer_id']
    OBSERVERS = {'CKD'}
    SITES = {'CC', 'CT', 'RW', 'JW', 'DQ'}
    HOW = {'V', 'S', 'C', 'O'}
    SEX = {'M', 'F', 'J', 'U'}
    AUTO_FILL_CAT_COLS = {'observer_id'}
    CAT_COLS = {'observer_id', 'site_id', 'species_code', 'how', 'sex'}
    BOOL_COLS = {'visual', 'migrating'}
    POINTS_RANGE = {'min': 1, 'max': 88}
    MINUTES_RANGE = {'min': 1, 'max': 6}
    DISTANCE_RANGE = {'min': 0, 'max': 1000}
    CLUSTER_SIZE = {'min': 1, 'max': 1000}
    NUM_COLS = ['point', 'minute', 'distance', 'cluster_size']
    REQUIRED_COLS = {'year', 'month', 'day', 'site_id', 'point', 'species_code'}
    NULL_DEFAULTS = {'cluster_size': 1,
                     'start_time': '00:00',
                     'sex': 'U',
                     'cluster_code': 'NaN',
                     'notes': 'NaN'}
    # SPECIES_CODE_PATH = './data/cleaned/species_codes.json'
    # SPECIES_CODES = list(pd.DataFrame \
    #         .from_dict(load_json(SPECIES_CODE_PATH), orient='index') \
    #         .reset_index()['index'].unique())


if __name__ == '__main__':
    pass

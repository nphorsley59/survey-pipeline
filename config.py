

import logging
import os


# Logging options
log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger()
# Log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
# Allow log level to be set, but only to DEBUG or INFO
logger.level = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO}[os.environ.get('LOG_LEVEL', 'INFO')]


class Config:
    PROJECT_DIR = os.path.dirname(__file__)
    COLUMN_NAMES = ['observer_id', 'year', 'month', 'day', 'site_id',
                    'start_time', 'point', 'minute', 'species_code', 'distance',
                    'how', 'visual', 'sex', 'migrating', 'cluster_size',
                    'cluster_code', 'notes']
    OBSERVERS = ['CKD']
    SITES = ['CC', 'CT', 'RW', 'JW', 'DQ']
    HOW = ['V', 'S', 'C', 'O']
    BOOL = ['X']
    SEX = ['M', 'F', 'J']
    CAT_COLS = ['observer_id', 'site_id', 'species_code', 'how', 'visual',
                'sex', 'migrating']
    POINTS_RANGE = {'min': 1, 'max': 88}
    MINUTES_RANGE = {'min': 1, 'max': 6}
    DISTANCE_RANGE = {'min': 0, 'max': 1000}
    CLUSTER_SIZE = {'min': 1, 'max': 1000}
    NUM_COLS = ['point', 'minute', 'distance', 'cluster_size']
    REQUIRED_COLS = ['year', 'month', 'day', 'site_id', 'point',
                     'species_code']

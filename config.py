

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

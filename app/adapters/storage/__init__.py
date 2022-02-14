"""
Storage adapters are used throughout the application to read and write data. The
universal factory, get_storage(), is a concise and flexible way to retrieve
an adapter.

get_storage() should always be used in place of calling adapter directly.
"""


from app.adapters.storage.local_directory import LocalDirectory
from config import Config, logger


def get_storage(storage_type: str = None):
    """Universal factory for local and cloud storage options.

    Args:
        storage_type (str): Storage adapter; possible values: 'local'.

    Notes:
        Default adapter is defined in config.py under DEFAULT_STORAGE.
    """
    storage_type = storage_type or Config.DEFAULT_STORAGE
    if storage_type == 'local':
        logger.info('[CONNECT] Connecting to local directory...')
        return LocalDirectory()
    else:
        raise ValueError(f'Storage type {storage_type} not recognized.')

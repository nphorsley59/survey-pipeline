"""
Global function to give easy and flexible access storage adapters.
Should always be used in place of calling adapter directly.
"""


from app.adapters.storage import localdir
import config


def get_storage(storage_type: str = None):
    """Universal factory for local and cloud storage options.

    Args:
        storage_type (str): Storage adapter; possible values: 'local'.
    """
    storage_type = storage_type or config.Config.DEFAULT_STORAGE
    if storage_type == 'local':
        config.logger.info('[CONNECT] Connecting to local directory...')
        return localdir.LocalDirectory()
    else:
        raise ValueError(f'Storage type {storage_type} not recognized')

"""
This script increases the accessibility of species names mapping data.
"""


from typing import Optional


import pandas as pd


from src.adapters.storage import get_storage
from config import logger


class SpeciesNames:
    """Class to store data and functionality for species name data."""

    def __init__(self, df: pd.DataFrame, storage: Optional = None):
        """Initialize SpeciesNames instance.

        Args:
            df (pd.DataFrame): Species names data.
            storage: Storage adapter used to write data.
        """
        self.df = df
        self.storage = storage

    def code_to_common_name_dict(self) -> dict:
        """Map 4-letter code to common name.

        Returns:
            {4_letter code: common_name}
        """
        logger.info('[STATUS] Retrieved dictionary (4-letter code: common name).')
        return dict(zip(self.df['4_letter_code'], self.df['common_name']))


def species_names_factory(df: Optional[pd.DataFrame] = None,
                          storage: Optional = None):
    """Factory to store data and functionality for species name data.

    Args:
        df (pd.DataFrame): Species names data.
        storage: Storage adapter used to write data.

    Notes:
        Defaults to read-only if adapter is not provided for storage.
        Pass data to df to run pipeline in memory.
    """
    logger.info('[INIT] species_name_factory()')
    read_storage = storage or get_storage()
    df = df or read_storage.read_file('data/reference/species_codes.json')
    species_names = SpeciesNames(df=df, storage=storage)
    logger.info('[PRIMED] species_name_factory()')
    return species_names


if __name__ == '__main__':
    test = species_names_factory()

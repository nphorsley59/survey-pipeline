"""
Raw point count data stores species as four-letter codes. To communicate survey
results more clearly, these codes must be converted to other naming conventions.

This class ingests a text map of species naming conventions and stores it as
a JSON nested dictionary.
"""


from typing import Optional


import pandas as pd


from app import utils
from app.adapters import storage
from config import logger


class SpeciesMapIngestor:
    """Ingest species naming conventions and return as a JSON dict."""

    def __init__(self, df: pd.DataFrame, storage_adapter):
        """Initiate SpeciesCodeIngestor instance.

        Args:
            df (pd.DataFrame): Raw species naming conventions data.
            storage_adapter: Storage adapter used to write data.
        """
        self.df = df
        self.storage_adapter = storage_adapter

    def clean_raw_text(self):
        """Remove un-needed chars and non-species records from df."""
        self.df = (
            self.df
            .pipe(utils.replace_substrings,
                  column='species', old='*', new='')
            .pipe(utils.replace_substrings,
                  column='species', old='\n', new='')
            .pipe(utils.subset_by_substring,
                  column='species', substring='\\+', keep=False)
            .pipe(utils.subset_by_substring,
                  column='species', substring='4-LETTER', keep=False)
            .pipe(utils.split_strings,
                  column='species', on=' ')
        )

    @staticmethod
    def get_code_position(df: pd.DataFrame) -> pd.DataFrame:
        """Get index of 4-letter English Code; helper function for
            parse_name_code().

        Args:
            df (pd.DataFrame): Species naming conventions dataframe.

        Returns:
            Input dataframe with additional column, `code_position`.
        """
        df['code_position'] = df['species'].map(
            lambda x: utils.index_all_caps(x))
        return df

    @staticmethod
    def get_convention_by_index(record: list, index: list,
                                convention: str) -> list[str]:
        """Index records to extract specific naming convention;
            helper function for parse_name_code().

        Args:
            record (list): Record to index.
            index (list): List of indices.
            convention (str): Naming convention, possible values:
                "common_name", "4_letter_code", "scientific_name".

        Returns:
            Species name in specified convention.
        """
        match convention:
            case "common_name":  # Example: Abert's Towhee
                return record[:index[0]]
            case "4_letter_code":  # Example: ABTO
                return record[index[0]]
            case "scientific_name":  # Example: Melozone aberti
                return record[index[0]+1:index[1]]

    def parse_text(self):
        """Parse English 4-letter Code, Common Name, and Scientific Name
            from text as columns."""
        self.df = self.get_code_position(self.df)
        # Define behavior by naming convention
        name_types = {'4_letter_code': {'join': False},
                      'common_name': {'join': True},
                      'scientific_name': {'join': True}}
        # Map new columns
        for name in name_types.keys():
            self.df[name] = self.df.apply(
                lambda x: self.get_convention_by_index(
                    x['species'], x['code_position'], name), axis=1)
            if name_types[name]['join']:
                self.df[name] = self.df[name].apply(lambda x: ' '.join(x))
        self.df = self.df[name_types.keys()]

    def export(self):
        """Export species mapping dataframe."""
        if self.storage_adapter is not None:
            self.storage_adapter.write_file(
                self.df, 'data/reference/species_codes.json')

    def ingest(self) -> pd.DataFrame:
        """Ingest species naming conventions data.

        Returns:
            Ingested species mapping dataframe.
        """
        self.clean_raw_text()
        self.parse_text()
        self.export()
        logger.info('[DONE] species_mapping_ingestor()')
        return self.df


def factory_ingest_species_map(storage_adapter: Optional = None,
                               df: Optional[pd.DataFrame] = None):
    """Factory to ingest species naming conventions.

    Args:
        storage_adapter: Storage adapter used to read/write data.
        df (pd.DataFrame): Raw species naming conventions data.

    Notes:
        Defaults to read-only if adapter is not provided for storage.
        Pass data to df to run pipeline in memory.
    """
    logger.info('[INIT] species_mapping_ingestor()')
    read_storage = storage_adapter or storage.get_storage()
    df = df or read_storage.read_file(
        'data/source/species_codes.txt', header=['species'])
    ingestor = SpeciesMapIngestor(df=df, storage_adapter=storage_adapter)
    logger.info('[PRIMED] species_mapping_ingestor()')
    return ingestor


if __name__ == '__main__':
    test = factory_ingest_species_map(storage_adapter=storage.get_storage()).ingest()

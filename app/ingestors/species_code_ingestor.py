

import json
import os
import pandas as pd
from config import Config, logger
from app.utils import index_all_caps, replace_substrings, subset_by_substring, split_strings


class SpeciesNamingIngestor:
    """Ingest flat text file of species naming conventions and return as a JSON dict."""
    def __init__(self, df: pd.DataFrame = None, save: bool = True):
        """Initiate SpeciesCodeIngestor instance.

        Args:
            df (pd.DataFrame): Dataframe containing raw species naming conventions data
            save (bool): Export dataframe as JSON (T/F)
        """
        self.df = df
        self.save = save

    def clean_raw_text(self):
        """Remove un-needed chars and non-species records from df."""
        self.df = (
            self.df
            .pipe(replace_substrings, column='species', old='*', new='')
            .pipe(replace_substrings, column='species', old='\n', new='')
            .pipe(subset_by_substring, column='species', substring='\\+', keep=False)
            .pipe(subset_by_substring, column='species', substring='4-LETTER', keep=False)
            .pipe(split_strings, column='species', on=' ')
        )

    @staticmethod
    def get_code_position(df: pd.DataFrame) -> pd.DataFrame:
        """Get index of 4-letter English Code; helper function for parse_name_code().

        Args:
            df (pd.DataFrame): Species naming conventions dataframe
        """
        df['code_position'] = df['species'].map(lambda x: index_all_caps(x))
        return df

    @staticmethod
    def split_on_index(species_names: list, index: list, column: str) -> list[str]:
        """Split records on index; helper function for parse_name_code().

        Args:
            species_names (list): Species described using multiple naming conventions
            index (list): Species code position within the list of names
            column (str): Column describing the desired naming convention
        """
        if column == 'common_name':
            return species_names[:index[0]]
        elif column == '4_letter_code':
            return species_names[index[0]]
        elif column == 'scientific_name':
            return species_names[index[0]+1:index[1]]

    def parse_name_code(self):
        """Parse English 4-letter Code, Common Name, and Scientific Name as columns."""
        self.df = self.get_code_position(self.df)
        name_types = {'4_letter_code': {'join': False},
                      'common_name': {'join': True},
                      'scientific_name': {'join': True}}
        for name in name_types.keys():
            self.df[name] = self.df.apply(lambda x: self.split_on_index(x['species'], x['code_position'], name), axis=1)
            if name_types[name]['join']:
                self.df[name] = self.df.apply(lambda x: ' '.join(x))
        self.df = self.df[[name_types.keys()]]

    def export(self):
        """Export dataframe as JSON."""
        out_json = json.dumps(self.df.T.to_dict())
        out_path = os.path.join(Config.PROJECT_DIR, 'data/reference/species_codes.json')
        with open(out_path, 'w') as f:
            json.dump(out_json, f)

    def ingest(self):
        """Ingest species codes."""
        self.clean_raw_text()
        self.parse_name_code()
        self.export()


def ingest_species_mapping(save: bool = True):
    """Factory to ingest flat text file of species naming conventions and return as a JSON dict.

    Args:
        save (bool): Export dataframe as JSON (T/F)
    """
    logger.info('[START ] ingest_species_mapping()')
    # read text file
    in_path = os.path.join(Config.PROJECT_DIR, 'data/raw/species_codes.txt')
    with open(in_path, 'r') as f:
        text = f.readlines()
        df = pd.DataFrame(text, columns=['species'])
    # ingest
    ingestor = SpeciesNamingIngestor(df=df, save=save)
    ingestor.ingest()
    logger.info('[FINISH] ingest_species_mapping()')


if __name__ == '__main__':
    ingest_species_mapping()

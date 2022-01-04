

import os
import numpy as np
import pandas as pd
from config import Config
from app.utils import replace_substrings, subset_by_substring, split_strings


def clean_raw_text(in_df: pd.DataFrame) -> pd.DataFrame:
    """Remove un-needed chars and non-species records from df."""
    out_df = (
        in_df
        .pipe(replace_substrings, column='species', old='*', new='')
        .pipe(replace_substrings, column='species', old='\n', new='')
        .pipe(subset_by_substring, column='species', substring='\\+', keep=False)
        .pipe(subset_by_substring, column='species', substring='4-LETTER', keep=False)
        .pipe(split_strings, column='species', on=' ')
    )
    return out_df


def get_code_position():
    """Docstring"""
    items = ['red', 'REd', 'RED']
    result = [x.isupper() for x in items]
    indexes = np.where(result)[0]
    print(indexes)


def extract_name_code():
    """Docstring"""
    pass


def ingest_species_codes():
    """Ingest text file of species information and return JSON dict to map 4-letter code to common name."""
    path = os.path.join(Config.PROJECT_DIR, 'data/raw/species_codes.txt')
    with open(path, 'r') as f:
        text = f.readlines()
        df = pd.DataFrame(text, columns=['species'])
        clean_raw_text(df)


if __name__ == '__main__':
    ingest_species_codes()
    get_code_position()



import json
import os
import pandas as pd
from config import Config, logger
from app.utils import index_all_caps, replace_substrings, subset_by_substring, split_strings


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


def get_code_position(in_df: pd.DataFrame) -> pd.DataFrame:
    """Get index of 4-letter English Code; helper function for parse_name_code()."""
    out_df = in_df.copy()
    out_df['code_position'] = out_df['species'].map(lambda x: index_all_caps(x))
    return out_df


def split_on_index(a_list: list, index: list, column: str) -> list[str]:
    """Split records on index; helper function for parse_name_code()."""
    if column == 'common_name':
        return a_list[:index[0]]
    elif column == '4_letter_code':
        return a_list[index[0]]
    elif column == 'scientific_name':
        return a_list[index[0]+1:index[1]]


def parse_name_code(in_df: pd.DataFrame) -> pd.DataFrame:
    """Parse English 4-letter Code, Common Name, and Scientific Name as columns."""
    out_df = get_code_position(in_df)
    code = '4_letter_code'
    name = 'common_name'
    sci = 'scientific_name'
    out_df[code] = out_df.apply(lambda x: split_on_index(x['species'], x['code_position'], code), axis=1)
    out_df[name] = out_df.apply(lambda x: split_on_index(x['species'], x['code_position'], name), axis=1)
    out_df[name] = out_df[name].apply(lambda x: ' '.join(x))
    out_df[sci] = out_df.apply(lambda x: split_on_index(x['species'], x['code_position'], sci), axis=1)
    out_df[sci] = out_df[sci].apply(lambda x: ' '.join(x))
    return out_df[[code, name, sci]]


def factory_ingest_species_codes():
    """Ingest text file of species information and return JSON dict to map 4-letter code to common name."""
    logger.info('ingest_species_codes() starting...')
    # read text file
    in_path = os.path.join(Config.PROJECT_DIR, 'data/raw/species_codes.txt')
    with open(in_path, 'r') as f:
        text = f.readlines()
        in_df = pd.DataFrame(text, columns=['species'])
    logger.info(f'\nINPUT:\n{in_df.head(5)}')
    # process raw df
    df = (
        in_df
        .pipe(clean_raw_text)
        .pipe(parse_name_code)
    )
    logger.info(f'\nOUTPUT:\n{df.head(5)}')
    # write to json
    out_json = json.dumps(df.T.to_dict())
    out_path = os.path.join(Config.PROJECT_DIR, 'data/reference/species_codes.json')
    with open(out_path, 'w') as f:
        json.dump(out_json, f)
    logger.info('ingest_species_codes() complete!')


if __name__ == '__main__':
    factory_ingest_species_codes()

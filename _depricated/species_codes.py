

import json
import os
import pandas as pd
import sys


# == Locate Root Dir == #
flare = '\\flare.py'
path = os.getcwd()
while not os.path.isfile(path + flare):
    path = os.path.dirname(path)
sys.path.append(path)


# == Local Modules == #
from functions.processStringsInDf import *


# == Functions == #
# transforms txt data to a pandas dataframe
def text_to_dataframe(text, col_name):
    return pd.DataFrame(text, columns=[col_name])

# categorizes a species' naming convention
# used to locate specific pieces of information in full species string
def classify_naming_convention(df):
    df['name_class'] = df['species'].apply(lambda x: len(x))
    return df[df['name_class'] < 8]

# determines position of information during extraction
# helper function for extract_fourletter_code and extract_english_name
def specify_position(name_class_value, adjustment):
    return name_class_value - adjustment

# extracts a species` four-letter code as a new column
def extract_fourletter_code(df, adjustment):
    df['fourletter_code'] = df.apply(
        lambda x: x['species'][specify_position(x['name_class'], adjustment)], axis=1
    )
    return df

# extracts a species` english name as a new column
def extract_english_name(df, adjustment):
    df['english_name'] = df.apply(
        lambda x: ' '.join(x['species'][: specify_position(x['name_class'], adjustment)]), axis=1
    )
    return df

# extracts a species` scientific name as a new column
def extract_scientific_name(df):
    df['scientific_name'] = df['species'].apply(lambda x: ' '.join(x[-3: -1]))
    return df


# == Load and Process species_codes.txt == #
# open, read, store as dataframe, and close a text file
path = '/data/raw/species_codes.txt'
with open(path, 'r') as f:
    text = f.readlines()
    df = text_to_dataframe(text, 'species')

# process species data in dataframe
bird_codes_df = (
    df.pipe(replace_substrings, 'species', '*', '')
        .pipe(replace_substrings, 'species', '\n', '')
        .pipe(subset_by_substring, 'species', '\+', False)
        .pipe(split_strings, 'species', ' ')
        .pipe(classify_naming_convention)
        .pipe(extract_fourletter_code, 4)
        .pipe(extract_english_name, 4)
        .pipe(extract_scientific_name)
        .drop(['species', 'name_class'], axis=1)
        .set_index('fourletter_code')
)


# == Transform to JSON and Write == #
bird_codes_dict = bird_codes_df.T.to_dict()
bird_codes_json = json.dumps(bird_codes_dict)
path = '/data/cleaned/species_codes.json'
with open(path, 'w') as f:
    json.dump(bird_codes_json, f)
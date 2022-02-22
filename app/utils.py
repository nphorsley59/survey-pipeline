"""
This script stores generic functionalities that may be broadly applicable within
the codebase.
"""


import os


import numpy as np
import pandas as pd


def replace_substrings(df: pd.DataFrame,
                       column: str,
                       old: str,
                       new: str) -> pd.DataFrame:
    """Replaces a substring with a new substring anywhere it occurs in a
    DataFrame column.

    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df with dtype str.
        old (str): Substring to be replaced.
        new (str): Substring to replace old with.

    Returns:
        df (pd.DataFrame)
    """
    df[column] = df[column].apply(lambda x: x.replace(old, new))
    return df


def subset_by_substring(df: pd.DataFrame,
                        column: str,
                        substring: str,
                        keep: bool = True) -> pd.DataFrame:
    """Subsets rows of a DataFrame on the presence/absence of a substring.

    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df with dtype str.
        substring (str): Substring to subset rows on.
        keep (bool, default=True): Subset by presence or absence of
            substring.

    Returns:
        df (pd.DataFrame)
    """
    if keep:
        return df[df[column].str.contains(substring)].copy()
    else:
        return df[~df[column].str.contains(substring)].copy()


def split_strings(df: pd.DataFrame,
                  column: str,
                  on: str) -> pd.DataFrame:
    """Splits strings in column into list on separator.

    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df with dtype str.
        on (str): Substring to separate strings on.

    Returns:
        df (pd.DataFrame)
    """
    df[column] = df[column].apply(lambda x: x.split(on))
    return df


def get_index_for_upper_str(a_list: list[str]) -> list[int]:
    """Get indexes for list elements in all caps."""
    is_all_caps = [ele.isupper() for ele in a_list]
    return np.where(is_all_caps)[0]


def delete_file(write_path):
    if os.path.isfile(write_path):
        os.remove(write_path)

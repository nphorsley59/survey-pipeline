

import numpy as np
import pandas as pd
import time


def number_in_range(x, minimum, maximum):
    return minimum <= x <= maximum


def yes_no_input(prompt):
    time.sleep(1)
    while True:
        user_input = input(f"{prompt} (Y/N) ")
        if user_input == "Y":
            return True
        elif user_input == "N":
            return False
        else:
            print("Invalid input...")
            continue


def valid_dtype(dtype):
    accepted_dtypes = ['float64', 'bool', 'int64', 'object', 'datetime64',
                       'timedelta[ns]', 'category']
    return dtype in accepted_dtypes


def change_dtype(df: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    """Changes data type of a column.

    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df.
        dtype (str): New data type for column.

    Returns:
        df (pd.DataFrame)
    """
    if not valid_dtype(dtype):
        print("Invalid data type.")
        exit()
    if dtype == 'int64':
        pd.to_numeric(df[column], errors='coerce').astype(int)
    else:
        df[column] = df[column].astype(dtype)
    return df


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


def index_all_caps(a_list: list[str]) -> list[int]:
    """Get indexes for list elements in all caps."""
    is_all_caps = [ele.isupper() for ele in a_list]
    return np.where(is_all_caps)[0]


def string_case(df: pd.DataFrame, columns: list, case: str) -> pd.DataFrame:
    """Converts string columns to desired case.

    Args:
        df (pd.DataFrame)
        columns (list): Target column(s) in df.
        case (str): Desired case; "upper" or "lower".

    Returns:
        df (pd.DataFrame)
    """
    for column in columns:
        if case == 'upper':
            df[column] = df[column].apply(lambda x: x.str.upper())
        elif case == 'lower':
            df[column] = df[column].apply(lambda x: x.str.lower())
        else:
            print(f"Invalid case ({case}) provided.")
    return df

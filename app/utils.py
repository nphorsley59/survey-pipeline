

import pandas as pd


def number_in_range(x, minimum, maximum):
    return minimum <= x <= maximum


def yes_no(prompt):
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
                        contains: bool = True) -> pd.DataFrame:
    """Subsets rows of a DataFrame on the presence/absence of a substring.

    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df with dtype str.
        substring (str): Substring to subset rows on.
        contains (bool, default=True): Subset by presence or absence of
            substring.

    Returns:
        df (pd.DataFrame)

    """
    if contains:
        return df[df[column].str.contains(substring)].copy()
    else:
        return df[~df[column].str.contains(substring)].copy()


def split_strings(df: pd.DataFrame,
                  column: str,
                  separator: str) -> pd.DataFrame:
    """Splits strings in column into list on separator.

    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df with dtype str.
        separator (str): Substring to separate strings on.

    Returns:
        df (pd.DataFrame)

    """
    df[column] = df[column].apply(lambda x: x.split(separator))
    return df

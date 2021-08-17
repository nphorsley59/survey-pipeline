# ============================================================================
# == Global Libraries == #
import pandas as pd
import json


# ============================================================================
# == Functions == #
def get_columns(df: pd.DataFrame) -> list:
    """Extract columns from pandas df as list."""
    return df.columns


def load_csv(path: str, column_names: list) -> pd.DataFrame:
    """Load .csv file as a pandas df.
    
    Args:
        path (str): Path to .csv file.
        column_names (list): Column names to use.
    
    Returns:
        df (pd.DataFrame)
    """
    return pd.read_csv(path, header=0, names=column_names)


def load_json(path: str) -> dict:
    """Load .json file as a dictionary.
    
    Args:
        path (str): Path to .json file.
    
    Returns:
        json_dict (dict)
    """
    with open(path, 'r') as f:
        json_string = json.load(f)
        json_dict = json.loads(json_string)
    return json_dict


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

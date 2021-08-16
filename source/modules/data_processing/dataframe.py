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
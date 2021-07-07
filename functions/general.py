# == Global Libraries == #
import json
import pandas as pd


# == Functions == #
def load_csv(path: str) -> pd.DataFrame:
    """Loads CSV file as pandas DataFrame.
    
    Args:
        path (str): Path to CSV file.
    
    Returns:
        df (pd.DataFrame)
    
    """
    return pd.read_csv(path)

def load_json(path: str) -> dict:
    """Loads JSON file as dictionary.
    
    Args:
        path (str): Path to JSON file.
    
    Returns:
        json_dict (dict)
    
    """
    with open(path, 'r') as f:
        json_string = json.load(f)
        json_dict = json.loads(json_string)
        
    return json_dict

def change_dtype(df: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    """Changes data type of a column.
    
    Args:
        df (pd.DataFrame)
        column (str): Name of target column in df.
        dtype (str): New data type for column.
    
    Returns:
        df (pd.DataFrame)
    
    """
    df[column] = df[column].astype(dtype)
    return df
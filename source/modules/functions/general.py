# ============================================================================
# == Global Libraries == #
import pandas as pd


# ============================================================================
# == Functions == #
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



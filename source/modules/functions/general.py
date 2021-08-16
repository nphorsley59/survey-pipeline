# ============================================================================
# == Global Libraries == #
import pandas as pd


# ============================================================================
# == Functions == #
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
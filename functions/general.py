# == Global Libraries == #
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
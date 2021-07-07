# == Global Libraries == #
import pandas as pd
import os
import sys


# == Functions == #
def replace_substring(df: pd.DataFrame, 
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

def split_string(df: pd.DataFrame, 
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
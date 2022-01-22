

import json
import os
import pandas as pd
from pathlib import Path
from typing import Optional


from config import Config


class LocalFolder:
    @staticmethod
    def read_file(relative_path: str, header: Optional[list] = None) -> pd.DataFrame:
        """Interpret relative path and read file type to pandas dataframe.

        Args:
            relative_path (str): Relative path to read location
            header (list): Optional argument to specify dataframe header

        Returns:
            Pandas dataframe or dictionary, depending on the file type
        """
        absolute_path = os.path.join(Config.PROJECT_DIR, relative_path)
        extension = Path(absolute_path).suffix
        match extension:
            case ".csv":
                return pd.read_csv(absolute_path, header=header)
            case ".pkl":
                return pd.read_pickle(absolute_path, header=header)
            case ".json":
                with open(absolute_path, 'r') as f:
                    json_string = json.load(f)
                    json_dict = json.loads(json_string)
                    return pd.DataFrame.from_dict(json_dict, orient='index', columns=header)
            case other:
                raise KeyError(f'Unsupported file type "{extension}"')

    @staticmethod
    def write_file(df: pd.DataFrame, relative_path: str):
        """Interpret relative path and write file type to location.

        Args:
            df (pd.DataFrame): Dataframe to write
            relative_path (str): Relative path to write location
        """
        absolute_path = os.path.join(Config.PROJECT_DIR, relative_path)
        extension = Path(absolute_path).suffix
        match extension:
            case ".csv":
                return pd.to_csv(df, absolute_path, index=False)
            case ".pkl":
                return pd.to_pickle(df, absolute_path)
            case ".json":
                json_dict = json.dumps(df.T.to_dict())
                with open(absolute_path, 'w') as f:
                    json.dump(json_dict, f)
            case other:
                raise KeyError(f'Unsupported file type "{extension}"')

"""
Storage adapter to read and write data from the local directory.

Can read and write the following file types:
    - .csv
    - .json
    - .pkl
    - .txt (read only)

File type is interpreted automatically and the local directory defaults
to the PROJECT_DIR object defined in config.py.
"""


import json
import os
import pathlib
from typing import Optional


import pandas as pd


from config import Config, logger


class LocalDirectory:
    """Class to read and write data from the local directory."""

    def __init__(self, directory: Optional[str] = None):
        """Initialize LocalDirectory instance."""
        self.directory = directory or Config.PROJECT_DIR

    def get_path_attrs(self, relative_path: str) -> tuple:
        """Convert relative path to an absolute path and extract extension.

        Args:
            relative_path (str): Relative path to read/write location.

        Notes:
            Helper method for read_file and write_file.
        """
        absolute_path = os.path.join(self.directory, relative_path)
        extension = pathlib.Path(absolute_path).suffix
        return absolute_path, extension

    def read_file(self, relative_path: str,
                  header: Optional[list] = None) -> pd.DataFrame:
        """Interpret relative path and read file type to pandas dataframe.

        Args:
            relative_path (str): Relative path to read location.
            header (list): Optional argument to specify dataframe header.

        Returns:
            Pandas dataframe or dictionary, depending on the file type.
        """
        logger.info(f'[READ] {relative_path}')
        absolute_path, extension = self.get_path_attrs(relative_path=relative_path)
        # Infer file type from extension and read
        match extension:
            case ".csv":
                header = header or 'infer'
                return pd.read_csv(absolute_path, header=header)
            case ".json":
                with open(absolute_path, 'r') as f:
                    json_string = json.load(f)
                    json_dict = json.loads(json_string)
                    return pd.DataFrame.from_dict(
                        json_dict, orient='index', columns=header)
            case ".pkl":
                return pd.read_pickle(absolute_path)
            case ".txt":
                with open(absolute_path, 'r') as f:
                    text = f.readlines()
                    return pd.DataFrame(text, columns=header)
            case _:
                raise KeyError(f'Unsupported file type "{extension}"')

    def write_file(self, df: pd.DataFrame, relative_path: str):
        """Interpret relative path and write file type to location.

        Args:
            df (pd.DataFrame): Dataframe to write.
            relative_path (str): Relative path to write location.
        """
        logger.info(f'[WRITE] {relative_path}')
        absolute_path, extension = self.get_path_attrs(relative_path=relative_path)
        # Infer file type from extension and write
        match extension:
            case ".csv":
                return df.to_csv(absolute_path, index=False)
            case ".pkl":
                return df.to_pickle(absolute_path)
            case ".json":
                json_dict = json.dumps(df.T.to_dict())
                with open(absolute_path, 'w') as f:
                    json.dump(json_dict, f)
            case _:
                raise KeyError(f'Unsupported file type "{extension}"')


def factory_local_directory() -> LocalDirectory:
    """Factory to read and write data from the local directory.

    Returns:
        LocalDirectory instance.
    """
    storage = LocalDirectory()
    return storage


if __name__ == '__main__':
    test = factory_local_directory()

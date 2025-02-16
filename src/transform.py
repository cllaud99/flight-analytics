import os
import sys

import pandas as pd

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from src.config_logger import logger_decorator


@logger_decorator
def append_dataframes_to_parquet(
    dataframes: list[pd.DataFrame], output_path: str
) -> pd.DataFrame:
    """
    Recebe uma lista de DataFrames concatena e os salva em um arquivo Parquet.
    Args:
        dataframes (list[pd.DataFrame]): Lista de DataFrames a serem concatenados.
        output_path (str): Caminho para salvar o arquivo Parquet.
    """
    df = pd.concat(dataframes)
    df.to_parquet(output_path)
    return df

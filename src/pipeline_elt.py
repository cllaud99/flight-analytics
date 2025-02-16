import os
import sys
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from transform import append_dataframes_to_parquet
from models import validate
from scraper_links import main_download

bronze_file_path = "data/bronze"

#main_download()


def get_dataframes_from_path(bronze_file_path: str) -> list[pd.DataFrame]:
    """
    Recebe um caminho, valida todos os modelos e devolve uma lista de DataFrames.
    
    Args:
        bronze_file_path (str): Caminho para a pasta com os arquivos CSV.
        
    Returns:
        list[pd.DataFrame]: Lista de DataFrames validados.
    """
    dataframes = []
    # Lista apenas os arquivos CSV para exibir a barra de progresso corretamente
    csv_files = [file for file in os.listdir(bronze_file_path) if file.endswith(".csv")]
    
    # tqdm exibirá a barra de progresso com o percentual de conclusão
    for file in tqdm(csv_files, desc="Processando CSVs", unit="arquivo"):
        file_path = os.path.join(bronze_file_path, file)
        df = validate(file_path)
        dataframes.append(df)
    
    return dataframes


if __name__ == "__main__":
    dataframes = get_dataframes_from_path(bronze_file_path)
    print(dataframes)
    append_dataframes_to_parquet(dataframes, "data/silver/voos.parquet")

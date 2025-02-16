import os
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Exibe progresso

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from src.config_logger import logger_decorator

# Diretório para salvar os arquivos
DOWNLOAD_DIR = "data/bronze"
MIN_YEAR = 2023  # Padrão, podendo ser alterado conforme necessário
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@logger_decorator
def scraper_links(
    url: str, ignorar_parent: bool = True, min_year: int = 2020
) -> tuple[list, list]:
    """
    Extrai os links de uma página web e retorna:
      - os links diretos para arquivos CSV;
      - os links para pastas (diretórios) que serão exploradas, considerando que o
        nome da pasta (se numérico) deve ser maior ou igual ao min_year.

    Args:
        url (str): URL da página da qual os links serão extraídos.
        ignorar_parent (bool): Se True, ignora o link para o diretório pai.
        min_year (int): Ano mínimo para considerar links de pastas (padrão: 2014).

    Returns:
        tuple[list, list]: Lista de links para arquivos CSV e lista de links para novas páginas.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        csv_links = set()
        page_links = set()

        for tag in soup.find_all("a", href=True):
            link_text = tag.get_text(strip=True)
            link = urljoin(url, tag["href"])

            # Ignora o link para "To Parent Directory"
            if ignorar_parent and link_text.lower() == "[to parent directory]":
                continue

            # Se for um link para uma pasta
            if link.endswith("/"):
                # Verifica se o nome da pasta é um número e se é inferior ao ano_minimo
                if link_text.isdigit() and int(link_text) < min_year:
                    continue
                page_links.add(link)
            # Se for um link para um arquivo CSV
            elif link.endswith(".csv"):
                csv_links.add(link)

        return list(csv_links), list(page_links)

    except requests.RequestException:
        return [], []


@logger_decorator
def download_file(url: str, folder: str):
    """
    Faz o download de um arquivo e exibe o progresso.

    Args:
        url (str): URL do arquivo para download.
        folder (str): Caminho da pasta onde o arquivo será salvo.
    """
    try:
        filename = os.path.join(folder, os.path.basename(url))
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))

        with (
            open(filename, "wb") as file,
            tqdm(
                desc=f"Baixando {os.path.basename(url)}",
                total=total,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar,
        ):
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))

        print(f"Download concluído: {filename}")

    except requests.RequestException as e:
        print(f"Erro ao baixar {url}: {e}")


@logger_decorator
def main_download():
    """
    Função principal para buscar arquivos CSV de uma URL e baixá-los, considerando o ano mínimo.
    """
    url = "https://siros.anac.gov.br/siros/registros/diversos/vra/"

    visited_pages = set()
    pages_to_visit = [url]
    all_csv_links = set()  # Garantindo que não há duplicatas

    while pages_to_visit:
        current_page = pages_to_visit.pop(0)

        if current_page in visited_pages:
            continue

        visited_pages.add(current_page)

        csv_links, new_pages = scraper_links(
            current_page, ignorar_parent=True, min_year=MIN_YEAR
        )
        all_csv_links.update(csv_links)
        pages_to_visit.extend(new_pages)

    # Exibe a quantidade total de arquivos CSV encontrados
    total_csv = len(all_csv_links)
    print(
        f"Total de arquivos CSV únicos encontrados para anos >= {MIN_YEAR}: {total_csv}"
    )

    # Baixa todos os arquivos CSV encontrados
    for i, csv_link in enumerate(all_csv_links, start=1):
        print(f"\n[{i}/{total_csv}] Iniciando download: {os.path.basename(csv_link)}")
        download_file(csv_link, DOWNLOAD_DIR)


if __name__ == "__main__":
    main_download()

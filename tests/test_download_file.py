import os
from unittest.mock import MagicMock, mock_open, patch

import pytest
import requests

from src.scraper_links import (
    download_file,
)  # Substitua pelo caminho correto do seu módulo


@pytest.fixture
def fake_url():
    return "https://example.com/file.txt"


@pytest.fixture
def fake_folder(tmp_path):
    """Cria um diretório temporário para os testes."""
    return str(tmp_path)


@patch("requests.get")
@patch("builtins.open", new_callable=mock_open)
@patch("tqdm.tqdm")  # Evita exibição da barra de progresso
def test_download_success(mock_tqdm, mock_open_file, mock_get, fake_url, fake_folder):
    """Testa se o download é bem-sucedido e o arquivo é salvo corretamente."""
    fake_content = b"teste de conteudo"
    mock_response = MagicMock()
    mock_response.iter_content = lambda chunk_size: [fake_content]
    mock_response.headers = {"content-length": str(len(fake_content))}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    download_file(fake_url, fake_folder)

    filename = os.path.join(fake_folder, "file.txt")
    mock_open_file.assert_called_once_with(
        filename, "wb"
    )  # Verifica se o arquivo foi aberto para escrita
    mock_open_file().write.assert_called_with(
        fake_content
    )  # Verifica se o conteúdo foi gravado


@patch("requests.get", side_effect=requests.ConnectionError)
def test_download_connection_error(mock_get, fake_url, fake_folder, capsys):
    """Testa erro de conexão."""
    download_file(fake_url, fake_folder)
    captured = capsys.readouterr()
    assert "Erro ao baixar" in captured.out


@patch("requests.get")
def test_download_http_error(mock_get, fake_url, fake_folder, capsys):
    """Testa erro HTTP (exemplo: 404)."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    download_file(fake_url, fake_folder)
    captured = capsys.readouterr()
    assert "Erro ao baixar" in captured.out
    assert "404 Not Found" in captured.out


@patch("requests.get", side_effect=requests.Timeout)
def test_download_timeout(mock_get, fake_url, fake_folder, capsys):
    """Testa erro de timeout."""
    download_file(fake_url, fake_folder)
    captured = capsys.readouterr()
    assert "Erro ao baixar" in captured.out


@patch("requests.get")
@patch("builtins.open", new_callable=mock_open)
def test_download_creates_correct_filename(
    mock_open_file, mock_get, fake_url, fake_folder
):
    """Testa se o caminho correto do arquivo é gerado e o arquivo é salvo corretamente."""
    mock_response = MagicMock()
    mock_response.iter_content = lambda chunk_size: [b"data"]
    mock_response.headers = {"content-length": "4"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    download_file(fake_url, fake_folder)

    expected_path = os.path.join(fake_folder, "file.txt")
    mock_open_file.assert_called_once_with(expected_path, "wb")

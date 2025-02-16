from unittest.mock import patch

import pytest

from src.scraper_links import scraper_links  # Importando a função do módulo correto


@pytest.fixture
def html_mock():
    """HTML de teste simulando uma página com links."""
    return """
    <html>
        <body>
            <a href="https://example.com/page1/">Diretório 1</a>
            <a href="https://example.com/old/2013">Diretório antigo</a>
            <a href="/page2/">Diretório 2</a>
            <a href="https://example.com/data.csv">Arquivo CSV</a>
        </body>
    </html>
    """


@patch("requests.get")
def test_scraper_links(mock_get, html_mock):
    """Testa se a função extrai corretamente os links da página."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = html_mock

    url_base = "https://example.com"
    csv_links, page_links = scraper_links(url_base)

    assert len(csv_links) == 1
    assert "https://example.com/data.csv" in csv_links

    assert len(page_links) == 2  # O diretório de 2013 deve ser ignorado
    assert "https://example.com/page1/" in page_links
    assert "https://example.com/page2/" in page_links  # Link relativo convertido


@patch("requests.get")
def test_scraper_links_no_links(mock_get):
    """Testa uma página sem links."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><body><p>Sem links aqui</p></body></html>"

    csv_links, page_links = scraper_links("https://example.com")

    assert csv_links == []  # Lista vazia de CSVs
    assert page_links == []  # Lista vazia de diretórios

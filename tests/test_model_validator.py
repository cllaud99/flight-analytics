import os
import sys

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from src.models import validate

CSV_VALIDO = "tests/models_tests/voos_validos.csv"
CSV_INVALIDO = "tests/models_tests/voos_invalidos.csv"


def test_csv_valid():
    """
    Testa a validação de um CSV com dados válidos.

    Verifica se o DataFrame resultante não está vazio, contém 13 registros
    e o primeiro registro possui 'AAL' como 'sigla_icao_empresa'.
    """

    df = validate(CSV_VALIDO)
    assert not df.empty  # Deve conter dados válidos
    assert df.shape[0] == 13
    assert df.iloc[0]["sigla_icao_empresa"] == "AAL"


def test_csv_invalid():
    """
    Testa a validação de um CSV com dados inválidos.

    Verifica se o DataFrame resultante está vazio, pois todos os registros
    contém erros de validação.
    """
    df = validate(CSV_INVALIDO)
    assert df.empty  # Deve ser vazio, pois todos os registros são inválidos


if __name__ == "__main__":
    pytest.main()

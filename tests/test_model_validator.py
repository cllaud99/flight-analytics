import os
import sys
import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src"))
)

from src.models import validate

CSV_VALIDO = "tests/models_tests/voos_validos.csv"
CSV_INVALIDO = "tests/models_tests/voos_invalidos.csv"


def test_csv_valido():
    df = validate(CSV_VALIDO)
    assert not df.empty  # Deve conter dados válidos
    assert df.shape[0] == 13
    assert df.iloc[0]["sigla_icao_empresa"] == "AAL"


def test_csv_invalido():
    df = validate(CSV_INVALIDO)
    assert df.empty  # Deve ser vazio, pois todos os registros são inválidos


if __name__ == "__main__":
    pytest.main()

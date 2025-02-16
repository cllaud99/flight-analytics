from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from typing import Optional
import pandas as pd
import math

class VooModel(BaseModel):
    sigla_icao_empresa: str = Field(..., title="Sigla ICAO da Empresa Aérea")
    empresa_aerea: str = Field(..., title="Nome da Empresa Aérea")
    numero_voo: int = Field(..., title="Número do Voo")
    codigo_di: str = Field(..., title="Código DI")
    codigo_tipo_linha: str = Field(..., title="Código do Tipo de Linha")
    modelo_equipamento: str = Field(..., title="Modelo do Equipamento")
    numero_assentos: int = Field(..., title="Número de Assentos")
    sigla_icao_origem: str = Field(..., title="Sigla ICAO do Aeroporto de Origem")
    descricao_origem: str = Field(..., title="Descrição do Aeroporto de Origem")
    partida_prevista: datetime = Field(..., title="Data e Hora da Partida Prevista")
    partida_real: datetime = Field(..., title="Data e Hora da Partida Real")
    sigla_icao_destino: str = Field(..., title="Sigla ICAO do Aeroporto de Destino")
    descricao_destino: str = Field(..., title="Descrição do Aeroporto de Destino")
    chegada_prevista: datetime = Field(..., title="Data e Hora da Chegada Prevista")
    chegada_real: datetime = Field(..., title="Data e Hora da Chegada Real")
    situacao_voo: str = Field(..., title="Situação do Voo")
    justificativa: Optional[str] = Field(None, title="Justificativa para Alteração")
    referencia: datetime = Field(..., title="Data de Referência")
    situacao_partida: str = Field(..., title="Situação da Partida")
    situacao_chegada: str = Field(..., title="Situação da Chegada")


    @field_validator('partida_prevista', 'partida_real', 'chegada_prevista', 'chegada_real', mode="before")
    def parse_datetime(cls, value):
        """
        Converte strings de data no formato 'DD/MM/YYYY HH:MM' para datetime.
        Se o valor já for datetime, retorna-o sem alteração.
        """
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, "%d/%m/%Y %H:%M")

    @field_validator('justificativa', mode="before")
    def validar_justificativa(cls, value):
        """
        Se o valor for NaN (não um número), converte para None.
        Caso contrário, retorna o valor inalterado.
        """
        if isinstance(value, float) and math.isnan(value):
            return None
        return value
    

def validar_voos(file_path: str) -> pd.DataFrame:
    """Lê um CSV, valida os dados e retorna um DataFrame apenas com os registros válidos."""
    df = pd.read_csv(file_path, dtype=str, sep=";")
    df.columns = [
    "sigla_icao_empresa", "empresa_aerea", "numero_voo", "codigo_di", 
    "codigo_tipo_linha", "modelo_equipamento", "numero_assentos",
    "sigla_icao_origem", "descricao_origem", "partida_prevista", "partida_real",
    "sigla_icao_destino", "descricao_destino", "chegada_prevista", "chegada_real",
    "situacao_voo", "justificativa", "referencia", "situacao_partida", "situacao_chegada"
    ]
    print(df.columns)
    voos_validos = []
    for _, row in df.iterrows():
        try:
            voo = VooModel(**row.to_dict())
            voos_validos.append(voo.model_dump())
        except ValidationError as e:
            print(e)
            pass  # Ignora os inválidos

    return pd.DataFrame(voos_validos)

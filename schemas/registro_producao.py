from pydantic import BaseModel, field_validator
from typing import List
from datetime import date
from model.registro_producao import RegistroProducao


class RegistroProducaoSchema(BaseModel):
    nome_vaca: str = "Mimosa"
    data_registro: date = date.today()
    litros: float = 18.5

    @field_validator("litros")
    @classmethod
    def validar_litros(cls, value: float):
        if value <= 0:
            raise ValueError("A quantidade de litros deve ser maior que zero.")
        return value


class RegistroBuscaSchema(BaseModel):
    nome_vaca: str = "Mimosa"


class RegistroViewSchema(BaseModel):
    id: int = 1
    nome_vaca: str = "Mimosa"
    data_registro: date = date.today()
    litros: float = 18.5


class ListagemRegistrosSchema(BaseModel):
    registros: List[RegistroViewSchema]


def apresenta_registro(registro: RegistroProducao, nome_vaca: str):
    return {
        "id": registro.id,
        "nome_vaca": nome_vaca,
        "data_registro": registro.data_registro,
        "litros": registro.litros
    }


def apresenta_registros(registros, nome_vaca: str):
    result = []
    for registro in registros:
        result.append({
            "id": registro.id,
            "nome_vaca": nome_vaca,
            "data_registro": registro.data_registro,
            "litros": registro.litros
        })
    return {"registros": result}
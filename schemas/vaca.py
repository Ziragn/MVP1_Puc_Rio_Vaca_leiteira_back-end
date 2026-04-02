from pydantic import BaseModel
from typing import Optional, List
from model.vaca import Vaca



class VacaSchema(BaseModel):
    """ Define como uma nova vaca, deve ser inserida e ser representada.
    """
    nome: str = "Mimosa"
    raca: str = "Nelore"
    


class VacaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da vaca.
    """
    nome: str = "Teste"


class ListagemVacasSchema(BaseModel):
    """ Define como uma listagem de vacas será retornada.
    """
    Vacas:List[VacaSchema]


def apresenta_vacas(vacas: List[Vaca]):
    """ Retorna uma representação da vaca, seguindo o schema definido em
        VacaViewSchema.
    """
    result = []
    for vaca in vacas:
        result.append({
            "nome": vaca.nome,
            "raca": vaca.raca,
        })

    return {"vacas": result}


class VacaViewSchema(BaseModel):
    """ Define como uma vaca será retornada: vaca
    """
    id: int = 1
    nome: str = "Mimosa"
    raca: str = "Nelore"
    
   


class VacaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_vaca(vaca: Vaca):
    """ Retorna uma representação da vaca seguindo o schema definido em
        VacaViewSchema.
    """
    return {
        "id": vaca.id,
        "nome": vaca.nome,
        "raca": vaca.raca,
    }

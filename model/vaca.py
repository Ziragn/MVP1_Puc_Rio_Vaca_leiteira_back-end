from sqlalchemy import Column, String, Integer, Float
from typing import Union

from  model import Base


class Vaca(Base):
    __tablename__ = 'Vaca'

    id = Column("pk_vaca", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    raca = Column(String(140))
    


    def __init__(self, nome:str, raca:str):
        """
        Cria o registro de uma vaca

        Arguments:
            nome: Nome da vaca, deve ser único
            raça: Qual a raça da vaca.
        """
        self.nome = nome
        self.raca = raca
        

      



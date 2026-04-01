from sqlalchemy import Column, String, Integer, Float
from typing import Union

from  model import Base


class Vaca(Base):
    __tablename__ = 'Vaca'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    raca = Column(String(140))
    producao_leiteira = Column(Float)


    def __init__(self, nome:str, raca:str, producao_leiteira:float):
        """
        Cria o registro de uma vaca

        Arguments:
            nome: Nome da vaca.
            raça: Qual a raça da vaca.
            producao_leiteira: Quanto a vaca produz de leite/dia em litros
        """
        self.nome = nome
        self.raca = raca
        self.producao_leiteira = producao_leiteira

      



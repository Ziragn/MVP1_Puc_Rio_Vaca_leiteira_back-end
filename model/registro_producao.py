from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from datetime import date
from model import Base


class RegistroProducao(Base):
    __tablename__ = 'registro_producao'

    id = Column(Integer, primary_key=True)
    data_registro = Column(Date, nullable=False, default=date.today)
    litros = Column(Float, nullable=False)
    vaca_id = Column(Integer, ForeignKey('Vaca.pk_vaca'), nullable=False)

    def __init__(self, data_registro: date, litros: float, vaca_id: int):
        self.data_registro = data_registro
        self.litros = litros
        self.vaca_id = vaca_id
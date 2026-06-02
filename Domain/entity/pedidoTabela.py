from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from enum import Enum

Base = declarative_base

class CanalPedido(Enum):
    APP = 1,
    TOTEM = 2,
    BALCAO = 3,
    PICKUP = 4,
    WEB = 5

class Pedido(Base):
    __tablename__ = "pedidos" 
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True)
    data_hora = Column("data_hora", DateTime(timezone=True), server_default=func.now())
    status = Column("status", Boolean)
    valor_total = Column("valor_total", Float)
    canalPedido = Column("canalPedido", Enum(CanalPedido))

    def __init__(self):
        self.data_hora = data_hora
        self.status = status
        self.valor_total = valor_total
        


from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Float, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from enum import Enum
from Domain.entities import CanalPedido

Base = declarative_base()
class PedidoModel(Base):
    __tablename__ = "pedidos" 
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True)
    status = Column("status", Boolean)
    valor_total = Column("valor_total", Float)
    canal_pedido = Column("canalPedido", SQLEnum(CanalPedido))
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Enum as SQLEnum
from src.Domain.entities.CanalPedido import CanalPedido
from src.Infrastructure.database.config import Base

class PedidoModel(Base):
    __tablename__ = "pedidos" 
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True)
    status = Column("status", Boolean)
    valor_total = Column("valor_total", Float)
    canal_pedido = Column("canalPedido", SQLEnum(CanalPedido))
    
class ClienteModel(Base):
    __tablename__ = "clientes" 
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", nullable=False)
    telefone = Column("telefone", Integer)
    endereco = Column("endereco", String)
    cpf = Column("cpf", String)

class FuncionarioModel(Base):
    __tablename__ = "funcionarios"
    id = Column("id",Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column("email", String)
    telefone = Column("telefone", Integer)
    endereco = Column("endereco", String)
    cpf = Column("cpf", String)
    setor = Column("setor", String)


class EstoqueModel(Base):
    __tablename__ = "estoques"
    id_estoque = Column("id", Integer, primary_key=True, unique=True)
    unidade_restaurante = Column("unidade", String)
    
class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id_ingrediente = Column("id", primary_key=True, unique=True)
    nome = Column("nome", String)

class Prato(Base):
    __tablename__ = "pratos"
    id_prato = Column("id", primary_key=True, unique=True)
    nome = Column("nome", String)
    valor = Column("valor", Float)
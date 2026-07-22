from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Float, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from src.Domain.entities.CanalPedido import CanalPedido
from src.Infrastructure.database.config import Base
import datetime

class PratoPedidoModel(Base):
    __tablename__ = "prato_pedido"
    id_prato_pedido = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)

    #Chaves estrangeiras
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"))
    id_prato = Column(Integer, ForeignKey("pratos.id_prato"))

    #Relacionamentos
    pedido = relationship("PedidoModel", back_populates="itens")
    prato = relationship("PratoModel")


class UnidadeModel(Base):
    __tablename__ = "unidades"
    id_unidade = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    endereco = Column(String)
    telefone = Column(String)

    #Relacionamentos
    pedidos = relationship("PedidoModel", back_populates="unidade")
    estoque = relationship("EstoqueModel", back_populates="unidade", uselist=False)


class ClienteModel(Base):
    __tablename__ = "clientes"
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    telefone = Column(String)
    endereco = Column(String)
    cpf = Column(String, unique=True)

    #Relacionamentos
    pedidos = relationship("PedidoModel", back_populates="cliente")


class PedidoModel(Base):
    __tablename__ = "pedidos"
    id_pedido = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="AGUARDANDO_PAGAMENTO")
    valor_total = Column(Float, default=0.0)
    canal_pedido = Column("canalPedido", SQLEnum(CanalPedido), nullable=False)

    #Chaves estrangeiras
    id_unidade = Column(Integer, ForeignKey("unidades.id_unidade"))
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))

    #Relacionamentos
    unidade = relationship("UnidadeModel", back_populates="pedidos")
    cliente = relationship("ClienteModel", back_populates="pedidos")
    itens = relationship("PratoPedidoModel", back_populates="pedido")
    pagamento = relationship("GatewayModel", back_populates="pedido", uselist=False)


class PratoModel(Base):
    __tablename__ = "pratos"
    id_prato = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String)
    saldo_estoque = Column(Integer, default=0)


class GatewayModel(Base):
    __tablename__ = "gateway_pagamento"
    id_pagamento = Column(Integer, primary_key=True, autoincrement=True)
    valor_pagamento = Column(Float, nullable=False)
    data_pagamento = Column(DateTime, default=datetime.datetime.utcnow)
    forma_pagamento = Column(String, nullable=False)
    status_pagamento = Column(String, nullable=False)

    #Chave estrangeira
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"))
    pedido = relationship("PedidoModel", back_populates="pagamento")


class EstoqueModel(Base):
    __tablename__ = "estoques"
    id_estoque = Column(Integer, primary_key=True, autoincrement=True)
    unidade_restaurante = Column(String)

    #Chave estrangeira
    id_unidade = Column(Integer, ForeignKey("unidades.id_unidade"))
    unidade = relationship("UnidadeModel", back_populates="estoque")


class LogAuditoriaModel(Base):
    __tablename__ = "logs_auditoria"
    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    acao = Column(String, nullable=False)
    detalhes = Column(String)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
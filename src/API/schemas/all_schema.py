from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from src.Domain.entities.CanalPedido import CanalPedido

class ItemPedidoSchema(BaseModel):
    produtoId: int = Field(gt=0, description="ID do produto")
    quantidade: int = Field(gt=0, description="Quantidade do item")


class PedidoCreate(BaseModel):
    canalPedido: CanalPedido = Field(description="Canal de origem do pedido")

    clienteId: int = Field(gt=0)
    unidadeId: int = Field(gt=0)

    #Uma lista de itens que obriga o envio de pelo menos 1 item no array
    itens: List[ItemPedidoSchema] = Field(min_length=1, description="Itens do pedido")

    #Campo para receber o indicativo do serviço externo de pagamento
    formaPagamento: str = Field(min_length=1, description="Forma de pagamento")

class ClienteSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=10, max_length=200)
    telefone: int = Field(max_length=13)
    endereco: str = Field(min_length=10, max_length=150)
    cpf: str = Field(min_length=11, max_length=11)

class LoginSchema(BaseModel):
    email: str = Field(min_length=10, max_length=200)
    senha: str = Field(min_length=4, max_length=12)

class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=10, max_length=200)
    email: str = Field(min_length=10, max_length=200)
    senha: str = Field(min_length=4, max_length=12)

class ColaboradorSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=10, max_length=200)
    telefone: int = Field(max_length=13)
    cpf: str = Field(min_length=11, max_length=11)

class UnidadeSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    cnpj: str = Field(min_length=1, max_length=200, description="CNPJ da unidade")
    endereco: str = Field(min_length=1, max_length=200, description="Endereco da unidade")
    telefone: str = Field(min_length=1, max_length=200, description="Telefone da unidade")

class EstoqueSchema(BaseModel):
    unidade_restaurante: str = Field(min_length=1, max_length=200)
    id_unidade: int = Field(gt=0, description="Unidade de origem")
    id_gestor: int = Field(gt=0, description="Gestor da unidade")
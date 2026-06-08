from pydantic import BaseModel, Field, ConfigDict
from src.Domain.entities import cliente, pedido, prato, ingrediente
'''
class ClienteBase(BaseModel):
    
    nome: str = Field(min_length=3, max_length=150)
    email: str = Field(min_length=10, max_length=200)
    telefone: int = Field(min_length=8, max_length=13)
    endereco: str = Field(min_length=10, max_length=150)
    cpf: str = Field(min_length=11, max_length=11)
'''
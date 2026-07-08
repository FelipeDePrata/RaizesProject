from pydantic import BaseModel, Field

class ClienteSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=10, max_length=200)
    telefone: int = Field(min_length=8, max_length=13)
    endereco: str = Field(min_length=10, max_length=150)
    cpf: str = Field(min_length=11, max_length=11)

class LoginSchema(BaseModel):
    email: str = Field(min_length=10, max_length=200)
    senha: str = Field(min_length=4, max_length=12)

class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=10, max_length=200)
    email: str = Field(min_length=10, max_length=200)
    senha: str = Field(min_length=4, max_length=12)

class PedidoCreate(BaseModel):
    pass

class ColaboradorSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    email: str = Field(min_length=10, max_length=200)
    telefone: int = Field(min_length=1, max_length=13)
    cpf: str = Field(min_length=11, max_length=11)

class UnidadeSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    cnpj: str = Field(min_length=1, max_length=200)
    endereco: str = Field(min_length=1, max_length=200)
    telefone: str = Field(min_length=1, max_length=200)

class EstoqueSchema(BaseModel):
    unidade_restaurante: str = Field(min_length=1, max_length=200)
    id_unidade: int
    id_gestor: int
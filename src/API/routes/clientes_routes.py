from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from pydantic import BaseModel
from src.API.main import app
from src.API.schemas.all_schema import ( LoginSchema, ClienteSchema, UsuarioCreate, UnidadeSchema,
                                         PedidoCreate)
from src.Infrastructure.database.config import SessionLocal

# Endpoints: /auth

@app.post("/auth/login")
def login(dados: LoginSchema):
    return{"mensagem": "123"}

@app.post("/auth/logout")
def logout():
    return {"mensagem": "Logout realizado com sucesso"}


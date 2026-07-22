from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.Infrastructure.database.config import get_db
from src.Infrastructure.database.models.models import ClienteModel
from src.API.schemas.all_schema import LoginSchema
from src.API.middlewares.auth import verificar_senha, criar_token_jwt
from src.API.utils.response import erro_padrao

router = APIRouter(tags=["Autenticação"])

@router.post("/auth/login")
def login(dados: LoginSchema, request: Request, db: Session = Depends(get_db)):
    usuario = db.query(ClienteModel).filter(ClienteModel.email == dados.email).first()

    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        return erro_padrao(
            status_code=401,
            error="CREDENCIAIS_INVALIDAS",
            message="E-mail ou senha inválidos.",
            path=request.url.path
        )

    token = criar_token_jwt(usuario.id_cliente, usuario.nome, "CLIENTE")

    return {
        "accessToken": token,
        "tokenType": "Bearer",
        "expiresIn": 7200,
        "user": {
            "id": usuario.id_cliente,
            "nome": usuario.nome,
            "perfil": "CLIENTE"
        }
    }
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

#Configuração do JWT.
SECRET_KEY = "chave_raizes_do_sertao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 2

#Configuração do Passlib para senhas.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Segurança para o Swagger
security = HTTPBearer()

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    #Verifica se a senha digitada bate com o hash do banco.
    return pwd_context.verify(senha_plana, senha_hash)

def criar_token_jwt(usuario_id: int, nome: str, perfil: str) -> str:
    #Gera um novo token JWT.
    expiracao = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": str(usuario_id),
        "nome": nome,
        "perfil": perfil,
        "exp": expiracao
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    #Decodifica o token e valida se ele é válido e não expirou.
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload #Retorna os dados do usuário.
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Faça login novamente."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )
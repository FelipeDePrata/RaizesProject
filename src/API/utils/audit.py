from src.Infrastructure.database.models.models import LogAuditoriaModel
from sqlalchemy.orm import Session

def registrar_log_auditoria(db: Session, id_usuario: int, acao: str, detalhes: str):
    #Registra ações sensíveis no banco de dados para fins de auditoria e LGPD.

    novo_log = LogAuditoriaModel(
        id_usuario=id_usuario,
        acao=acao,
        detalhes=detalhes
    )
    db.add(novo_log)
    db.commit()
from sqlalchemy.orm import Session
from src.Infrastructure.database.models.models import PedidoModel, ClienteModel, FuncionarioModel
from src.API.schemas.all_schema import UsuarioCreate,PedidoCreate, ClienteSchema

def criar_usuario(db: Session, usuario: UsuarioCreate): #Cria um usuario
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def atualizar_usuario(db: Session, usuario: ClienteModel, payload: ClienteSchema): # Atualiza informações de usuário
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(usuario, field, value)
    db.commit()
    db.refresh(usuario)
    return usuario

def delete_usuario(db: Session, usuario: ClienteModel): # Deleta um usuario
    db.delete(usuario)
    db.commit()

def get_pedido(db: Session, pedido_id: int): #Busca pedido por ID
    return db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first

def create_pedido(db: Session, payload: PedidoCreate): # Cria pedido
    pedido = PedidoCreate(**payload.dict())
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido

def delete_pedido(db: Session, pedido:PedidoModel): # Deleta pedido
    db.delete(pedido)
    db.commit()
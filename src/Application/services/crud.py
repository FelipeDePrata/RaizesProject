from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.Infrastructure.database.models.models import PedidoModel, ClienteModel, PratoPedidoModel
from src.API.schemas.all_schema import UsuarioCreate, PedidoCreate, ClienteSchema

#Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str):
    return pwd_context.hash(password)


def criar_usuario(db: Session, usuario: UsuarioCreate):
    #Cria o usuario, transformando o Schema no Model do banco de dados e criptografando a senha
    db_usuario = ClienteModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=get_password_hash(usuario.senha)  # LGPD e Segurança aplicadas
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def atualizar_usuario(db: Session, usuario: ClienteModel, payload: ClienteSchema):
    #atualiza dados do usuario
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(usuario, field, value)
    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, usuario: ClienteModel):
    #Deleta usuario
    db.delete(usuario)
    db.commit()


def get_pedido(db: Session, pedido_id: int):
    #Lista pedidos
    return db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()


def create_pedido(db: Session, payload: PedidoCreate):
    #Cria o Pedido principal mapeando corretamente os dados de entrada para o SQLAlchemy
    novo_pedido = PedidoModel(
        canal_pedido=payload.canalPedido,
        id_cliente=payload.clienteId,
        id_unidade=payload.unidadeId,
        status="AGUARDANDO_PAGAMENTO"
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)  # Precisamos do ID do pedido gerado pelo banco

    #Salva os itens do pedido na tabela associativa
    for item in payload.itens:
        db_item = PratoPedidoModel(
            id_pedido=novo_pedido.id_pedido,
            id_prato=item.produtoId,
            quantidade=item.quantidade
        )
        db.add(db_item)

    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


def delete_pedido(db: Session, pedido: PedidoModel):
    #Deleta pedido
    db.delete(pedido)
    db.commit()
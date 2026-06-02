from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from database.models import pedidoTabela

db = create_engine("sqlite:///raizesdosertao.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

pedido = pedidoTabela.Pedido(status=True ,valor_total=10.87, canal_pedido="APP")
session.add(pedido)
session.commit()
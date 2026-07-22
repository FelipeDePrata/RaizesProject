from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from src.Infrastructure.database.config import get_db
from src.Infrastructure.database.models.models import PedidoModel, GatewayModel, UnidadeModel, PratoModel
from src.Infrastructure.integrations.pagamento_mock import simular_gateway_pagamento
from pydantic import BaseModel
from src.API.schemas.all_schema import PedidoCreate
from src.Application.services.crud import create_pedido
from src.API.middlewares.auth import validar_token
from src.API.utils.response import erro_padrao

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

#Schema temporário apenas para receber a forma de pagamento na rota.
class PagamentoRequest(BaseModel):
    forma_pagamento: str

#Abaixo, está o fluxo e endpoint de pagamento e atualização de status do pedido.

@router.post("/{id_pedido}/pagar")
def processar_pagamento(id_pedido: int, payload: PagamentoRequest, request: Request, db: Session = Depends(get_db)):

    #Busca o pedido no banco de dados.
    pedido = db.query(PedidoModel).filter(PedidoModel.id_pedido == id_pedido).first()

    #Caso o pedido não for encontrado (Status 404 exigido).
    if not pedido:
        return erro_padrao(
            status_code=404,
            error="PEDIDO_NAO_ENCONTRADO",
            message=f"Não foi possível localizar o pedido com ID {id_pedido}.",
            path=request.url.path
        )

    #Para evitar o pagamento duplo (Status 409 exigido).
    if pedido.status != "AGUARDANDO_PAGAMENTO":
        return erro_padrao(
            status_code=409,
            error="CONFLITO_STATUS_PEDIDO",
            message=f"O pedido não pode ser pago pois seu status atual é '{pedido.status}'.",
            path=request.url.path
        )

    #Chama o mock do pagamento.
    valor_a_cobrar = pedido.valor_total if pedido.valor_total > 0 else 50.0
    resposta_gateway = simular_gateway_pagamento(
        id_pedido=pedido.id_pedido,
        valor_total=valor_a_cobrar,
        forma_pagamento=payload.forma_pagamento
    )

    #Registra o retorno do Gateway no banco de dados.
    registro_pagamento = GatewayModel(
        valor_pagamento=resposta_gateway["valor_processado"],
        forma_pagamento=resposta_gateway["forma_pagamento"],
        status_pagamento=resposta_gateway["status_pagamento"],
        id_pedido=pedido.id_pedido
    )
    db.add(registro_pagamento)

    #Atualiza o status do pedido baseado no retorno do mock.
    if resposta_gateway["status_pagamento"] == "APROVADO":
        pedido.status = "PREPARANDO"  #Status atualizado para a cozinha.
        db.commit()
        db.refresh(pedido)

        return {
            "message": "Pagamento aprovado com sucesso!",
            "pedido_id": pedido.id_pedido,
            "novo_status": pedido.status,
            "comprovante_gateway": resposta_gateway
        }
    else:
        pedido.status = "FALHA_PAGAMENTO"  # Atualiza status para falha.
        db.commit()

        #Retorna o erro 422
        return erro_padrao(
            status_code=422,
            error="PAGAMENTO_RECUSADO",
            message=resposta_gateway["mensagem_gateway"],
            path=request.url.path
        )


#Abaixo, está o fluxo e endpoint para criar um novo pedido, validar multicanalidade e calcular total de pedido.

@router.post("", status_code=201)
def criar_pedido(
    #A rota exige o token. Caso contrário, retorna 401.
    payload: PedidoCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(validar_token)
):
    pass

    #Validação e cálculo total de produtos.
    valor_total_calculado = 0.0
    itens_resposta = []

    for item in payload.itens:
        prato = db.query(PratoModel).filter(PratoModel.id_prato == item.produtoId).first()
        if not prato:
            return erro_padrao(
                status_code=404,
                error="PRODUTO_NAO_ENCONTRADO",
                message=f"O produto com ID {item.produtoId} não foi encontrado no cardápio.",
                path=request.url.path
            )

        #Calculo do subtotal do item.
        valor_total_calculado += prato.preco * item.quantidade

        #Montagem da estrutura do item para a resposta JSON.
        itens_resposta.append({
            "produtoId": prato.id_prato,
            "quantidade": item.quantidade,
            "precoUnitario": prato.preco
        })

    novo_pedido = create_pedido(db=db, payload=payload)

    #Atualiza o valor total que foi calculado e salva no banco de dados.
    novo_pedido.valor_total = valor_total_calculado
    db.commit()

    return {
        "pedidoId": novo_pedido.id_pedido,
        "status": novo_pedido.status,
        "total": round(novo_pedido.valor_total, 2),
        "itens": itens_resposta,
        "createdAt": novo_pedido.data_hora.isoformat() + "Z"
    }
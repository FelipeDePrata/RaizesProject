import uuid
import random
from datetime import datetime


def simular_gateway_pagamento(id_pedido: int, valor_total: float, forma_pagamento: str) -> dict:

    #Simulação do tempo de resposta e o retorno de uma API de pagamento externa.


    #REGRA PARA TESTES:
    #Se a forma de pagamento vier como "ERRO_MOCK", nós forçamos a falha.
    #Caso contrário, temos 80% de chance de aprovação.
    if forma_pagamento.upper() == "ERRO_MOCK":
        aprovado = False
    else:
        aprovado = random.random() < 0.8

    payload_retorno = {
        "id_transacao_externa": str(uuid.uuid4()),  #Gera um ID simulando o Gateway
        "id_pedido_interno": id_pedido,
        "valor_processado": valor_total,
        "forma_pagamento": forma_pagamento,
        "data_transacao": datetime.utcnow().isoformat(),
        "status_pagamento": "APROVADO" if aprovado else "RECUSADO",
        "mensagem_gateway": "Transação autorizada com sucesso." if aprovado else "Transação recusada pela operadora."
    }

    return payload_retorno
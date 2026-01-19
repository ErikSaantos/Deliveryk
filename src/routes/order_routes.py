from fastapi import APIRouter, Depends, HTTPException
from schemas import PedidoSchema
from dependencies import pegar_sessao
from sqlalchemy.orm import Session
from models import Pedido

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Explicando a função aqui:
    ...
    """
    return {"msg": "Acessou a rota de pedidos!"}


@order_router.post("/criar_pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario= pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return { "msg": f"Pedido criado com sucesso! ID: {novo_pedido.id}" }
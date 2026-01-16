from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Explicando a função aqui:
    ...
    """
    return {"msg": "Acessou a rota de pedidos!"}
#pip install fastapi uvicorn sqlalchemy passlib\[bcrypt\] python-jose\[cryptography\] python-dotenv python-multipart
#uvicorn main:app --reload
# Ter cuidado nas importações para não cair em Referência Circular:
# main precisa dos arquivos de rotas e arquivos de rotas precisam do main

from fastapi import FastAPI

app = FastAPI()

from routes.auth_routes import auth_router #router -> Roteador
from routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
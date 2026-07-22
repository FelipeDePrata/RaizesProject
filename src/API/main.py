from fastapi import FastAPI
from src.API.routes import clientes_routes
from src.API.routes import pedidos_routes

app = FastAPI(title="Raízes do Sertão", version="1.0.0")

#Registra os controllers no FastAPI
app.include_router(clientes_routes.router)
app.include_router(pedidos_routes.router)
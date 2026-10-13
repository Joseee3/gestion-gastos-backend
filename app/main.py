from fastapi import FastAPI
from app.routers import gastos, ingresos, resumen

app = FastAPI(
    title="Gestión de Gastos API",
    description="API para administrar ingresos y gastos personales",
    version="1.0.0",
)

app.include_router(gastos.router)
app.include_router(ingresos.router)
app.include_router(resumen.router)

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido a Gestión de Gastos"}


@app.get("/health")
def verificar_estado():
    return {"estado": "ok"}
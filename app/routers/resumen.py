
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import obtener_usuario_actual
from app.database import obtener_db
from app.models import Gasto, Ingreso


router = APIRouter(prefix="/resumen", tags=["Resumen"])


@router.get("/")
def obtener_resumen(
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(obtener_usuario_actual),
):
    total_gastos = db.query(
        func.coalesce(func.sum(Gasto.monto), 0)
    ).filter(
        Gasto.usuario_id == usuario["id"]
    ).scalar()

    total_ingresos = db.query(
        func.coalesce(func.sum(Ingreso.monto), 0)
    ).filter(
        Ingreso.usuario_id == usuario["id"]
    ).scalar()

    saldo = total_ingresos - total_gastos

    return {
        "total_ingresos": float(total_ingresos),
        "total_gastos": float(total_gastos),
        "saldo": float(saldo),
    }


@router.get("/gastos-por-categoria")
def gastos_por_categoria(
    db: Session = Depends(obtener_db),
    usuario: dict = Depends(obtener_usuario_actual),
):
    resultados = (
        db.query(
            Gasto.categoria,
            func.sum(Gasto.monto).label("total"),
        )
        .filter(Gasto.usuario_id == usuario["id"])
        .group_by(Gasto.categoria)
        .order_by(func.sum(Gasto.monto).desc())
        .all()
    )

    return [
        {
            "categoria": categoria,
            "total": float(total),
        }
        for categoria, total in resultados
    ]

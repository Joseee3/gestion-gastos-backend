
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import func
from datetime import date

from app.database import obtener_db
from app.models import Gasto, Ingreso

router = APIRouter(prefix="/resumen", tags=["Resumen"])


@router.get("/")
def obtener_resumen(db: Session = Depends(obtener_db)):
    total_gastos = db.query(
        func.coalesce(func.sum(Gasto.monto), 0)
    ).scalar()

    total_ingresos = db.query(
        func.coalesce(func.sum(Ingreso.monto), 0)
    ).scalar()

    saldo = total_ingresos - total_gastos

    return {
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "saldo": saldo
    }


@router.get("/gastos-por-categoria")
def gastos_por_categoria(db: Session = Depends(obtener_db)):
    resultados = (
        db.query(
            Gasto.categoria,
            func.sum(Gasto.monto).label("total")
        )
        .group_by(Gasto.categoria)
        .order_by(func.sum(Gasto.monto).desc())
        .all()
    )

    return [
        {
            "categoria": categoria,
            "total": float(total)
        }
        for categoria, total in resultados
    ]


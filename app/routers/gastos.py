
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import obtener_db
from app.models import Gasto
from app.schemas import GastoCrear, GastoRespuesta

router = APIRouter(prefix="/gastos", tags=["Gastos"])


@router.post("/", response_model=GastoRespuesta, status_code=201)
def crear_gasto(datos: GastoCrear, db: Session = Depends(obtener_db)):
    nuevo_gasto = Gasto(**datos.model_dump())

    db.add(nuevo_gasto)
    db.commit()
    db.refresh(nuevo_gasto)

    return nuevo_gasto



@router.get("/", response_model=list[GastoRespuesta])
def listar_gastos(
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None,
    db: Session = Depends(obtener_db)
):
    consulta = db.query(Gasto)

    if fecha_inicio:
        consulta = consulta.filter(Gasto.fecha >= fecha_inicio)

    if fecha_fin:
        consulta = consulta.filter(Gasto.fecha <= fecha_fin)

    return consulta.order_by(Gasto.fecha.desc()).all()



@router.get("/{gasto_id}", response_model=GastoRespuesta)
def obtener_gasto(gasto_id: int, db: Session = Depends(obtener_db)):
    gasto = db.get(Gasto, gasto_id)

    if gasto is None:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return gasto


from fastapi import HTTPException


@router.put("/{gasto_id}", response_model=GastoRespuesta)
def actualizar_gasto(
    gasto_id: int,
    datos: GastoCrear,
    db: Session = Depends(obtener_db)
):
    gasto = db.get(Gasto, gasto_id)

    if gasto is None:
        raise HTTPException(
            status_code=404,
            detail="Gasto no encontrado"
        )

    cambios = datos.model_dump()

    for campo, valor in cambios.items():
        setattr(gasto, campo, valor)

    db.commit()
    db.refresh(gasto)

    return gasto


@router.delete("/{gasto_id}", status_code=204)
def eliminar_gasto(
    gasto_id: int,
    db: Session = Depends(obtener_db)
):
    gasto = db.get(Gasto, gasto_id)

    if gasto is None:
        raise HTTPException(
            status_code=404,
            detail="Gasto no encontrado"
        )

    db.delete(gasto)
    db.commit()


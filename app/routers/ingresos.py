
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import obtener_db
from app.models import Ingreso
from app.schemas import IngresoCrear, IngresoRespuesta

router = APIRouter(prefix="/ingresos", tags=["Ingresos"])


@router.post("/", response_model=IngresoRespuesta, status_code=201)
def crear_ingreso(
    datos: IngresoCrear,
    db: Session = Depends(obtener_db)
):
    nuevo_ingreso = Ingreso(**datos.model_dump())

    db.add(nuevo_ingreso)
    db.commit()
    db.refresh(nuevo_ingreso)

    return nuevo_ingreso



@router.get("/", response_model=list[IngresoRespuesta])
def listar_ingresos(
    fecha_inicio: date | None = None,
    fecha_fin: date | None = None,
    db: Session = Depends(obtener_db)
):
    consulta = db.query(Ingreso)

    if fecha_inicio:
        consulta = consulta.filter(Ingreso.fecha >= fecha_inicio)

    if fecha_fin:
        consulta = consulta.filter(Ingreso.fecha <= fecha_fin)

    return consulta.order_by(Ingreso.fecha.desc()).all()


@router.get("/{ingreso_id}", response_model=IngresoRespuesta)
def obtener_ingreso(
    ingreso_id: int,
    db: Session = Depends(obtener_db)
):
    ingreso = db.get(Ingreso, ingreso_id)

    if ingreso is None:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")

    return ingreso

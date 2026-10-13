

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class GastoCrear(BaseModel):
    descripcion: str = Field(min_length=1, max_length=200)
    monto: float = Field(gt=0)
    categoria: str = Field(min_length=1, max_length=100)
    fecha: date = Field(default_factory=date.today)
    medio_pago: Literal["Yape", "Tarjeta", "Efectivo"] = "Efectivo"


class GastoRespuesta(GastoCrear):
    id: int
    model_config = ConfigDict(from_attributes=True)



class IngresoCrear(BaseModel):
    descripcion: str = Field(min_length=1, max_length=200)
    monto: float = Field(gt=0)
    categoria: str = Field(min_length=1, max_length=100)
    fecha: date = Field(default_factory=date.today)


class IngresoRespuesta(IngresoCrear):
    id: int

    model_config = ConfigDict(from_attributes=True)



from sqlalchemy import Column, Integer, String, Numeric, Date, Uuid
from datetime import date

from app.database import Base


class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Uuid(as_uuid=False),
        nullable=True,
        index=True
    )

    descripcion = Column(String(200), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(100), nullable=False)
    fecha = Column(Date, default=date.today, nullable=False)


class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Uuid(as_uuid=False),
        nullable=True,
        index=True
    )

    descripcion = Column(String(200), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(100), nullable=False)
    fecha = Column(Date, default=date.today, nullable=False)
    medio_pago = Column(
        String(30),
        nullable=False,
        default="Efectivo"
    )

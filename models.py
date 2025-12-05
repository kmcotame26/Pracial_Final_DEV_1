from typing import Optional, List
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship

class JugadorDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    numero: int = Field(..., ge=1, le=99, description="Número de camiseta único 1-99")
    nacionalidad: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    posicion: Optional[str] = None
    pie_habil: Optional[str] = None
    estado: str = Field(default="ACTIVO")
    foto_url: Optional[str] = None

    estadisticas: List["EstadisticaDB"] = Relationship(back_populates="jugador")
pass




class Estadistica():

    pass


class Partido():
    pass



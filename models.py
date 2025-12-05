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

    def edad(self) -> Optional[int]:
        """Calculamos edad en años a desde de la fecha de nacimiento."""
        if not self.fecha_nacimiento:
            return None
        hoy = date.today()
        anios = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            anios -= 1
        return anios

    def total_goles(self) -> int:
        return sum(e.goles for e in (self.estadisticas or []))

    def total_minutos(self) -> int:
        return sum(e.minutos for e in (self.estadisticas or []))


pass




class EstadisticaDB(SQLModel, table=True):
    """Desempeño de un jugador en un partido."""
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugadordb.id")
    partido_id: int = Field(foreign_key="partidodb.id")
    minutos: int = 0
    goles: int = 0
    asistencias: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    faltas: int = 0
    comentario: Optional[str] = None

    jugador: JugadorDB = Relationship(back_populates="estadisticas")
    partido: PartidoDB = Relationship(back_populates="estadisticas")

    pass


class PartidoDB(SQLModel, table=True):
    """Tabla de partidos"""
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: date
    rival: str
    goles_local: int = 0
    goles_rival: int = 0
    condicion: str = Field(default="LOCAL")  # LOCAL / VISITANTE
    resultado: str = Field(default="PENDIENTE")  # VICTORIA / EMPATE / DERROTA / PENDIENTE
    created_at: datetime = Field(default_factory=datetime.utcnow)

    estadisticas: List["EstadisticaDB"] = Relationship(back_populates="partido")

    pass



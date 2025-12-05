from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# Enums
class Position(str, Enum):
    ARQUERO = "ARQUERO"
    DEFENSA_C = "DEFENSA CENTRAL"
    DEFENSA_L = "DEFENSA LATERAL"
    VOLANTE_D = "VOLANTE DEFENSIVO"
    VOLANTE_O = "VOLANTE OFENSIVO"
    VOLANTE_C = "VOLANTE CENTRAL"
    VOLANTE_E = "VOLANTE EXTREMO"
    DELANTERO_C = "DELANTERO CENTRAL"
    DELANTERO_P = "DELANTERO PUNTA"


class Estado(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    LESIONADO = "LESIONADO"
    SUSPENDIDO = "SUSPENDIDO"


class PieDominante(str, Enum):
    DERECHO = "DERECHO"
    IZQUIERDO = "IZQUIERDO"
    AMBIDIESTRO = "AMBIDIESTRO"


class ResultadoPartido(str, Enum):
    VICTORIA = "VICTORIA"
    EMPATE = "EMPATE"
    DERROTA = "DERROTA"


# Modelos de Base de Datos
class Jugador(SQLModel, table=True):
    __tablename__ = "jugadores"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Datos Personales
    nombre_completo: str = Field(index=True, min_length=3, max_length=100)
    numero_camiseta: int = Field(unique=True, ge=1, le=99, index=True)
    fecha_nacimiento: date
    nacionalidad: str = Field(min_length=2, max_length=50)
    fotografia_url: Optional[str] = Field(default=None, max_length=500)

    # Datos Deportivos
    altura_cm: int = Field(ge=150, le=220)
    peso_kg: float = Field(ge=50.0, le=120.0)
    pie_dominante: PieDominante
    posicion: Position
    valor_mercado: Optional[float] = Field(default=0.0, ge=0)
    anio_ingreso: int = Field(ge=1900, le=2100)
    estado: Estado = Field(default=Estado.ACTIVO)

    # Fechas de control
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = Field(default=None)

    # Relaciones
    estadisticas: List["Estadistica"] = Relationship(back_populates="jugador")


class Partido(SQLModel, table=True):
    __tablename__ = "partidos"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Datos del Partido
    rival: str = Field(min_length=3, max_length=100)
    fecha_partido: date = Field(index=True)
    goles_sigmotaa: int = Field(ge=0)
    goles_rival: int = Field(ge=0)
    es_local: bool = Field(default=True)
    resultado: ResultadoPartido

    # Datos opcionales
    estadio: Optional[str] = Field(default=None, max_length=200)
    observaciones: Optional[str] = Field(default=None, max_length=500)

    # Fechas de control
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    estadisticas: List["Estadistica"] = Relationship(back_populates="partido")

    def calcular_resultado(self) -> ResultadoPartido:
        """Calcula automáticamente el resultado del partido"""
        if self.goles_sigmotaa > self.goles_rival:
            return ResultadoPartido.VICTORIA
        elif self.goles_sigmotaa < self.goles_rival:
            return ResultadoPartido.DERROTA
        else:
            return ResultadoPartido.EMPATE


class Estadistica(SQLModel, table=True):
    __tablename__ = "estadisticas"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    jugador_id: int = Field(foreign_key="jugadores.id", index=True)
    partido_id: int = Field(foreign_key="partidos.id", index=True)

    # Estadísticas del Jugador en el Partido
    minutos_jugados: int = Field(ge=0, le=120)  # Tiempo en minutos
    goles_anotados: int = Field(default=0, ge=0)
    asistencias: int = Field(default=0, ge=0)

    # Estadísticas Defensivas
    intercepciones: int = Field(default=0, ge=0)
    balones_recuperados: int = Field(default=0, ge=0)

    # Disciplina
    tarjetas_amarillas: int = Field(default=0, ge=0, le=2)
    tarjetas_rojas: int = Field(default=0, ge=0, le=1)
    faltas_cometidas: int = Field(default=0, ge=0)

    # Fechas de control
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    jugador: Optional[Jugador] = Relationship(back_populates="estadisticas")
    partido: Optional[Partido] = Relationship(back_populates="estadisticas")


# Modelos Pydantic para API (Request/Response)
class JugadorCreate(SQLModel):
    nombre_completo: str
    numero_camiseta: int
    fecha_nacimiento: date
    nacionalidad: str
    fotografia_url: Optional[str] = None
    altura_cm: int
    peso_kg: float
    pie_dominante: PieDominante
    posicion: Position
    valor_mercado: Optional[float] = 0.0
    anio_ingreso: int
    estado: Estado = Estado.ACTIVO


class JugadorUpdate(SQLModel):
    nombre_completo: Optional[str] = None
    numero_camiseta: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    fotografia_url: Optional[str] = None
    altura_cm: Optional[int] = None
    peso_kg: Optional[float] = None
    pie_dominante: Optional[PieDominante] = None
    posicion: Optional[Position] = None
    valor_mercado: Optional[float] = None
    anio_ingreso: Optional[int] = None
    estado: Optional[Estado] = None


class PartidoCreate(SQLModel):
    rival: str
    fecha_partido: date
    goles_sigmotaa: int
    goles_rival: int
    es_local: bool = True
    estadio: Optional[str] = None
    observaciones: Optional[str] = None


class EstadisticaCreate(SQLModel):
    jugador_id: int
    partido_id: int
    minutos_jugados: int
    goles_anotados: int = 0
    asistencias: int = 0
    intercepciones: int = 0
    balones_recuperados: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    faltas_cometidas: int = 0
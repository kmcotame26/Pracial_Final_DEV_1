from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sigmotaa_fc.db")

# Ajuste para PostgreSQL en Railway/Render
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)

# Configuración del engine
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """Crea todas las tablas en la base de datos"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Generador de sesiones para dependency injection"""
    with Session(engine) as session:
        yield session
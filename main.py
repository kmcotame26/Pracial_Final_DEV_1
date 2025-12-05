from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from database import create_db_and_tables
from routers import jugadores, partidos, estadisticas


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializar base de datos al arrancar la aplicación"""
    create_db_and_tables()
    yield


app = FastAPI(
    title="sigmotaa FC - Sistema de Gestión",
    description="Sistema de registro y análisis de jugadores y partidos",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(jugadores.router)
app.include_router(partidos.router)
app.include_router(estadisticas.router)


# ====== RUTAS PRINCIPALES ======

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api", response_class=HTMLResponse)
async def api_info(request: Request):
    """Información de la API"""
    return {
        "message": "sigmotaa FC API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "jugadores": "/jugadores",
            "partidos": "/partidos",
            "estadisticas": "/estadisticas"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
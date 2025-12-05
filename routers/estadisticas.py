from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional

from database import get_session
from models import Estadistica, EstadisticaCreate, Jugador, Partido, Estado

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])
templates = Jinja2Templates(directory="templates")


# ====== API ENDPOINTS ======

@router.post("/", response_model=Estadistica)
def create_estadistica(
        estadistica: EstadisticaCreate,
        session: Session = Depends(get_session)
):
    """Crear una nueva estadística"""
    try:
        # Validar que existan jugador y partido
        jugador = session.get(Jugador, estadistica.jugador_id)
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        partido = session.get(Partido, estadistica.partido_id)
        if not partido:
            raise HTTPException(status_code=404, detail="Partido no encontrado")

        # Verificar que no exista ya una estadística para este jugador en este partido
        existing = session.exec(
            select(Estadistica).where(
                Estadistica.jugador_id == estadistica.jugador_id,
                Estadistica.partido_id == estadistica.partido_id
            )
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una estadística para este jugador en este partido"
            )

        # Actualizar estado del jugador si recibe tarjetas
        if estadistica.tarjetas_rojas > 0 or estadistica.tarjetas_amarillas >= 2:
            jugador.estado = Estado.SUSPENDIDO
            session.add(jugador)

        db_estadistica = Estadistica.model_validate(estadistica)
        session.add(db_estadistica)
        session.commit()
        session.refresh(db_estadistica)
        return db_estadistica

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear estadística: {str(e)}")


@router.get("/", response_model=list[Estadistica])
def read_estadisticas(
        jugador_id: Optional[int] = None,
        partido_id: Optional[int] = None,
        session: Session = Depends(get_session)
):
    """Obtener lista de estadísticas con filtros opcionales"""
    try:
        statement = select(Estadistica)

        if jugador_id:
            statement = statement.where(Estadistica.jugador_id == jugador_id)
        if partido_id:
            statement = statement.where(Estadistica.partido_id == partido_id)

        estadisticas = session.exec(statement).all()
        return estadisticas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")


@router.get("/{estadistica_id}", response_model=Estadistica)
def read_estadistica(estadistica_id: int, session: Session = Depends(get_session)):
    """Obtener una estadística por ID"""
    estadistica = session.get(Estadistica, estadistica_id)
    if not estadistica:
        raise HTTPException(status_code=404, detail="Estadística no encontrada")
    return estadistica


@router.delete("/{estadistica_id}")
def delete_estadistica(estadistica_id: int, session: Session = Depends(get_session)):
    """Eliminar una estadística"""
    try:
        estadistica = session.get(Estadistica, estadistica_id)
        if not estadistica:
            raise HTTPException(status_code=404, detail="Estadística no encontrada")

        session.delete(estadistica)
        session.commit()
        return {"message": "Estadística eliminada correctamente"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar estadística: {str(e)}")


# ====== HTML VIEWS ======

@router.get("/html/crear", response_class=HTMLResponse)
def crear_estadistica_form(
        request: Request,
        partido_id: Optional[int] = None,
        session: Session = Depends(get_session)
):
    """Vista HTML: Formulario de creación"""
    jugadores = session.exec(select(Jugador).where(Jugador.estado == Estado.ACTIVO)).all()
    partidos = session.exec(select(Partido)).all()

    partido_seleccionado = None
    if partido_id:
        partido_seleccionado = session.get(Partido, partido_id)

    return templates.TemplateResponse(
        "estadisticas/crear.html",
        {
            "request": request,
            "jugadores": jugadores,
            "partidos": partidos,
            "partido_seleccionado": partido_seleccionado
        }
    )


@router.post("/html/crear", response_class=HTMLResponse)
async def crear_estadistica_submit(
        request: Request,
        jugador_id: int = Form(...),
        partido_id: int = Form(...),
        minutos_jugados: int = Form(...),
        goles_anotados: int = Form(0),
        asistencias: int = Form(0),
        intercepciones: int = Form(0),
        balones_recuperados: int = Form(0),
        tarjetas_amarillas: int = Form(0),
        tarjetas_rojas: int = Form(0),
        faltas_cometidas: int = Form(0),
        session: Session = Depends(get_session)
):
    """Procesar formulario de creación"""
    try:
        estadistica_data = EstadisticaCreate(
            jugador_id=jugador_id,
            partido_id=partido_id,
            minutos_jugados=minutos_jugados,
            goles_anotados=goles_anotados,
            asistencias=asistencias,
            intercepciones=intercepciones,
            balones_recuperados=balones_recuperados,
            tarjetas_amarillas=tarjetas_amarillas,
            tarjetas_rojas=tarjetas_rojas,
            faltas_cometidas=faltas_cometidas
        )

        create_estadistica(estadistica_data, session)
        return RedirectResponse(
            url=f"/partidos/html/detalle/{partido_id}",
            status_code=303
        )

    except HTTPException as e:
        jugadores = session.exec(select(Jugador).where(Jugador.estado == Estado.ACTIVO)).all()
        partidos = session.exec(select(Partido)).all()

        return templates.TemplateResponse(
            "estadisticas/crear.html",
            {
                "request": request,
                "jugadores": jugadores,
                "partidos": partidos,
                "error": e.detail
            }
        )


@router.get("/html/jugador/{jugador_id}", response_class=HTMLResponse)
def historial_jugador_html(
        request: Request,
        jugador_id: int,
        session: Session = Depends(get_session)
):
    """Vista HTML: Historial de estadísticas de un jugador"""
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    # Obtener estadísticas ordenadas por fecha de partido
    estadisticas = session.exec(
        select(Estadistica)
        .where(Estadistica.jugador_id == jugador_id)
        .join(Partido)
        .order_by(Partido.fecha_partido.desc())
    ).all()

    # Calcular totales
    totales = {
        "partidos_jugados": len(estadisticas),
        "minutos_totales": sum(e.minutos_jugados for e in estadisticas),
        "goles_totales": sum(e.goles_anotados for e in estadisticas),
        "asistencias_totales": sum(e.asistencias for e in estadisticas),
        "tarjetas_amarillas": sum(e.tarjetas_amarillas for e in estadisticas),
        "tarjetas_rojas": sum(e.tarjetas_rojas for e in estadisticas),
        "intercepciones_totales": sum(e.intercepciones for e in estadisticas),
        "balones_recuperados_totales": sum(e.balones_recuperados for e in estadisticas)
    }

    return templates.TemplateResponse(
        "estadisticas/historial.html",
        {
            "request": request,
            "jugador": jugador,
            "estadisticas": estadisticas,
            "totales": totales
        }
    )
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional
from datetime import date

from database import get_session
from models import Partido, PartidoCreate, ResultadoPartido

router = APIRouter(prefix="/partidos", tags=["partidos"])
templates = Jinja2Templates(directory="templates")


# ====== API ENDPOINTS ======

@router.post("/", response_model=Partido)
def create_partido(partido: PartidoCreate, session: Session = Depends(get_session)):
    """Crear un nuevo partido"""
    try:
        db_partido = Partido.model_validate(partido)

        # Calcular resultado automáticamente
        db_partido.resultado = db_partido.calcular_resultado()

        session.add(db_partido)
        session.commit()
        session.refresh(db_partido)
        return db_partido

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear partido: {str(e)}")


@router.get("/", response_model=list[Partido])
def read_partidos(
        resultado: Optional[ResultadoPartido] = None,
        session: Session = Depends(get_session)
):
    """Obtener lista de todos los partidos"""
    try:
        statement = select(Partido).order_by(Partido.fecha_partido.desc())
        if resultado:
            statement = statement.where(Partido.resultado == resultado)
        partidos = session.exec(statement).all()
        return partidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener partidos: {str(e)}")


@router.get("/{partido_id}", response_model=Partido)
def read_partido(partido_id: int, session: Session = Depends(get_session)):
    """Obtener un partido por ID"""
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido


@router.delete("/{partido_id}")
def delete_partido(partido_id: int, session: Session = Depends(get_session)):
    """Eliminar un partido"""
    try:
        partido = session.get(Partido, partido_id)
        if not partido:
            raise HTTPException(status_code=404, detail="Partido no encontrado")

        session.delete(partido)
        session.commit()
        return {"message": "Partido eliminado correctamente"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar partido: {str(e)}")


# ====== HTML VIEWS ======

@router.get("/html/lista", response_class=HTMLResponse)
def lista_partidos_html(request: Request, session: Session = Depends(get_session)):
    """Vista HTML: Lista de partidos"""
    partidos = session.exec(
        select(Partido).order_by(Partido.fecha_partido.desc())
    ).all()

    # Calcular estadísticas generales
    total_partidos = len(partidos)
    victorias = len([p for p in partidos if p.resultado == ResultadoPartido.VICTORIA])
    empates = len([p for p in partidos if p.resultado == ResultadoPartido.EMPATE])
    derrotas = len([p for p in partidos if p.resultado == ResultadoPartido.DERROTA])

    goles_favor = sum(p.goles_sigmotaa for p in partidos)
    goles_contra = sum(p.goles_rival for p in partidos)

    estadisticas = {
        "total": total_partidos,
        "victorias": victorias,
        "empates": empates,
        "derrotas": derrotas,
        "goles_favor": goles_favor,
        "goles_contra": goles_contra,
        "diferencia": goles_favor - goles_contra
    }

    return templates.TemplateResponse(
        "partidos/lista.html",
        {
            "request": request,
            "partidos": partidos,
            "estadisticas": estadisticas
        }
    )


@router.get("/html/detalle/{partido_id}", response_class=HTMLResponse)
def detalle_partido_html(
        request: Request,
        partido_id: int,
        session: Session = Depends(get_session)
):
    """Vista HTML: Detalle de partido con estadísticas de jugadores"""
    partido = session.get(Partido, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    return templates.TemplateResponse(
        "partidos/detalle.html",
        {"request": request, "partido": partido}
    )


@router.get("/html/crear", response_class=HTMLResponse)
def crear_partido_form(request: Request):
    """Vista HTML: Formulario de creación"""
    return templates.TemplateResponse(
        "partidos/crear.html",
        {"request": request}
    )


@router.post("/html/crear", response_class=HTMLResponse)
async def crear_partido_submit(
        request: Request,
        rival: str = Form(...),
        fecha_partido: str = Form(...),
        goles_sigmotaa: int = Form(...),
        goles_rival: int = Form(...),
        es_local: bool = Form(False),
        estadio: Optional[str] = Form(None),
        observaciones: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):
    """Procesar formulario de creación"""
    try:
        fecha = date.fromisoformat(fecha_partido)

        partido_data = PartidoCreate(
            rival=rival,
            fecha_partido=fecha,
            goles_sigmotaa=goles_sigmotaa,
            goles_rival=goles_rival,
            es_local=es_local,
            estadio=estadio if estadio else None,
            observaciones=observaciones if observaciones else None
        )

        partido = create_partido(partido_data, session)
        return RedirectResponse(
            url=f"/partidos/html/detalle/{partido.id}",
            status_code=303
        )

    except HTTPException as e:
        return templates.TemplateResponse(
            "partidos/crear.html",
            {"request": request, "error": e.detail}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partidos/crear.html",
            {"request": request, "error": f"Error al crear partido: {str(e)}"}
        )
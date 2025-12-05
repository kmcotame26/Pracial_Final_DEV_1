from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional
from datetime import date, datetime

from database import get_session
from models import (
    Jugador, JugadorCreate, JugadorUpdate,
    Position, Estado, PieDominante
)

router = APIRouter(prefix="/jugadores", tags=["jugadores"])
templates = Jinja2Templates(directory="templates")


# ====== API ENDPOINTS ======

@router.post("/", response_model=Jugador)
def create_jugador(jugador: JugadorCreate, session: Session = Depends(get_session)):
    """Crear un nuevo jugador"""
    try:
        # Verificar número de camiseta único
        existing = session.exec(
            select(Jugador).where(Jugador.numero_camiseta == jugador.numero_camiseta)
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"El número de camiseta {jugador.numero_camiseta} ya está en uso"
            )

        db_jugador = Jugador.model_validate(jugador)
        session.add(db_jugador)
        session.commit()
        session.refresh(db_jugador)
        return db_jugador

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear jugador: {str(e)}")


@router.get("/", response_model=list[Jugador])
def read_jugadores(
        estado: Optional[Estado] = None,
        session: Session = Depends(get_session)
):
    """Obtener lista de todos los jugadores"""
    try:
        statement = select(Jugador)
        if estado:
            statement = statement.where(Jugador.estado == estado)
        jugadores = session.exec(statement).all()
        return jugadores
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener jugadores: {str(e)}")


@router.get("/{jugador_id}", response_model=Jugador)
def read_jugador(jugador_id: int, session: Session = Depends(get_session)):
    """Obtener un jugador por ID"""
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@router.patch("/{jugador_id}", response_model=Jugador)
def update_jugador(
        jugador_id: int,
        jugador_update: JugadorUpdate,
        session: Session = Depends(get_session)
):
    """Actualizar un jugador existente"""
    try:
        db_jugador = session.get(Jugador, jugador_id)
        if not db_jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        # Verificar número de camiseta único si se está actualizando
        if jugador_update.numero_camiseta:
            existing = session.exec(
                select(Jugador).where(
                    Jugador.numero_camiseta == jugador_update.numero_camiseta,
                    Jugador.id != jugador_id
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"El número de camiseta {jugador_update.numero_camiseta} ya está en uso"
                )

        # Actualizar campos
        jugador_data = jugador_update.model_dump(exclude_unset=True)
        for key, value in jugador_data.items():
            setattr(db_jugador, key, value)

        db_jugador.fecha_actualizacion = datetime.utcnow()
        session.add(db_jugador)
        session.commit()
        session.refresh(db_jugador)
        return db_jugador

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar jugador: {str(e)}")


@router.delete("/{jugador_id}")
def delete_jugador(jugador_id: int, session: Session = Depends(get_session)):
    """Eliminar un jugador (soft delete cambiando a INACTIVO)"""
    try:
        jugador = session.get(Jugador, jugador_id)
        if not jugador:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        jugador.estado = Estado.INACTIVO
        session.add(jugador)
        session.commit()
        return {"message": "Jugador marcado como inactivo"}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar jugador: {str(e)}")


# ====== HTML VIEWS ======

@router.get("/html/lista", response_class=HTMLResponse)
def lista_jugadores_html(request: Request, session: Session = Depends(get_session)):
    """Vista HTML: Lista de jugadores"""
    jugadores = session.exec(select(Jugador)).all()
    return templates.TemplateResponse(
        "jugadores/lista.html",
        {"request": request, "jugadores": jugadores}
    )


@router.get("/html/detalle/{jugador_id}", response_class=HTMLResponse)
def detalle_jugador_html(
        request: Request,
        jugador_id: int,
        session: Session = Depends(get_session)
):
    """Vista HTML: Detalle de jugador con estadísticas"""
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return templates.TemplateResponse(
        "jugadores/detalle.html",
        {"request": request, "jugador": jugador}
    )


@router.get("/html/crear", response_class=HTMLResponse)
def crear_jugador_form(request: Request):
    """Vista HTML: Formulario de creación"""
    return templates.TemplateResponse(
        "jugadores/crear.html",
        {
            "request": request,
            "posiciones": [p.value for p in Position],
            "estados": [e.value for e in Estado],
            "pies": [p.value for p in PieDominante]
        }
    )


@router.post("/html/crear", response_class=HTMLResponse)
async def crear_jugador_submit(
        request: Request,
        nombre_completo: str = Form(...),
        numero_camiseta: int = Form(...),
        fecha_nacimiento: str = Form(...),
        nacionalidad: str = Form(...),
        altura_cm: int = Form(...),
        peso_kg: float = Form(...),
        pie_dominante: str = Form(...),
        posicion: str = Form(...),
        valor_mercado: float = Form(0.0),
        anio_ingreso: int = Form(...),
        fotografia_url: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):
    """Procesar formulario de creación"""
    try:
        fecha_nac = date.fromisoformat(fecha_nacimiento)

        jugador_data = JugadorCreate(
            nombre_completo=nombre_completo,
            numero_camiseta=numero_camiseta,
            fecha_nacimiento=fecha_nac,
            nacionalidad=nacionalidad,
            altura_cm=altura_cm,
            peso_kg=peso_kg,
            pie_dominante=PieDominante(pie_dominante),
            posicion=Position(posicion),
            valor_mercado=valor_mercado,
            anio_ingreso=anio_ingreso,
            fotografia_url=fotografia_url if fotografia_url else None
        )

        create_jugador(jugador_data, session)
        return RedirectResponse(url="/jugadores/html/lista", status_code=303)

    except HTTPException as e:
        return templates.TemplateResponse(
            "jugadores/crear.html",
            {
                "request": request,
                "error": e.detail,
                "posiciones": [p.value for p in Position],
                "estados": [e.value for e in Estado],
                "pies": [p.value for p in PieDominante]
            }
        )


@router.get("/html/editar/{jugador_id}", response_class=HTMLResponse)
def editar_jugador_form(
        request: Request,
        jugador_id: int,
        session: Session = Depends(get_session)
):
    """Vista HTML: Formulario de edición"""
    jugador = session.get(Jugador, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return templates.TemplateResponse(
        "jugadores/editar.html",
        {
            "request": request,
            "jugador": jugador,
            "posiciones": [p.value for p in Position],
            "estados": [e.value for e in Estado],
            "pies": [p.value for p in PieDominante]
        }
    )


@router.post("/html/editar/{jugador_id}", response_class=HTMLResponse)
async def editar_jugador_submit(
        request: Request,
        jugador_id: int,
        nombre_completo: str = Form(...),
        numero_camiseta: int = Form(...),
        estado: str = Form(...),
        session: Session = Depends(get_session)
):
    """Procesar formulario de edición"""
    try:
        jugador_update = JugadorUpdate(
            nombre_completo=nombre_completo,
            numero_camiseta=numero_camiseta,
            estado=Estado(estado)
        )

        update_jugador(jugador_id, jugador_update, session)
        return RedirectResponse(
            url=f"/jugadores/html/detalle/{jugador_id}",
            status_code=303
        )

    except HTTPException as e:
        jugador = session.get(Jugador, jugador_id)
        return templates.TemplateResponse(
            "jugadores/editar.html",
            {
                "request": request,
                "jugador": jugador,
                "error": e.detail,
                "posiciones": [p.value for p in Position],
                "estados": [e.value for e in Estado],
                "pies": [p.value for p in PieDominante]
            }
        )
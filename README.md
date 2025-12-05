# Parcial Final Karol y Laura

Instrucciones:

1. Crear y activar entorno virtual:
   - `python -m venv .venv`
   - Windows: `source .venv\Scripts\activate`
   - Linux: `source .venv/bin/activate`

2. Instalar dependencias:
   - `pip install -r requirements.txt`

3. Iniciar servidor:
   - `uvicorn main:app --reload`

4. Rutas:
   - Web UI: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs

Estructura:
- main.py
- database.py (inicia DB)
- models.py (todas las tablas SQLModel)
- routers/ (API y vistas HTML)
- templates/ (Jinja2)
- static/ (CSS)

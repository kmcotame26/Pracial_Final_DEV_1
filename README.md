#  Parcial laura y karol - Sistema de Gestión

Sistema integral de gestión de jugadores, partidos y estadísticas para el equipo sigmotaa FC. Desarrollado con FastAPI, SQLModel y HTML/CSS.

##  Descripción

Este sistema permite a los entrenadores:
- Registrar y gestionar jugadores del plantel
- Controlar estados (activo, inactivo, lesionado, suspendido)
- Registrar partidos con resultados automáticos
- Llevar estadísticas detalladas por jugador y partido
- Visualizar historial completo de desempeño

##  Tecnologías

- **Backend**: FastAPI 0.109+
- **Base de Datos**: SQLModel + SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Despliegue**: Render / Railway / Clever Cloud

##  Instalación Local

### Requisitos Previos
- Python 3.10+
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/sigmotoa/Final_DEV_1.git
cd Final_DEV_1
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
uvicorn main:app --reload
```

5. **Abrir en navegador**
```
http://localhost:8000
```

##  Estructura del Proyecto

```
Final_DEV_1/
│
├── main.py                 # Aplicación principal
├── database.py             # Configuración de BD
├── models.py               # Modelos SQLModel
│
├── routers/
│   ├── jugadores.py       # Endpoints de jugadores
│   ├── partidos.py        # Endpoints de partidos
│   └── estadisticas.py    # Endpoints de estadísticas
│
├── templates/
│   ├── base.html          # Template base
│   ├── index.html         # Página principal
│   ├── jugadores/
│   │   ├── lista.html
│   │   ├── detalle.html
│   │   ├── crear.html
│   │   └── editar.html
│   ├── partidos/
│   │   ├── lista.html
│   │   ├── detalle.html
│   │   └── crear.html
│   └── estadisticas/
│       ├── crear.html
│       └── historial.html
│
├── static/
│   └── style.css          # Estilos CSS
│
├── requirements.txt
├── runtime.txt
└── README.md
```

##  Endpoints Principales

### Interfaz HTML
- `GET /` - Página principal
- `GET /jugadores/html/lista` - Lista de jugadores
- `GET /jugadores/html/crear` - Formulario nuevo jugador
- `GET /jugadores/html/detalle/{id}` - Detalle de jugador
- `GET /partidos/html/lista` - Lista de partidos
- `GET /partidos/html/crear` - Formulario nuevo partido
- `GET /estadisticas/html/crear` - Formulario nueva estadística

### API REST
- `GET /docs` - Documentación interactiva Swagger
- `GET /redoc` - Documentación ReDoc

#### Jugadores
- `POST /jugadores/` - Crear jugador
- `GET /jugadores/` - Listar jugadores
- `GET /jugadores/{id}` - Obtener jugador
- `PATCH /jugadores/{id}` - Actualizar jugador
- `DELETE /jugadores/{id}` - Eliminar jugador (soft delete)

#### Partidos
- `POST /partidos/` - Crear partido
- `GET /partidos/` - Listar partidos
- `GET /partidos/{id}` - Obtener partido
- `DELETE /partidos/{id}` - Eliminar partido

#### Estadísticas
- `POST /estadisticas/` - Crear estadística
- `GET /estadisticas/` - Listar estadísticas
- `GET /estadisticas/{id}` - Obtener estadística
- `DELETE /estadisticas/{id}` - Eliminar estadística

## Funcionalidades Principales

### RF-01: Gestión de Jugadores
-  Formulario completo con validación
-  Número de camiseta único (1-99)
-  Vista lista y detalle
-  Edición de jugadores
-  Gestión de estados (activo/inactivo/lesionado/suspendido)

### RF-02: Estadísticas por Partido
-  Registro de minutos, goles, tarjetas
-  Consulta de historial por jugador
-  Actualización automática de estado por tarjetas

### RF-03: Gestión de Partidos
-  Formulario con datos del encuentro
-  Cálculo automático de resultado (Victoria/Empate/Derrota)
-  Vista detalle con estadísticas de jugadores

### RF-04: Interfaz HTML
-  Formularios con validación HTML5
-  Vistas organizadas en tablas
-  Navegación con menú principal
-  Mensajes de confirmación y error

### RNF-01: Código Profesional
-  FastAPI con decoradores y routers
-  Separación en capas (modelos, routers, templates)
-  Validación con Pydantic/SQLModel
-  Manejo de errores con HTTPException

### RNF-02: Base de Datos
-  SQLModel con table=True
-  Tres tablas con relaciones (jugadores, partidos, estadísticas)
-  Persistencia de datos


### Comandos Render/Railway
```bash
# Instalar dependencias
pip install -r requirements.txt

# Comando de inicio
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Modelos de Datos

### Jugador
- Datos personales (nombre, número, fecha nacimiento, nacionalidad)
- Datos deportivos (altura, peso, pie dominante, posición)
- Estado (activo, inactivo, lesionado, suspendido)
- Relación: muchas estadísticas

### Partido
- Información del encuentro (rival, fecha, goles, local/visitante)
- Resultado automático (Victoria/Empate/Derrota)
- Relación: muchas estadísticas

### Estadistica
- Rendimiento individual (minutos, goles, asistencias, tarjetas)
- Foreign keys: jugador_id, partido_id

##  Datos de Prueba

Ejecutar en la consola de Python:
```python
from create_test_data import crear_datos_prueba
crear_datos_prueba()
```



Desarrollado para el examen final de Desarrollo 1


- **Repositorio GitHub**: [https://github.com/sigmotoa/Final_DEV_1](https://github.com/kmcotame26/Parcial_Final_DEV_1)

- **URL de Despliegue**: 

- **Documentación API**: 

##  Licencia

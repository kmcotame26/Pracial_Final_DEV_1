#  Parcial laura y karol 🌸

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

- ### Detalle de Parámetros y Restricciones
#### 1. Entidad: Jugador () `jugadores`

| Campo | Tipo | Restricciones / Descripción |
| --- | --- | --- |
| `nombre_completo` | String | Min: 3, Max: 100 caracteres. Indexado. |
| `numero_camiseta` | Int | Entre 1 y 99. Único en el sistema. |
| `fecha_nacimiento` | Date | Fecha de nacimiento. |
| `nacionalidad` | String | Min: 2, Max: 50 caracteres. |
| `altura_cm` | Int | Entre 150 y 220 cm. |
| `peso_kg` | Float | Entre 50.0 y 120.0 kg. |
| `pie_dominante` | Enum | , , . `DERECHO``IZQUIERDO``AMBIDIESTRO` |
| `posicion` | Enum | Ej: `ARQUERO`, `DEFENSA CENTRAL`, `VOLANTE OFENSIVO`, etc. |
| `estado` | Enum | `ACTIVO` (Default), `INACTIVO`, `LESIONADO`, . `SUSPENDIDO` |

###2. Partido () `partidos`

| Campo | Tipo | Restricciones / Descripción |
| --- | --- | --- |
| `rival` | String | Min: 3, Max: 100 caracteres. Nombre del equipo contrario. |
| `fecha_partido` | Date | Fecha del encuentro. |
| `goles_sigmotaa` | Int | Mayor o igual a 0. Goles propios. |
| `goles_rival` | Int | Mayor o igual a 0. Goles recibidos. |
| `es_local` | Bool | `True` si es local, `False` si es visitante. |
| `resultado` | Enum | Calculado auto.: , , . `VICTORIA``EMPATE``DERROTA` |
#### 3. Estadistica (`estadisticas`)
Representa el rendimiento individual de un jugador en un partido específico. | Campo | Tipo | Restricciones / Descripción | | :--- | :--- | :--- | | `minutos_jugados` | Int | Entre 0 y 120 minutos. | | `tarjetas_amarillas`| Int | Máximo 2 por partido. | | `tarjetas_rojas` | Int | Máximo 1 por partido. |
## 🚀 Endpoints del API
La API está organizada en tres routers principales.
### 👤 Jugadores (`/jugadores`)
Gestiona la plantilla del equipo.

| Método | Endpoint | Descripción | Parámetros Body/Query |
| --- | --- | --- | --- |
| `POST` | `/jugadores/` | Crear un nuevo jugador. | JSON () `JugadorCreate` |
| `GET` | `/jugadores/` | Listar todos los jugadores. | `offset` (int), `limit` (int) |
| `GET` | `/jugadores/{jugador_id}` | Obtener detalle de un jugador. | `jugador_id` (path) |
| `PATCH` | `/jugadores/{jugador_id}` | Actualizar datos parciales. | `jugador_id`, JSON () `JugadorUpdate` |
| `DELETE` | `/jugadores/{jugador_id}` | Eliminar un jugador. | `jugador_id` |
### 🏟️ Partidos (`/partidos`)
Gestiona el calendario y resultados.

| Método | Endpoint | Descripción | Parámetros Body/Query |
| --- | --- | --- | --- |
| `POST` | `/partidos/` | Registrar un nuevo partido. | JSON () `PartidoCreate` |
| `GET` | `/partidos/` | Listar historial de partidos. | `offset`, `limit` |
| `GET` | `/partidos/{partido_id}` | Ver detalle de un partido. | `partido_id` |
| `GET` | `/partidos/{partido_id}/estadisticas` | **Estadísticas del partido**: Devuelve el partido con la lista de estadísticas de los jugadores que participaron. | `partido_id` |
| `PATCH` | `/partidos/{partido_id}` | Actualizar resultado/datos. | `partido_id`, JSON Update |
| `DELETE` | `/partidos/{partido_id}` | Eliminar partido. | `partido_id` |
### 📊 Estadísticas (`/estadisticas`)
Gestiona los datos de rendimiento individual por partido.

| Método | Endpoint | Descripción | Parámetros Body/Query |
| --- | --- | --- | --- |
| `POST` | `/estadisticas/` | Crear registro estadístico. | JSON ( con `jugador_id` y `partido_id`) `EstadisticaCreate` |
| `GET` | `/estadisticas/` | Listar todas las estadísticas. | `offset`, `limit` |
| `GET` | `/estadisticas/{estadistica_id}` | Ver una estadística puntual. | `estadistica_id` |
| `PATCH` | `/estadisticas/{estadistica_id}` | Actualizar datos (goles, minutos, etc). | `estadistica_id`, JSON Update |
| `DELETE` | `/estadisticas/{estadistica_id}` | Eliminar registro. | `estadistica_id` |

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**
```bash
uvicorn main:app --reload
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


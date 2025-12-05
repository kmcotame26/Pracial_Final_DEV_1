from datetime import date, datetime
from sqlmodel import Session
from database import engine, create_db_and_tables
from models import (
    Jugador, Partido, Estadistica,
    Position, Estado, PieDominante, ResultadoPartido
)


def crear_datos_prueba():
    """Crea datos de prueba para validar el funcionamiento del sistema"""

    # Crear tablas
    create_db_and_tables()

    with Session(engine) as session:
        # Verificar si ya existen datos
        existing = session.query(Jugador).first()
        if existing:
            print("⚠️  Ya existen datos en la base de datos. Saltando creación de datos de prueba.")
            return

        print("📝 Creando datos de prueba...")

        # ===== JUGADORES =====
        jugadores = [
            Jugador(
                nombre_completo="Carlos Martínez Rodríguez",
                numero_camiseta=1,
                fecha_nacimiento=date(1995, 3, 15),
                nacionalidad="Colombia",
                altura_cm=185,
                peso_kg=80.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.ARQUERO,
                valor_mercado=500000.0,
                anio_ingreso=2020,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Andrés Felipe García",
                numero_camiseta=4,
                fecha_nacimiento=date(1998, 7, 22),
                nacionalidad="Colombia",
                altura_cm=180,
                peso_kg=75.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.DEFENSA_C,
                valor_mercado=800000.0,
                anio_ingreso=2021,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Juan Pablo Sánchez",
                numero_camiseta=2,
                fecha_nacimiento=date(1997, 11, 8),
                nacionalidad="Colombia",
                altura_cm=178,
                peso_kg=72.0,
                pie_dominante=PieDominante.IZQUIERDO,
                posicion=Position.DEFENSA_L,
                valor_mercado=600000.0,
                anio_ingreso=2022,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Miguel Ángel Torres",
                numero_camiseta=5,
                fecha_nacimiento=date(1996, 5, 12),
                nacionalidad="Argentina",
                altura_cm=182,
                peso_kg=77.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.VOLANTE_D,
                valor_mercado=900000.0,
                anio_ingreso=2021,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Luis Fernando Gómez",
                numero_camiseta=8,
                fecha_nacimiento=date(1999, 2, 28),
                nacionalidad="Colombia",
                altura_cm=175,
                peso_kg=70.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.VOLANTE_C,
                valor_mercado=1000000.0,
                anio_ingreso=2023,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Santiago Ramírez",
                numero_camiseta=10,
                fecha_nacimiento=date(1997, 9, 5),
                nacionalidad="Colombia",
                altura_cm=176,
                peso_kg=71.0,
                pie_dominante=PieDominante.IZQUIERDO,
                posicion=Position.VOLANTE_O,
                valor_mercado=1500000.0,
                anio_ingreso=2020,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="David Alejandro López",
                numero_camiseta=7,
                fecha_nacimiento=date(1998, 12, 18),
                nacionalidad="Colombia",
                altura_cm=172,
                peso_kg=68.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.VOLANTE_E,
                valor_mercado=1200000.0,
                anio_ingreso=2022,
                estado=Estado.LESIONADO
            ),
            Jugador(
                nombre_completo="Roberto Carlos Silva",
                numero_camiseta=9,
                fecha_nacimiento=date(1996, 4, 30),
                nacionalidad="Brasil",
                altura_cm=183,
                peso_kg=79.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.DELANTERO_C,
                valor_mercado=2000000.0,
                anio_ingreso=2021,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Pedro Antonio Vargas",
                numero_camiseta=11,
                fecha_nacimiento=date(2000, 1, 14),
                nacionalidad="Colombia",
                altura_cm=179,
                peso_kg=73.0,
                pie_dominante=PieDominante.IZQUIERDO,
                posicion=Position.DELANTERO_P,
                valor_mercado=800000.0,
                anio_ingreso=2023,
                estado=Estado.ACTIVO
            ),
            Jugador(
                nombre_completo="Javier Hernández",
                numero_camiseta=3,
                fecha_nacimiento=date(1994, 8, 20),
                nacionalidad="México",
                altura_cm=181,
                peso_kg=76.0,
                pie_dominante=PieDominante.DERECHO,
                posicion=Position.DEFENSA_C,
                valor_mercado=700000.0,
                anio_ingreso=2019,
                estado=Estado.SUSPENDIDO
            )
        ]

        for jugador in jugadores:
            session.add(jugador)
        session.commit()
        print(f"✅ {len(jugadores)} jugadores creados")

        # Refrescar jugadores para obtener IDs
        for jugador in jugadores:
            session.refresh(jugador)

        # ===== PARTIDOS =====
        partidos = [
            Partido(
                rival="Deportivo Cali",
                fecha_partido=date(2024, 11, 15),
                goles_sigmotaa=3,
                goles_rival=1,
                es_local=True,
                estadio="Estadio Olímpico",
                resultado=ResultadoPartido.VICTORIA
            ),
            Partido(
                rival="América de Cali",
                fecha_partido=date(2024, 11, 22),
                goles_sigmotaa=2,
                goles_rival=2,
                es_local=False,
                estadio="Pascual Guerrero",
                resultado=ResultadoPartido.EMPATE
            ),
            Partido(
                rival="Millonarios FC",
                fecha_partido=date(2024, 11, 29),
                goles_sigmotaa=1,
                goles_rival=2,
                es_local=True,
                estadio="Estadio Olímpico",
                resultado=ResultadoPartido.DERROTA
            ),
            Partido(
                rival="Atlético Nacional",
                fecha_partido=date(2024, 12, 3),
                goles_sigmotaa=4,
                goles_rival=0,
                es_local=True,
                estadio="Estadio Olímpico",
                resultado=ResultadoPartido.VICTORIA
            )
        ]

        for partido in partidos:
            session.add(partido)
        session.commit()
        print(f"✅ {len(partidos)} partidos creados")

        # Refrescar partidos para obtener IDs
        for partido in partidos:
            session.refresh(partido)

        # ===== ESTADÍSTICAS =====
        # Partido 1: Victoria 3-1
        estadisticas_p1 = [
            Estadistica(jugador_id=jugadores[0].id, partido_id=partidos[0].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[1].id, partido_id=partidos[0].id, minutos_jugados=90, intercepciones=5),
            Estadistica(jugador_id=jugadores[2].id, partido_id=partidos[0].id, minutos_jugados=90, intercepciones=3),
            Estadistica(jugador_id=jugadores[3].id, partido_id=partidos[0].id, minutos_jugados=90,
                        balones_recuperados=8),
            Estadistica(jugador_id=jugadores[4].id, partido_id=partidos[0].id, minutos_jugados=90, asistencias=2),
            Estadistica(jugador_id=jugadores[5].id, partido_id=partidos[0].id, minutos_jugados=90, goles_anotados=1,
                        asistencias=1),
            Estadistica(jugador_id=jugadores[7].id, partido_id=partidos[0].id, minutos_jugados=90, goles_anotados=2),
            Estadistica(jugador_id=jugadores[8].id, partido_id=partidos[0].id, minutos_jugados=75),
        ]

        # Partido 2: Empate 2-2
        estadisticas_p2 = [
            Estadistica(jugador_id=jugadores[0].id, partido_id=partidos[1].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[1].id, partido_id=partidos[1].id, minutos_jugados=90,
                        tarjetas_amarillas=1),
            Estadistica(jugador_id=jugadores[2].id, partido_id=partidos[1].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[3].id, partido_id=partidos[1].id, minutos_jugados=90,
                        balones_recuperados=6),
            Estadistica(jugador_id=jugadores[4].id, partido_id=partidos[1].id, minutos_jugados=90, goles_anotados=1),
            Estadistica(jugador_id=jugadores[5].id, partido_id=partidos[1].id, minutos_jugados=80, asistencias=1),
            Estadistica(jugador_id=jugadores[7].id, partido_id=partidos[1].id, minutos_jugados=90, goles_anotados=1),
            Estadistica(jugador_id=jugadores[8].id, partido_id=partidos[1].id, minutos_jugados=90),
        ]

        # Partido 3: Derrota 1-2
        estadisticas_p3 = [
            Estadistica(jugador_id=jugadores[0].id, partido_id=partidos[2].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[1].id, partido_id=partidos[2].id, minutos_jugados=90, intercepciones=4),
            Estadistica(jugador_id=jugadores[2].id, partido_id=partidos[2].id, minutos_jugados=90,
                        tarjetas_amarillas=1),
            Estadistica(jugador_id=jugadores[3].id, partido_id=partidos[2].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[4].id, partido_id=partidos[2].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[5].id, partido_id=partidos[2].id, minutos_jugados=90, goles_anotados=1),
            Estadistica(jugador_id=jugadores[7].id, partido_id=partidos[2].id, minutos_jugados=65),
            Estadistica(jugador_id=jugadores[8].id, partido_id=partidos[2].id, minutos_jugados=90,
                        tarjetas_amarillas=2),
        ]

        # Partido 4: Victoria 4-0
        estadisticas_p4 = [
            Estadistica(jugador_id=jugadores[0].id, partido_id=partidos[3].id, minutos_jugados=90),
            Estadistica(jugador_id=jugadores[1].id, partido_id=partidos[3].id, minutos_jugados=90, intercepciones=6),
            Estadistica(jugador_id=jugadores[2].id, partido_id=partidos[3].id, minutos_jugados=90, goles_anotados=1),
            Estadistica(jugador_id=jugadores[3].id, partido_id=partidos[3].id, minutos_jugados=90,
                        balones_recuperados=10),
            Estadistica(jugador_id=jugadores[4].id, partido_id=partidos[3].id, minutos_jugados=90, asistencias=2),
            Estadistica(jugador_id=jugadores[5].id, partido_id=partidos[3].id, minutos_jugados=90, goles_anotados=1,
                        asistencias=1),
            Estadistica(jugador_id=jugadores[7].id, partido_id=partidos[3].id, minutos_jugados=90, goles_anotados=2,
                        asistencias=1),
            Estadistica(jugador_id=jugadores[8].id, partido_id=partidos[3].id, minutos_jugados=85),
        ]

        todas_estadisticas = estadisticas_p1 + estadisticas_p2 + estadisticas_p3 + estadisticas_p4

        for estadistica in todas_estadisticas:
            session.add(estadistica)
        session.commit()
        print(f"✅ {len(todas_estadisticas)} estadísticas creadas")

        print("\n✨ ¡Datos de prueba creados exitosamente!")
        print(f"\n📊 Resumen:")
        print(f"   • {len(jugadores)} jugadores")
        print(f"   • {len(partidos)} partidos")
        print(f"   • {len(todas_estadisticas)} registros de estadísticas")
        print(f"\n🌐 Accede a la aplicación en: http://localhost:8000")


if __name__ == "__main__":
    crear_datos_prueba()
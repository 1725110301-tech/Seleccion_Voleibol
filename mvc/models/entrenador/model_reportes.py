from mvc.helpers import fechas
from mvc.models.comun import model_asistencias, model_jugadores, model_partidos
from mvc.models.comun.conexion import consultar


def reporte_general(rama, desde, hasta):
    """RF-10: asistencias por jugador y resultados de partidos en el rango."""
    jugadores = model_asistencias.jugadores_con_asistencia(rama, desde, hasta)
    partidos = model_partidos.listar(rama, desde, hasta)
    return {
        "jugadores": jugadores,
        "partidos": partidos,
        "ganados": sum(1 for p in partidos if p.resultado == "ganado"),
        "perdidos": sum(1 for p in partidos if p.resultado == "perdido"),
    }


def reporte_individual(jugador_id, desde, hasta):
    """RF-18: días que entrenó, faltas, % y partidos disponible/convocado."""
    j = model_jugadores.obtener(jugador_id)
    if not j:
        return None
    entrenos = consultar("""select e.fecha, e.hora_inicio, a.estado, a.motivo from asistencias a
                            join entrenamientos e on e.id = a.entrenamiento_id
                            where a.jugador_id = %s and e.fecha between %s and %s order by e.fecha""",
                         (jugador_id, desde, hasta))
    total = consultar("""select count(*) n from entrenamientos where rama = %s and estado = 'programado'
                         and fecha between %s and %s and fecha <= %s""",
                      (j.rama, desde, hasta, fechas.hoy()), uno=True).n
    presentes = sum(1 for e in entrenos if e.estado == "presente")
    return {
        "jugador": j,
        "entrenos": entrenos,
        "presentes": presentes,
        "faltas": sum(1 for e in entrenos if e.estado == "falta"),
        "porcentaje": round(100.0 * presentes / total, 1) if total else 0.0,
        "disponible": consultar("""select p.fecha, p.rival from disponibilidad d join partidos p on p.id = d.partido_id
                                   where d.jugador_id = %s and d.puede_asistir and p.fecha between %s and %s
                                   order by p.fecha""", (jugador_id, desde, hasta)),
        "convocado": consultar("""select c.nombre, c.fecha_inicio, c.fecha_fin from convocatorias cv
                                  join competencias c on c.id = cv.competencia_id
                                  where cv.jugador_id = %s and c.fecha_inicio <= %s and c.fecha_fin >= %s""",
                               (jugador_id, hasta, desde)),
    }

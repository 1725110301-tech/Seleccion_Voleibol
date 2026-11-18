from mvc.models.comun.conexion import conectar, consultar

MAX_CONVOCADOS = 12


def convocados(competencia_id, rama):
    filas = consultar("""select cv.jugador_id from convocatorias cv join jugadores j on j.id = cv.jugador_id
                         where cv.competencia_id = %s and j.rama = %s""", (competencia_id, rama))
    return {f.jugador_id for f in filas}


def guardar(competencia_id, jugador_ids, rama):
    """RF-17: máximo 12 jugadores activos de la misma rama para un torneo."""
    comp = consultar("select tipo from competencias where id = %s", (competencia_id,), uno=True)
    if not comp or comp.tipo != "torneo":
        return False, "Selecciona un torneo válido"
    if len(jugador_ids) > MAX_CONVOCADOS:
        return False, "Máximo %d jugadores por convocatoria" % MAX_CONVOCADOS
    if jugador_ids:
        validos = consultar("select id from jugadores where id = any(%s) and rama = %s and estado = 'activo'",
                            (jugador_ids, rama))
        if len(validos) != len(set(jugador_ids)):
            return False, "Solo se pueden convocar jugadores activos de la rama seleccionada"
    con = conectar()
    try:
        with con:
            with con.cursor() as cur:
                cur.execute("""delete from convocatorias where competencia_id = %s
                               and jugador_id in (select id from jugadores where rama = %s)""",
                            (competencia_id, rama))
                for jid in jugador_ids:
                    cur.execute("insert into convocatorias (competencia_id, jugador_id) values (%s,%s)",
                                (competencia_id, jid))
    finally:
        con.close()
    return True, "Convocatoria guardada"

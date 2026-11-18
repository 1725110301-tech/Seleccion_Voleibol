from datetime import timedelta
from mvc.helpers import fechas
from mvc.models.comun.conexion import conectar, consultar


def sabado_limite(fecha_partido):
    """Último día para editar: el sábado anterior al partido (RF-16)."""
    delta = (fecha_partido.weekday() - 5) % 7 or 7
    return fecha_partido - timedelta(days=delta)


def actuales(partido_id):
    return {f.jugador_id: f.puede_asistir
            for f in consultar("select jugador_id, puede_asistir from disponibilidad where partido_id = %s",
                               (partido_id,))}


def guardar(partido_id, respuestas):
    """RF-16: respuestas = {jugador_id: bool}. Solo hasta el sábado anterior al partido."""
    p = consultar("""select p.fecha, c.tipo from partidos p join competencias c on c.id = p.competencia_id
                     where p.id = %s""", (partido_id,), uno=True)
    if not p or p.tipo != "liga":
        return False, "La disponibilidad solo aplica a partidos de liga"
    if fechas.hoy() > sabado_limite(p.fecha):
        return False, "Ya no se puede modificar: el límite era el sábado %s" % sabado_limite(p.fecha)
    con = conectar()
    try:
        with con:
            with con.cursor() as cur:
                for jid, puede in respuestas.items():
                    cur.execute("""insert into disponibilidad (partido_id, jugador_id, puede_asistir)
                                   values (%s,%s,%s)
                                   on conflict (partido_id, jugador_id)
                                   do update set puede_asistir = excluded.puede_asistir""",
                                (partido_id, jid, puede))
    finally:
        con.close()
    return True, "Disponibilidad guardada"

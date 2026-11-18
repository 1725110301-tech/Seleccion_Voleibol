from mvc.helpers import fechas
from mvc.models.comun.conexion import conectar, consultar


def jugadores_para_lista(rama):
    """RF-03: solo jugadores con estado 'activo'."""
    return consultar("select id, nombre, numero_playera, posicion from jugadores "
                     "where rama = %s and estado = 'activo' order by numero_playera", (rama,))


def guardar(entrenamiento_id, registros):
    """RF-05 + RF-14: guarda el pase de lista; bloquea si ya existe registro del jugador."""
    if not entrenamiento_id:
        return False, "Selecciona un entrenamiento"
    ent = consultar("select id, estado from entrenamientos where id = %s", (entrenamiento_id,), uno=True)
    if not ent or ent.estado != "programado":
        return False, "El entrenamiento no existe o está cancelado"
    if not registros:
        return False, "No hay jugadores activos para pasar lista"
    for r in registros:
        if r["estado"] not in ("presente", "falta", "justificada"):
            return False, "Marca presente, falta o justificada para %s" % r["nombre"]
        if r["estado"] == "justificada" and len(r["motivo"] or "") < 10:
            return False, "El motivo de %s debe tener al menos 10 caracteres" % r["nombre"]
    ids = [r["jugador_id"] for r in registros]
    dup = consultar("""select j.nombre from asistencias a join jugadores j on j.id = a.jugador_id
                       where a.entrenamiento_id = %s and a.jugador_id = any(%s)""", (entrenamiento_id, ids))
    if dup:
        return False, "Ya existe asistencia registrada para: " + ", ".join(d.nombre for d in dup)
    con = conectar()
    try:
        with con:
            with con.cursor() as cur:
                for r in registros:
                    cur.execute("insert into asistencias (entrenamiento_id, jugador_id, estado, motivo) "
                                "values (%s,%s,%s,%s)",
                                (entrenamiento_id, r["jugador_id"], r["estado"], r["motivo"]))
    finally:
        con.close()
    return True, "Asistencia guardada correctamente"


def posibles_bajas(rama):
    """RF-13: activos sin ninguna asistencia en los últimos 12 entrenamientos (3 semanas)."""
    filas = consultar("""
        with ult as (select id from entrenamientos where rama = %s and estado = 'programado'
                     and fecha <= %s order by fecha desc, hora_inicio desc limit 12)
        select j.id from jugadores j
        where j.rama = %s and j.estado = 'activo' and (select count(*) from ult) = 12
          and not exists (select 1 from asistencias a where a.jugador_id = j.id
                          and a.estado = 'presente' and a.entrenamiento_id in (select id from ult))
        """, (rama, fechas.hoy(), rama))
    return [f.id for f in filas]


def jugadores_con_asistencia(rama, desde=None, hasta=None):
    """RF-06 + RF-13: jugadores con % de asistencia y marca 'posible baja'."""
    hasta = hasta or fechas.hoy()
    filtro, params = " and e.fecha <= %s", [rama, hasta]
    if desde:
        filtro += " and e.fecha >= %s"
        params.append(desde)
    total = consultar("select count(*) n from entrenamientos e where e.rama = %s and e.estado = 'programado'"
                      + filtro, params, uno=True).n
    conteos = {}
    for f in consultar("""select a.jugador_id, a.estado, count(*) n from asistencias a
                          join entrenamientos e on e.id = a.entrenamiento_id
                          where e.rama = %s and e.estado = 'programado'""" + filtro +
                       " group by a.jugador_id, a.estado", params):
        conteos.setdefault(f.jugador_id, {})[f.estado] = f.n
    bajas = set(posibles_bajas(rama))
    jugadores = consultar("select * from jugadores where rama = %s order by estado, numero_playera", (rama,))
    for j in jugadores:
        c = conteos.get(j.id, {})
        j.asistencias = c.get("presente", 0)
        j.faltas = c.get("falta", 0)
        j.justificadas = c.get("justificada", 0)
        j.total = total
        j.porcentaje = round(100.0 * j.asistencias / total, 1) if total else 0.0
        j.posible_baja = j.id in bajas
    return jugadores


def historial(rama, desde, hasta):
    return consultar("""select e.fecha, e.hora_inicio, e.tipo, j.nombre, j.numero_playera, a.estado, a.motivo
                        from asistencias a join entrenamientos e on e.id = a.entrenamiento_id
                        join jugadores j on j.id = a.jugador_id
                        where e.rama = %s and e.fecha between %s and %s
                        order by e.fecha desc, e.hora_inicio, j.numero_playera""", (rama, desde, hasta))

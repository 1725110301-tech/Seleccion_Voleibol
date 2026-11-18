from datetime import timedelta
from mvc.helpers import fechas
from mvc.models.comun.conexion import conectar, consultar, ejecutar

# RF-15: (día de la semana 0=lunes, inicio, fin)
HORARIO_FIJO = [(0, "13:00", "15:00"), (1, "16:30", "18:00"), (3, "16:30", "18:00"), (4, "08:30", "10:30")]


def crear_extra(rama, fecha, hora_inicio, hora_fin):
    """RF-04: entrenamiento extra sin empalmarse con otro de la misma rama."""
    if not (fecha and hora_inicio and hora_fin):
        return False, "Fecha, hora de inicio y hora de fin son obligatorias"
    if hora_fin <= hora_inicio:
        return False, "La hora de fin debe ser mayor a la de inicio"
    choque = consultar("""select 1 from entrenamientos where rama = %s and fecha = %s and estado = 'programado'
                          and hora_inicio < %s and hora_fin > %s""", (rama, fecha, hora_fin, hora_inicio), uno=True)
    if choque:
        return False, "El horario se empalma con otro entrenamiento de la misma rama"
    ejecutar("insert into entrenamientos (fecha, hora_inicio, hora_fin, rama, tipo) values (%s,%s,%s,%s,'extra')",
             (fecha, hora_inicio, hora_fin, rama))
    return True, "Entrenamiento extra creado y habilitado para pase de lista"


def generar_semana(referencia=None):
    """RF-15: crea los 4 entrenamientos fijos por rama (idempotente). Devuelve cuántos creó."""
    h = referencia or fechas.hoy()
    lunes = h - timedelta(days=h.weekday())
    creados = 0
    con = conectar()
    try:
        with con:
            with con.cursor() as cur:
                for rama in ("femenil", "varonil"):
                    for dia, ini, fin in HORARIO_FIJO:
                        cur.execute("""insert into entrenamientos (fecha, hora_inicio, hora_fin, rama, tipo)
                                       values (%s,%s,%s,%s,'fijo') on conflict (fecha, hora_inicio, rama) do nothing""",
                                    (lunes + timedelta(days=dia), ini, fin, rama))
                        creados += cur.rowcount
    finally:
        con.close()
    return creados

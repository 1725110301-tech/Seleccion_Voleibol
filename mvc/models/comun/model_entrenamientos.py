from mvc.helpers import fechas
from mvc.models.comun.conexion import consultar


def obtener(entrenamiento_id):
    return consultar("select * from entrenamientos where id = %s", (entrenamiento_id,), uno=True)


def listar(rama, desde, hasta):
    return consultar("""select * from entrenamientos where rama = %s and fecha between %s and %s
                        order by fecha, hora_inicio""", (rama, desde, hasta))


def recientes_y_proximos(rama, dias_atras=14, dias_adelante=7):
    from datetime import timedelta
    h = fechas.hoy()
    return consultar("""select * from entrenamientos where rama = %s and estado = 'programado'
                        and fecha between %s and %s order by fecha desc, hora_inicio desc""",
                     (rama, h - timedelta(days=dias_atras), h + timedelta(days=dias_adelante)))

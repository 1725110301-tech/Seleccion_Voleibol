from mvc.models.comun.conexion import consultar, ejecutar


def listar():
    return consultar("select * from competencias order by fecha_inicio desc")


def crear(nombre, tipo, fecha_inicio, fecha_fin):
    """RF-08: registra liga o torneo."""
    errores = []
    if not (nombre or "").strip():
        errores.append("El nombre es obligatorio")
    if tipo not in ("liga", "torneo"):
        errores.append("El tipo debe ser liga o torneo")
    if not fecha_inicio or not fecha_fin:
        errores.append("Las fechas son obligatorias")
    elif fecha_fin < fecha_inicio:
        errores.append("La fecha de fin no puede ser menor a la de inicio")
    if errores:
        return False, errores
    ejecutar("insert into competencias (nombre, tipo, fecha_inicio, fecha_fin) values (%s,%s,%s,%s)",
             (nombre.strip(), tipo, fecha_inicio, fecha_fin))
    return True, ["Competencia guardada"]

def entero(valor, defecto=None):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return defecto


def registros_asistencia(f, jugadores):
    """Convierte el formulario del pase de lista en una lista de registros."""
    registros = []
    for j in jugadores:
        motivo = (f.get("motivo_%s" % j.id) or "").strip()
        registros.append({
            "jugador_id": j.id,
            "nombre": j.nombre,
            "estado": f.get("estado_%s" % j.id),
            "motivo": motivo or None,
        })
    return registros

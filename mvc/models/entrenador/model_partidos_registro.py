from mvc.models.comun.conexion import ejecutar


def crear(rama, rival, fecha, sets, resultado, competencia_id=None):
    """RF-07: guarda rival, fecha, marcadores por set y resultado final."""
    errores = []
    if not (rival or "").strip():
        errores.append("El rival es obligatorio")
    if not fecha:
        errores.append("La fecha es obligatoria")
    if not (sets or "").strip():
        errores.append("Captura los marcadores por set (ej. 25-20, 22-25, 25-18)")
    if resultado not in ("ganado", "perdido"):
        errores.append("El resultado debe ser ganado o perdido")
    if errores:
        return False, errores
    ejecutar("""insert into partidos (competencia_id, rama, rival, fecha, sets, resultado)
                values (%s,%s,%s,%s,%s,%s)""",
             (competencia_id or None, rama, rival.strip(), fecha, sets.strip(), resultado))
    return True, ["Partido guardado"]

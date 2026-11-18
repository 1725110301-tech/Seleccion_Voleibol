from mvc.models.comun.conexion import consultar, ejecutar

RAMAS = ("femenil", "varonil")
POSICIONES = ("colocador", "opuesto", "central", "receptor", "libero")


def listar(rama, solo_activos=False):
    sql = "select * from jugadores where rama = %s"
    if solo_activos:
        sql += " and estado = 'activo'"
    return consultar(sql + " order by estado, numero_playera", (rama,))


def obtener(jugador_id):
    return consultar("select * from jugadores where id = %s", (jugador_id,), uno=True)


def _entero(valor, minimo, maximo):
    try:
        n = int(valor)
        return n if minimo <= n <= maximo else None
    except (TypeError, ValueError):
        return None


def validar(d):
    """RF-02: campos obligatorios completos. Devuelve lista de errores."""
    errores = []
    for campo, etiqueta in [("nombre", "Nombre"), ("matricula", "Matrícula"), ("correo", "Correo"),
                            ("carrera", "Carrera"), ("rama", "Rama"), ("posicion", "Posición")]:
        if not (d.get(campo) or "").strip():
            errores.append("%s es obligatorio" % etiqueta)
    if d.get("rama") and d["rama"] not in RAMAS:
        errores.append("Rama inválida")
    if d.get("posicion") and d["posicion"] not in POSICIONES:
        errores.append("Posición inválida")
    if len((d.get("matricula") or "").strip()) > 10:
        errores.append("La matrícula debe tener máximo 10 caracteres")
    if _entero(d.get("edad"), 15, 60) is None:
        errores.append("Edad entre 15 y 60")
    if _entero(d.get("cuatrimestre"), 1, 11) is None:
        errores.append("Cuatrimestre entre 1 y 11")
    if _entero(d.get("numero_playera"), 0, 99) is None:
        errores.append("Número de playera entre 0 y 99")
    return errores


def crear(d):
    """RF-11: guarda como 'activo' verificando matrícula y número de playera por rama."""
    errores = validar(d)
    if errores:
        return False, errores
    if consultar("select 1 from jugadores where matricula = %s", (d["matricula"].strip(),), uno=True):
        return False, ["La matrícula ya está registrada"]
    if consultar("select 1 from jugadores where rama = %s and numero_playera = %s",
                 (d["rama"], int(d["numero_playera"])), uno=True):
        return False, ["El número de playera ya está en uso en esa rama"]
    ejecutar("""insert into jugadores (nombre, matricula, correo, telefono, edad, cuatrimestre,
                carrera, rama, posicion, numero_playera, estado)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'activo')""",
             (d["nombre"].strip(), d["matricula"].strip(), d["correo"].strip(),
              (d.get("telefono") or "").strip() or None, int(d["edad"]), int(d["cuatrimestre"]),
              d["carrera"].strip(), d["rama"], d["posicion"], int(d["numero_playera"])))
    return True, ["Jugador guardado correctamente"]


def cambiar_estado(jugador_id, estado):
    """RF-12: baja lógica / reactivar. No elimina el registro ni su historial."""
    if estado not in ("activo", "baja"):
        return False
    ejecutar("update jugadores set estado = %s where id = %s", (estado, jugador_id))
    return True

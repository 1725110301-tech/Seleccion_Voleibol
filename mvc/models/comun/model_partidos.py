from mvc.helpers import fechas
from mvc.models.comun.conexion import consultar


def listar(rama, desde=None, hasta=None):
    sql = """select p.*, c.nombre as competencia, c.tipo as tipo_competencia
             from partidos p left join competencias c on c.id = p.competencia_id where p.rama = %s"""
    params = [rama]
    if desde and hasta:
        sql += " and p.fecha between %s and %s"
        params += [desde, hasta]
    return consultar(sql + " order by p.fecha desc", params)


def proximos_liga(rama):
    return consultar("""select p.* from partidos p join competencias c on c.id = p.competencia_id
                        where p.rama = %s and c.tipo = 'liga' and p.fecha >= %s order by p.fecha""",
                     (rama, fechas.hoy()))


def obtener(partido_id):
    return consultar("""select p.*, c.tipo as tipo_competencia from partidos p
                        left join competencias c on c.id = p.competencia_id where p.id = %s""",
                     (partido_id,), uno=True)


def competencias(tipo=None):
    if tipo:
        return consultar("select * from competencias where tipo = %s order by fecha_inicio desc", (tipo,))
    return consultar("select * from competencias order by fecha_inicio desc")

from mvc.helpers import sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina
from mvc.models.comun import model_asistencias


class Jugadores:
    @requiere_rol("coordinacion")
    def GET(self):  # RF-06 (solo consulta)
        rama = sesion.rama()
        return pagina("coordinacion", "jugadores_lista", "Lista de jugadores",
                      model_asistencias.jugadores_con_asistencia(rama), rama)

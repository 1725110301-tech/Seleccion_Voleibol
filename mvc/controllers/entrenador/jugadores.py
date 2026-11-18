import web
from mvc.helpers import sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina
from mvc.models.comun import model_asistencias


class Jugadores:
    @requiere_rol("entrenador")
    def GET(self):
        # RF-06 (% asistencia) y RF-13 (posible baja)
        f = web.input(mensaje="")
        rama = sesion.rama()
        jugadores = model_asistencias.jugadores_con_asistencia(rama)
        return pagina("entrenador", "jugadores_lista", "Lista de jugadores", jugadores, rama, f.mensaje)

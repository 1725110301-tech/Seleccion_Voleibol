import web
from datetime import timedelta
from mvc.helpers import fechas, sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina
from mvc.models.comun import model_entrenamientos
from mvc.models.entrenador import model_entrenamientos_extra


class Entrenamientos:
    def _mostrar(self, error=None, mensaje=None):
        rama, h = sesion.rama(), fechas.hoy()
        lista = model_entrenamientos.listar(rama, h - timedelta(days=7), h + timedelta(days=21))
        return pagina("entrenador", "entrenamientos", "Entrenamientos", lista, rama, error, mensaje)

    @requiere_rol("entrenador")
    def GET(self):
        return self._mostrar()

    @requiere_rol("entrenador")
    def POST(self):  # RF-04
        f = web.input(fecha="", hora_inicio="", hora_fin="")
        ok, msg = model_entrenamientos_extra.crear_extra(sesion.rama(), f.fecha, f.hora_inicio, f.hora_fin)
        return self._mostrar(None if ok else msg, msg if ok else None)

import web
from mvc.helpers import fechas, sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina
from mvc.models.entrenador import model_reportes


class Reportes:
    @requiere_rol("entrenador")
    def GET(self):  # RF-10
        f = web.input(desde="", hasta="")
        desde, hasta = fechas.rango(f.desde, f.hasta)
        rama = sesion.rama()
        reporte = model_reportes.reporte_general(rama, desde, hasta)
        return pagina("entrenador", "reportes", "Reportes", reporte, desde, hasta, rama)

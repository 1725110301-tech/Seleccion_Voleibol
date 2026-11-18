import web
from mvc.helpers import fechas, sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.formularios import entero
from mvc.helpers.vistas import pagina
from mvc.models.comun import model_jugadores
from mvc.models.entrenador import model_reportes


class ReporteJugador:
    @requiere_rol("entrenador")
    def GET(self):  # RF-18
        f = web.input(jugador_id="", desde="", hasta="")
        desde, hasta = fechas.rango(f.desde, f.hasta)
        rama = sesion.rama()
        jid = entero(f.jugador_id)
        reporte = model_reportes.reporte_individual(jid, desde, hasta) if jid else None
        return pagina("entrenador", "reporte_jugador", "Reporte individual",
                      model_jugadores.listar(rama), jid, reporte, desde, hasta, rama)

import web
from mvc.helpers import sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.formularios import entero
from mvc.helpers.vistas import pagina
from mvc.models.comun import model_partidos
from mvc.models.entrenador import model_partidos_registro


class Partidos:
    def _mostrar(self, errores=(), mensaje=None):
        rama = sesion.rama()
        return pagina("entrenador", "partidos", "Partidos", model_partidos.listar(rama),
                      model_partidos.competencias(), rama, list(errores), mensaje)

    @requiere_rol("entrenador")
    def GET(self):
        return self._mostrar()

    @requiere_rol("entrenador")
    def POST(self):  # RF-07
        f = web.input(competencia_id="", rival="", fecha="", sets="", resultado="")
        ok, res = model_partidos_registro.crear(sesion.rama(), f.rival, f.fecha, f.sets, f.resultado,
                                                entero(f.competencia_id))
        return self._mostrar([] if ok else res, res[0] if ok else None)

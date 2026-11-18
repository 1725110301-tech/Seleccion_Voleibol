import web
from mvc.helpers import sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.formularios import entero
from mvc.helpers.vistas import pagina
from mvc.models.comun import model_jugadores, model_partidos
from mvc.models.entrenador import model_convocatorias


class Convocatorias:
    def _mostrar(self, competencia_id, error=None, mensaje=None):
        rama = sesion.rama()
        torneos = model_partidos.competencias("torneo")
        jugadores = model_jugadores.listar(rama, solo_activos=True) if competencia_id else []
        convocados = model_convocatorias.convocados(competencia_id, rama) if competencia_id else set()
        return pagina("entrenador", "convocatorias", "Convocatorias", torneos, competencia_id, jugadores,
                      convocados, rama, error, mensaje)

    @requiere_rol("entrenador")
    def GET(self):
        f = web.input(competencia_id="")
        return self._mostrar(entero(f.competencia_id))

    @requiere_rol("entrenador")
    def POST(self):  # RF-17
        f = web.input(competencia_id="", jugadores=[])
        cid = entero(f.competencia_id)
        ids = [entero(x) for x in (f.jugadores if isinstance(f.jugadores, list) else [f.jugadores])]
        ok, msg = model_convocatorias.guardar(cid, [i for i in ids if i], sesion.rama())
        return self._mostrar(cid, None if ok else msg, msg if ok else None)

import web
from mvc.helpers.auth import requiere_rol
from mvc.helpers.formularios import entero
from mvc.models.comun import model_jugadores


class CambiarEstado:
    """RF-12: Dar de baja / Reactivar (baja lógica, conserva historial)."""
    @requiere_rol("entrenador")
    def POST(self):
        f = web.input(id="", estado="")
        model_jugadores.cambiar_estado(entero(f.id), f.estado)
        raise web.seeother("/entrenador/jugadores")

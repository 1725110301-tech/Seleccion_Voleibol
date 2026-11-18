import web
from mvc.helpers import sesion


class CambiarRama:
    """RF-09: filtro Femenil / Varonil global (se guarda en la sesión)."""
    def GET(self):
        if not sesion.usuario():
            raise web.seeother("/login")
        f = web.input(rama="", volver="/dashboard")
        sesion.cambiar_rama(f.rama)
        destino = f.volver if f.volver.startswith("/") and not f.volver.startswith("//") else "/dashboard"
        raise web.seeother(destino)

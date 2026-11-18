import web
from mvc.helpers import sesion


class Dashboard:
    """Redirige al panel según el rol (RF-20)."""
    def GET(self):
        u = sesion.usuario()
        if not u:
            raise web.seeother("/login")
        raise web.seeother("/%s/dashboard" % u["rol"])

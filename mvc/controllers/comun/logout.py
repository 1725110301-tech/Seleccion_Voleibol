import web
from mvc.helpers import sesion


class Logout:
    """RF-20: invalida la sesión y regresa al login."""
    def GET(self):
        sesion.get().kill()
        raise web.seeother("/login")

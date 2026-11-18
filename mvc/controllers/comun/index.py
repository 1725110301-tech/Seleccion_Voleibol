import web
from mvc.helpers import sesion


class Index:
    def GET(self):
        raise web.seeother("/dashboard" if sesion.usuario() else "/login")

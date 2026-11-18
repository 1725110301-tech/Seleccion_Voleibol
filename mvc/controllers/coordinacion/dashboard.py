from mvc.helpers import sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina


class Dashboard:
    @requiere_rol("coordinacion")
    def GET(self):
        return pagina("coordinacion", "dashboard", "Inicio", sesion.usuario(), sesion.rama())

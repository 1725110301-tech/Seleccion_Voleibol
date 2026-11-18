import functools
import web
from mvc.helpers import sesion


def requiere_rol(*roles):
    """RBAC: sin sesión -> /login; con rol incorrecto -> a su propio panel."""
    def decorador(fn):
        @functools.wraps(fn)
        def envoltura(self, *args, **kwargs):
            u = sesion.usuario()
            if not u:
                raise web.seeother("/login")
            if u["rol"] not in roles:
                raise web.seeother("/dashboard")
            return fn(self, *args, **kwargs)
        return envoltura
    return decorador

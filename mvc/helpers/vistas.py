import web
from mvc.helpers import sesion
from mvc.helpers.menu import MENUS

_BASE = "mvc/views/"
_layout = web.template.render(_BASE + "layout")
_renders = {c: web.template.render(_BASE + c) for c in ("comun", "entrenador", "capitan", "coordinacion")}


def sin_layout(carpeta, vista, *args):
    """Renderiza una vista sola (login)."""
    return getattr(_renders[carpeta], vista)(*args)


def pagina(carpeta, vista, titulo, *args):
    """Renderiza la vista de un rol dentro de la plantilla maestra (menú lateral por rol)."""
    contenido = getattr(_renders[carpeta], vista)(*args)
    u = sesion.usuario()
    return _layout.template(contenido, titulo, MENUS.get(u["rol"], []), u, sesion.rama(), web.ctx.fullpath)

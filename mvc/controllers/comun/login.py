import web
import config
from mvc.helpers import sesion
from mvc.helpers.vistas import sin_layout
from mvc.models.comun import model_usuarios

MENSAJE = "Usuario o contraseña incorrectos, o el usuario está inactivo."


class Login:
    def GET(self):
        if sesion.usuario():
            raise web.seeother("/dashboard")
        return sin_layout("comun", "login", None, "")

    def POST(self):
        f = web.input(usuario="", contrasena="")
        u = model_usuarios.autenticar(f.usuario, f.contrasena)
        if not u:
            config.logger.warning("Login fallido: %s", f.usuario)
            return sin_layout("comun", "login", MENSAJE, f.usuario)
        sesion.get().usuario = u
        sesion.get().rama = "femenil"
        config.logger.info("Login: %s (%s)", u["usuario"], u["rol"])
        raise web.seeother("/%s/dashboard" % u["rol"])

import web
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina
from mvc.models.entrenador import model_competencias


class Competencias:
    def _mostrar(self, errores=(), mensaje=None):
        return pagina("entrenador", "competencias", "Ligas y torneos", model_competencias.listar(),
                      list(errores), mensaje)

    @requiere_rol("entrenador")
    def GET(self):
        return self._mostrar()

    @requiere_rol("entrenador")
    def POST(self):  # RF-08
        f = web.input(nombre="", tipo="", fecha_inicio="", fecha_fin="")
        ok, res = model_competencias.crear(f.nombre, f.tipo, f.fecha_inicio, f.fecha_fin)
        return self._mostrar([] if ok else res, res[0] if ok else None)

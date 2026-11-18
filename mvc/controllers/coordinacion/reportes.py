import web
from mvc.helpers import pdf, sesion
from mvc.helpers.auth import requiere_rol
from mvc.helpers.vistas import pagina
from mvc.models.coordinacion import model_reportes_coord


class Reportes:
    @requiere_rol("coordinacion")
    def GET(self):  # RF-19
        f = web.input(rama="", pdf="")
        sesion.cambiar_rama(f.rama)
        rama = sesion.rama()
        datos = model_reportes_coord.consulta_rama(rama)
        if f.pdf:
            secciones = [
                ("Jugadores activos - %s" % rama, ["#", "Nombre", "Posicion", "Carrera"],
                 [(j.numero_playera, j.nombre, j.posicion, j.carrera) for j in datos["jugadores"]]),
                ("Resultados (ganados: %s, perdidos: %s)" % (datos["ganados"], datos["perdidos"]),
                 ["Fecha", "Rival", "Competencia", "Sets", "Resultado"],
                 [(p.fecha, p.rival, p.competencia or "-", p.sets or "-", p.resultado or "-")
                  for p in datos["partidos"]]),
            ]
            web.header("Content-Type", "application/pdf")
            web.header("Content-Disposition", "attachment; filename=reporte_%s.pdf" % rama)
            return pdf.generar("Reporte de coordinacion deportiva", secciones)
        return pagina("coordinacion", "reportes", "Reportes", datos, rama)

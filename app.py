import web
import config
from mvc.tareas import scheduler

C = "mvc.controllers."
RUTAS = [
    # comunes
    ("/", "comun.index.Index"),
    ("/login", "comun.login.Login"),
    ("/logout", "comun.logout.Logout"),
    ("/dashboard", "comun.dashboard.Dashboard"),
    ("/rama", "comun.cambiar_rama.CambiarRama"),
    # entrenador
    ("/entrenador/dashboard", "entrenador.dashboard.Dashboard"),
    ("/entrenador/jugadores", "entrenador.jugadores.Jugadores"),
    ("/entrenador/jugadores/nuevo", "entrenador.insertar_jugador.InsertarJugador"),
    ("/entrenador/jugadores/estado", "entrenador.cambiar_estado.CambiarEstado"),
    ("/entrenador/asistencia/lista", "entrenador.pase_lista.PaseLista"),
    ("/entrenador/asistencia/historial", "entrenador.historial_asistencias.HistorialAsistencias"),
    ("/entrenador/entrenamientos", "entrenador.entrenamientos.Entrenamientos"),
    ("/entrenador/competencias", "entrenador.competencias.Competencias"),
    ("/entrenador/partidos", "entrenador.partidos.Partidos"),
    ("/entrenador/convocatorias", "entrenador.convocatorias.Convocatorias"),
    ("/entrenador/reportes", "entrenador.reportes.Reportes"),
    ("/entrenador/reportes/jugador", "entrenador.reporte_jugador.ReporteJugador"),
    # capitán
    ("/capitan/dashboard", "capitan.dashboard.Dashboard"),
    ("/capitan/jugadores", "capitan.jugadores.Jugadores"),
    ("/capitan/jugadores/nuevo", "capitan.insertar_jugador.InsertarJugador"),
    ("/capitan/asistencia/lista", "capitan.pase_lista.PaseLista"),
    ("/capitan/asistencia/historial", "capitan.historial_asistencias.HistorialAsistencias"),
    ("/capitan/disponibilidad", "capitan.disponibilidad.Disponibilidad"),
    # coordinación deportiva
    ("/coordinacion/dashboard", "coordinacion.dashboard.Dashboard"),
    ("/coordinacion/jugadores", "coordinacion.jugadores.Jugadores"),
    ("/coordinacion/reportes", "coordinacion.reportes.Reportes"),
]
urls = tuple(x for ruta, clase in RUTAS for x in (ruta, C + clase))

app = web.application(urls, globals())

if web.config.get("_session") is None:
    web.config._session = web.session.Session(
        app, web.session.DiskStore("sessions"), initializer={"usuario": None, "rama": "femenil"})

application = app.wsgifunc()
scheduler.iniciar()  # RF-15

if __name__ == "__main__":
    app.run()

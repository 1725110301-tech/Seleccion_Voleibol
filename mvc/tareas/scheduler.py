import threading
import time
import config
from mvc.helpers import fechas

_iniciado = False
_ultimo_lunes = None


def _ciclo():
    global _ultimo_lunes
    from mvc.models.entrenador import model_entrenamientos_extra
    while True:
        try:
            hoy = fechas.hoy()
            if hoy.weekday() == 0 and _ultimo_lunes != hoy:  # lunes, 00:00 en adelante
                n = model_entrenamientos_extra.generar_semana(hoy)
                config.logger.info("RF-15: %s entrenamientos fijos creados", n)
                _ultimo_lunes = hoy
        except Exception:
            config.logger.exception("Error generando la semana")
        time.sleep(60)


def iniciar():
    global _iniciado
    if not _iniciado:
        _iniciado = True
        threading.Thread(target=_ciclo, daemon=True).start()

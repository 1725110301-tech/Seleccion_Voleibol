from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import config


def ahora():
    return datetime.now(ZoneInfo(config.TZ_APP))


def hoy():
    return ahora().date()


def parsear(valor, defecto):
    try:
        return date.fromisoformat(valor) if valor else defecto
    except ValueError:
        return defecto


def rango(desde, hasta, dias=30):
    h = parsear(hasta, hoy())
    d = parsear(desde, h - timedelta(days=dias))
    return (d, h) if d <= h else (h, d)

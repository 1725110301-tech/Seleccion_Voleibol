from mvc.models.comun import model_jugadores, model_partidos


def consulta_rama(rama):
    """RF-19: jugadores activos y resultados de liga y torneos con totales."""
    partidos = model_partidos.listar(rama)
    return {
        "jugadores": model_jugadores.listar(rama, solo_activos=True),
        "partidos": partidos,
        "ganados": sum(1 for p in partidos if p.resultado == "ganado"),
        "perdidos": sum(1 for p in partidos if p.resultado == "perdido"),
    }

import web


def get():
    return web.config._session


def usuario():
    return get().get("usuario")


def rama():
    return get().get("rama", "femenil")


def cambiar_rama(valor):
    if valor in ("femenil", "varonil"):
        get().rama = valor

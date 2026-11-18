import psycopg2
import psycopg2.extras
import web
from config import DATABASE_URL


def conectar():
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)


def consultar(sql, params=(), uno=False):
    con = conectar()
    try:
        with con.cursor() as cur:
            cur.execute(sql, params)
            if uno:
                fila = cur.fetchone()
                return web.storage(fila) if fila else None
            return [web.storage(f) for f in cur.fetchall()]
    finally:
        con.close()


def ejecutar(sql, params=(), retornar=False):
    con = conectar()
    try:
        with con:
            with con.cursor() as cur:
                cur.execute(sql, params)
                if retornar:
                    return web.storage(cur.fetchone())
    finally:
        con.close()

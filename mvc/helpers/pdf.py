from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generar(titulo, secciones):
    """secciones = [(subtitulo, [encabezados], [filas])] -> bytes de un PDF simple."""
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    ancho, alto = letter
    y = alto - 50

    def linea(texto, tam=10, salto=15):
        nonlocal y
        if y < 50:
            c.showPage()
            y = alto - 50
        c.setFont("Helvetica", tam)
        c.drawString(40, y, str(texto)[:110])
        y -= salto

    linea(titulo, 16, 28)
    for sub, cols, filas in secciones:
        linea(sub, 12, 20)
        linea(" | ".join(cols), 9)
        for fila in filas:
            linea(" | ".join(str(x) for x in fila), 9)
        y -= 10
    c.save()
    return buf.getvalue()

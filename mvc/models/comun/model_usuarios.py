import hmac
import bcrypt
from mvc.models.comun.conexion import consultar


def _verificar(password, guardada):
    if guardada.startswith("$2"):
        return bcrypt.checkpw(password.encode(), guardada.encode())
    return hmac.compare_digest(password, guardada)  # seed en texto plano (solo desarrollo)


def autenticar(usuario, password):
    """RF-01 / RF-06: devuelve el usuario si existe, está activo y la contraseña coincide."""
    u = consultar(
        "select id, nombre, usuario, contrasena, rol from usuarios where usuario = %s and activo = true",
        (usuario.strip(),), uno=True)
    if u and _verificar(password, u.contrasena):
        return {"id": u.id, "nombre": u.nombre, "usuario": u.usuario, "rol": u.rol}
    return None

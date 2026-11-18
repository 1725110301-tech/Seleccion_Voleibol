"""Uso: python scripts/hash_password.py MiContraseña  -> imprime el hash bcrypt para guardarlo en usuarios.contrasena"""
import sys, bcrypt
print(bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt()).decode())

"""Genera los entrenamientos fijos de la semana actual (RF-15). Útil para cron."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mvc.models.entrenador import model_entrenamientos_extra as m

if __name__ == "__main__":
    print("Entrenamientos creados:", m.generar_semana())

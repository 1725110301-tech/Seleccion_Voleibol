# Sistema de Gestión · Selección de Voleibol UTEC

Control de jugadores, entrenamientos, asistencias, partidos y reportes (rama femenil y varonil).
Stack: Python 3.11 + web.py (MVC), PostgreSQL / Supabase, HTML/CSS/JS.

## Arrancar
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                              # y poner DATABASE_URL de Supabase
# ejecutar sql/schema.sql y sql/seed.sql en Supabase
python app.py                                     # http://localhost:8080
```
Despliegue en Render: Build `pip install -r requirements.txt`, Start `gunicorn app:application`.

## Organización por rol
Cada capa (models / controllers / views) tiene una carpeta por tipo de usuario:

| Carpeta | Quién la usa | Requerimientos |
|---|---|---|
| `comun/` | Todos | RF-01, RF-06 (consulta), RF-09, RF-20 |
| `entrenador/` | Entrenador | RF-02, 04, 05, 07, 08, 10, 11, 12, 15, 17, 18 (+ lectura de RF-03, 06, 13, 14) |
| `capitan/` | Capitán | RF-02, 03, 05, 11, 14, 16 (+ RF-06, 13) |
| `coordinacion/` | Coordinación deportiva | RF-06 (consulta), RF-19 |

Notas de diseño:
- Lo compartido (jugadores, asistencias, entrenamientos, partidos de lectura) vive en `models/comun/`.
- Cada controlador valida con `@requiere_rol(...)` (RBAC, RF-20).
- RF-15: `mvc/tareas/scheduler.py` crea los 4 entrenamientos fijos cada lunes (idempotente). También: `python scripts/generar_semana.py` para cron.
- "Entrenamientos realizados" (RF-06) = programados con fecha <= hoy; el % cuenta solo "presente".
- Las contraseñas del seed están en texto plano; `model_usuarios` acepta bcrypt ($2b$...) o texto plano. **Hashear antes de producción** (`python scripts/hash_password.py`).

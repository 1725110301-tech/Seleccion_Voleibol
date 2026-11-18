import logging
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
TZ_APP = os.getenv("TZ_APP", "America/Mexico_City")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("aplicacion.log", encoding="utf-8"), logging.StreamHandler()],
)
logger = logging.getLogger("voleibol")

import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Lese die Umgebungsvariablen
TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

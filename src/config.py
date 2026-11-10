"""Configuration centralisée.

Les valeurs viennent des variables d'environnement ; à défaut, du fichier .env à la
racine du projet (lu ici sans dépendance), pour que les notebooks lancés dans VS Code
fonctionnent sans réglage supplémentaire.
"""
import os
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]


def _charger_dotenv() -> None:
    fichier = RACINE / ".env"
    if not fichier.exists():
        return
    for ligne in fichier.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, valeur = ligne.split("=", 1)
        os.environ.setdefault(cle.strip(), valeur.strip())


_charger_dotenv()

# --- Data lake (RustFS, API S3) ---
RUSTFS_ENDPOINT = os.getenv("RUSTFS_ENDPOINT", "http://localhost:9000")
RUSTFS_ACCESS_KEY = os.getenv("RUSTFS_ACCESS_KEY", "rustfsadmin")
RUSTFS_SECRET_KEY = os.getenv("RUSTFS_SECRET_KEY", "rustfsadmin")
LAKE_BUCKET = os.getenv("LAKE_BUCKET", "velib")

BRONZE_PATH = f"s3a://{LAKE_BUCKET}/bronze"
SILVER_PATH = f"s3a://{LAKE_BUCKET}/silver"
GOLD_PATH = f"s3a://{LAKE_BUCKET}/gold"

# --- PostgreSQL (gold) ---
PG_HOST = os.getenv("POSTGRES_HOST", "localhost")
PG_PORT = os.getenv("POSTGRES_PORT", "5432")
PG_DB = os.getenv("POSTGRES_DB", "velib_gold")
PG_USER = os.getenv("POSTGRES_USER", "velib")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD", "velib")
PG_JDBC_URL = f"jdbc:postgresql://{PG_HOST}:{PG_PORT}/{PG_DB}"
PG_SQLALCHEMY_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# --- Données locales (collectées par src/collecter_velib.py) ---
_data = Path(os.getenv("DATA_DIR", "data"))
DATA_DIR = _data if _data.is_absolute() else RACINE / _data

"""Configuration centralisée (lue depuis les variables d'environnement / .env)."""
import os

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

# --- Données locales (téléchargées par scripts/telecharger_donnees.sh) ---
DATA_DIR = os.getenv("DATA_DIR", "/home/jovyan/work/data")

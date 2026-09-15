import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "flights.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"


import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "flights.db"
SCHEMA_PATH = BASE_DIR /"db" / "schema.sql"

# users: (username, password, role).
users = [
    ("guest_user", "guest_1234", "guest"),
    ("admin_user", "admin_1234", "admin")
]

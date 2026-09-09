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

def seed_users():
    """
    Creates the users table (if it does not already exist) 
    and inserts the test accounts defined in users, 
    hashing each password before storing it.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read()) # ensures both tables (flights, users) exist

    for username, plain_password, role in users:
        password_hash = generate_password_hash(plain_password)
        cursor.execute(
            "Insert or Ignore into users (username, password_hash, role) values (?, ?, ?)",
            (username, password_hash, role)
        )

    conn.commit()
    conn.close()
    print("Test user created: guest_user / admin_user")


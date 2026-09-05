from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
DB_PATH = BASE_DIR / "data" /  "flights.db" # where the SQLite database file will be created
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql" # the SQL file defining the flights table structure

# list of fictional flights to insert

flights = [
    ("SK101", "Airbus A330", "JFK", "TLV", "2026-09-09 17:30", "2026-09-10 10:50", 620, "B12", "ON TIME"),
    ("SK204", "Airbus A220-100", "FCO", "LCY", "2026-09-10 09:15", "2026-09-10 11:00", 165, "A4", "BOARDING"),
    ("SK315", "Airbus A320", "AMS", "CDG", "2026-09-10 10:00", "2026-09-10 11:20", 80, "C7", "DELAYED"),
    ("SK427", "Airbus A319", "BUD", "VCE", "2026-09-10 07:45", "2026-09-10 09:00", 75, "D2", "ON TIME"),
    ("SK588", "Boeing 737", "MAD", "LIS", "2026-09-10 12:00", "2026-09-10 12:10", 70, "B8", "ON TIME"),
    ("SK612", "Airbus A321", "MUC", "BCN", "2026-09-10 14:20", "2026-09-10 16:00", 100, "A1", "DELAYED"),
    ("SK733", "Boeing 737", "CDG", "ATH", "2026-09-10 06:50", "2026-09-10 10:10", 200, "C3", "DEPARTED"),
    ("SK849", "Airbus A320", "FRA", "CPH", "2026-09-10 16:30", "2026-09-10 18:00", 90, "B5", "ON TIME"),
    ("SK901", "Airbus A320", "ORY", "MXP", "2026-09-10 18:00", "2026-09-10 19:15", 75, "D9", "ON TIME"),
    ("SK1024", "Airbus A319", "VIE", "WAW", "2026-09-10 20:10", "2026-09-10 21:30", 80, "A6", "LANDED"),

]

def seed_database():
    # sqlite3.connect() opens a connection to the database file.
    # If the file specified by DB_PATH doesn't exist yet, SQLite creates it automatically here.
    conn = sqlite3.connect(DB_PATH)  # creates the .db file if it doesn't exist yet

    cursor = conn.cursor() # A cursor is the object used to actually send SQL commands and read results.

    # Open and read the schema.sql file, then execute it.
    # executescript() (instead of execute()) allows running multiple SQL statements at once,
    # which schema.sql could contain in the future (e.g. more than one CREATE TABLE).

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())  # run the CREATE TABLE statement from schema.sql


    # Insert all fictional flights in a single batch operation.
    # "INSERT OR IGNORE" means: if a flight_number already exists (UNIQUE constraint in schema.sql),
    # silently skip that row instead of raising an error. This makes the script safe to re-run
    # multiple times without creating duplicates or crashing.
    cursor.executemany(
        """
        INSERT OR IGNORE INTO flights
        (flight_number, aircraft_type, origin, destination, departure_time, arrival_time, duration_minutes, gate, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        flights
    )

    conn.commit() # commit() saves all the changes (table creation + inserted rows) permanently to the .db file
    conn.close()  # close the connection, freeing the database file so other processes can access it
    print(f"Database created and seeded at: {DB_PATH}")


# This is a standard Python convention.
# __name__ is a special variable: Python sets it to "__main__" only when this file
# If this file were instead imported from another script (e.g. "from db.seed_flights import seed_database"),
# __name__ would be "seed_flights" instead, and the code below would NOT run automatically.
# This lets us reuse seed_database() elsewhere later (e.g. to reset the database from the Flask app)
# without accidentally re-seeding the database every time this file is imported.

if __name__ == "__main__":
    seed_database()
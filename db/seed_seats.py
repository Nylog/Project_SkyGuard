import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "flights.db"
SCHEMA_PATH = BASE_DIR / "db" / "schema.sql"


def row_position (row, total_row) :
    """
    Determine the aircraft section (front, middle, or rear) based on the row number.

    """
    third = total_row / 3
    if row <= third :    # Check if the row belongs to the first third (front)
        return "front" 
    elif row <= (third * 2) :   # Check if the row belongs to the second third (middle)
        return "middle"

    return "rear"





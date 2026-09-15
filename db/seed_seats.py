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



def generate_narrow_body():
    """
    Generate a standard list of seats for a narrow-body aircraft.
    """

    # Single aisle, 3-3 layout: A B C | aisle | D E F
    columns = {
        "A" : "window", "B" : "middle", "C" : "aisle",
        "D" : "aisle", "E" : "middle", "F" : "window"
        }

    total_row = 30
    seats = []

    for row in range(1, total_row + 1) :
        for col, position in columns.items():
            seats.append(("narrow_body", f"{row}{col}",
                          position,
                          row_position(row, total_row),
                          1, # has usb
                          1 if row <= 10 else 0,  # has power outlet: front rows only
                          0,  # has_tv: none on narrow-body 
                          ))

    return seats



def generate_wide_body():
    """
        Generate a standard list of seats for a wide-body aircraft.
        """

    # Double aisle, 2-4-2 layout: A B | aisle | C D E F | aisle | G H
    columns = {
        "A" : "window", "B" : "aisle",
        "C" : "aisle", "D" : "middle", "E" : "middle", "F" : "aisle",
        "G" : "aisle", "H" : "window"
    }

    total_row = 35
    seats = []

    for row in range(1, total_row +1):
        for col, position in columns.items():
            seats.append(("wide_body", f"{row}{col}",
                          position,
                          row_position(row, total_row),
                          1, # has usb
                          1, # has power outlet
                          1, # has tv
                          ))
    return seats


def seed_seats():
    """
    Initialize the database schema and populate the seats table.
    """
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r") as f:
        cursor.executescript(f.read())

    all_seats = generate_narrow_body() + generate_wide_body()

    cursor.executemany(
        """
        INSERT OR IGNORE INTO seats
        (category, seat_number, position, row_position, has_usb, has_power_outlet, has_tv)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        all_seats
    )

    conn.commit()
    conn.close()

    print(f"seat map generated: {len(all_seats)} seats total")



if __name__ == "__main__":
    seed_seats()
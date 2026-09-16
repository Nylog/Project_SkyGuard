"""
db_utils.py 

Utility functions to interact with the Skyguard flights database.
This file centralizes all the queries used to read and update flight data,
so that other parts of the project (mainly the agent and Flask backend)
can retrieve flight information without writing raw SQL themselves.

Functions provided:
    - get_connection() -> opens a connection to the database (flight.db)
    - get_flight_by_number() -> retrieves a single flight's details
    - get_flights_by_status() -> retrieves all flights matching a given status
    - update_flight_status() -> update flight status 
"""


from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "flights.db"

from datetime import datetime
import random


def get_connection():
    conn = sqlite3.connect(DB_PATH)   # open a connection to the database file
    conn.row_factory = sqlite3.Row    # make query results behave like dictionaries (access columns by name)
    return conn


def get_flight_by_number(flight_number):
    conn = get_connection()
    cursor = conn.cursor() # object used to send SQL commands
    cursor.execute("SELECT * FROM flights WHERE flight_number = ?", (flight_number,)) # "?" safely inserts the value, avoiding SQL injection
    row = cursor.fetchone() # get the first (and only, since flight_number is UNIQUE) matching row
    conn.close() 
    return dict(row) if row else None # convert to a plain dictionary, or None if no flight was found


def get_flights_by_status(status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flights WHERE status = ?", (status,))
    rows = cursor.fetchall()  # get ALL matching rows (not just the first one)
    conn.close() 
    return [dict(row) for row in rows] # convert every row to a dictionary, returned as a list


def update_flight_status(flight_number, new_status):
    # Updates the status of a specific flight (e.g. simulating a delay caused by a MAINTENANCE issue).
    # Returns True if a flight was actually updated, False if the flight_number didn't exist.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE flights SET status = ? WHERE flight_number = ?",
        (new_status, flight_number)
    )
    conn.commit() # save the change permanently to the database file
    updated = cursor.rowcount > 0 # rowcount tells us how many rows were actually changed
    conn.close()
    return updated # True if the flight existed and was updated, False otherwise


def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def generate_reference_number():
    # Generates a unique reference code for a baggage item.
    #  The code follows the format 'BAG-YYYY-NNNN', where YYYY is the current year and NNNN is a random 4-digit number.
    year = datetime.now().year
    random_digits = random.randint(1000, 9999)  # Small risk of collision within the same year. DB schema enforces UNIQUE.

    return f"BAG-{year}-{random_digits}"


def create_baggage_report(flight_number, description):
    # Creates a new baggage report in the database with a generated reference number.
    reference_number = generate_reference_number()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO baggage_reports (reference_number, flight_number, description) VALUES (?, ?, ?)",
                   (reference_number, flight_number, description)
                   )
    conn.commit()
    conn.close()

    return reference_number


def get_baggage_report(reference_number):
    # Retrieves a baggage report from the database by its unique reference number.

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM baggage_reports WHERE reference_number =?", (reference_number,))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None



def get_seat_info(category, seat_number):
    # Retrieves information for a specific seat based on its category and number.

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM seats WHERE category = ? AND seat_number = ?", (category, seat_number))
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None



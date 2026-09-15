CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL UNIQUE,
    airline TEXT NOT NULL DEFAULT 'Celestial Line',
    aircraft_type TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    gate TEXT,
    status TEXT NOT NULL DEFAULT 'ON TIME'
        CHECK (status IN ('ON TIME', 'DELAYED', 'BOARDING', 'DEPARTED', 'LANDED', 'CANCELLED'))
);


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'guest'
        CHECK (role IN ('guest', 'admin'))
);


CREATE TABLE IF NOT EXISTS baggage_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_number TEXT NOT NULL UNIQUE,
    flight_number TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'REPORTED'
        CHECK (status IN ('REPORTED', 'IN PROGRESS', 'FOUND', 'CLOSED')),
    FOREIGN KEY (flight_number) REFERENCES flights(flight_number)
);

CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL CHECK (category IN ('narrow_body', 'wide_body')),
    seat_number TEXT NOT NULL,
    position TEXT NOT NULL CHECK (position in ('window', 'middle', 'aisle')),
    row_position TEXT NOT NULL CHECK (row_position in ('front', 'middle', 'rear')),
    has_usb INTEGER NOT NULL,
    has_power_outlet INTEGER NOT NULL,
    has_tv INTEGER NOT NULL,
    UNIQUE (category, seat_number)
);

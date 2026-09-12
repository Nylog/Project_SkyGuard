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
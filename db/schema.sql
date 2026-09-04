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
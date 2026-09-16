"""
Combines flight data (from the SQLite database) and weather data (from Open-Meteo)
that the SkyGuard agent can call to answer operational
queries about a specific flight.
"""

import sys # provides access to Python's import system, including the list of folders it searches for modules
from pathlib import Path


# By default, Python only looks for modules in a few standard locations
# Since this script may be executed from inside agent/ rather than the project root,
# we manually add the project root to sys.path (the list of folders Python searches when importing),
# so that "from db..." and "from agent..." resolve correctly regardless of the current working directory.

sys.path.append(str(Path(__file__).resolve().parent.parent)) 

from db.db_utils import get_flight_by_number, create_baggage_report, get_baggage_report, get_seat_info
from agent.weather import get_weather, interpret_departure_weather, get_destination_weather_info, Airport_cities

from math import radians, sin, cos, sqrt, atan2
from agent.weather import Airports_coordinates

from  data.aircraft_category import aircraft_category

def get_flight_status(flight_number):
    """
    Retrieves full flight info from the database, plus current weather
    conditions at both departure and destination airports.
    Returns None if the flight number doesn't exist in the database.
    """
    flight = get_flight_by_number(flight_number)

    if flight is None:
        return None

    departure_weather = get_weather(flight["origin"])
    destination_weather = get_weather(flight["destination"])


    # Build the base result using the flight's data from the database.
    result = {
    "flight_number" : flight["flight_number"],
    "airline" : flight["airline"],
    "aircraft_type" : flight["aircraft_type"],
    "origin" : flight["origin"],
    "destination" : flight["destination"],
    "departure_time" : flight["departure_time"],
    "arrival_time" : flight["arrival_time"],
    "status" : flight["status"],
    "gate" : flight["gate"]
    }

    result["origin_city"] = Airport_cities.get(flight["origin"], flight["origin"])
    result["destination_city"] = Airport_cities.get(flight["destination"], flight["destination"])

    # Weather data might be unavailable if the airport code isn't in our coordinates map,
    # so we check before trying to interpret it.

    if departure_weather is not None:
        result["departure_weather"] = interpret_departure_weather(departure_weather)
    else:
        result["departure_weather"] = {"condition" : "unavailable", "delay_notes" : "Weather data unavailable"}


    if destination_weather is not None:
        result["destination_weather"] = get_destination_weather_info(destination_weather)
    else:
        result["destination_weather"] = {"condition" : "unavailable", "info_notes" : "Weather data unavailable"}

    return result # a single dictionary combining flight status and weather at both airports


def report_lost_baggage(flight_number, description):
    """
    Registers a lost baggage report and returns a user-facing success confirmation
    """

    reference_number = create_baggage_report(flight_number, description)

    return {"reference_number" : reference_number,
            "message" : f"Your baggage report has been registred with reference number {reference_number}"}



def check_baggage_status(reference_number):

    report =get_baggage_report(reference_number)

    if report is None:
        return {"error" : f"No baggage report found with reference number {reference_number}"}

    return report


def calculate_distance_km(origin_code, destination_code):
    """
    Calculates the great-circle distance (in km) between two airports,
    using their coordinates and the Haversine formula.
    """

    lat_1, lon_1 = Airports_coordinates[origin_code]
    lat_2, lon_2 = Airports_coordinates[destination_code]

    R = 6371   # Earth's radius in km (from wikipedia)

    lat_1, lon_1, lat_2, lon_2 = map(radians, [lat_1, lon_1, lat_2, lon_2])
    d_lat = lat_2 - lat_1
    d_lon = lon_2 - lon_1

    # 'a' is the square of the half-chord length between the two points
    a = sin(d_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(d_lon / 2) ** 2

    # 'c' is the central angle between the points, expressed in radians
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def calculate_fuel_load(flight_number, passengers):
    """
    Calculates estimated fuel load (in liters) for a flight, based on
    distance between origin and destination, and number of passengers.

    Formula: (distance_km * 0.5) + (passengers * 20)
    """

    flight = get_flight_by_number(flight_number)

    if flight is None:
        return {"error" : f"No flight found with number {flight_number}"}

    distance_km = calculate_distance_km(flight["origin"], flight["destination"])

    fuel_liters = (distance_km  * 0.5) + (passengers * 20)

    return {
        "flight_number" : flight_number,
        "distance_km" : round(distance_km, 1),
        "passengers" : passengers,
        "fuel_liters" : round(fuel_liters, 1)
    }



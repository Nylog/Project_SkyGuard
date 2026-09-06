import sys # provides access to Python's import system, including the list of folders it searches for modules
from pathlib import Path


# By default, Python only looks for modules in a few standard locations
# Since this script may be executed from inside agent/ rather than the project root,
# we manually add the project root to sys.path (the list of folders Python searches when importing),
# so that "from db..." and "from agent..." resolve correctly regardless of the current working directory.

sys.path.append(str(Path(__file__).resolve().parent.parent)) 

from db.db_utils import get_flight_by_number
from agent.weather import get_weather, interpret_departure_weather, get_destination_weather_info

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

    # Weather data might be unavailable if the airport code isn't in our coordinates map,
    # so we check before trying to interpret it.

    if departure_weather is not None:
        result["departure_weather"] = interpret_departure_weather(departure_weather)
    else:
        result["departure_weather"] = {"condition" : "unavaible", "delay_notes" : "Weather data unavaible"}


    if destination_weather is not None:
        result["destination_weather"] = get_destination_weather_info(destination_weather)
    else:
        result["destination_weather"] = {"condition" : "unavaible", "delay_notes" : "Weather data unavaible"}

    return result # a single dictionary combining flight status and weather at both airports


from db.db_utils import get_flight_by_number
from agent.weather import get_weather, interpret_departure_weather, get_destination_weather_info

def get_flight_status(flight_number):
    flight = get_flight_by_number(flight_number)

    if flight is None:
        return None

    departure_weather = get_weather(flight["origin"])
    destination_weather = get_weather(flight["destination"])

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

    return result

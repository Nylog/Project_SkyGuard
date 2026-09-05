import requests

Airports_coordinates= {
    "JFK" : (40.6413, -73.7781),
    "TLV" : (32.0004, 34.8706),
    "FCO" : (41.8003, 12.2389),
    "LCY" : (51.5053, 0.0553),
    "AMS" : (52.3105, 4.7683),
    "CDG" : (49.0097, 2.5479),
    "BUD" : (47.4369, 19.2556),
    "VCE" : (45.5053, 12.3519),
    "MAD" : (40.4983, -3.5676),
    "LIS" : (38.7813, -9.1359),
    "MUC" : (48.3538, 11.7861),
    "BNC" : (41.2974, 2.0833),
    "ATH" : (37.9364, 23.9445),
    "FRA" : (50.0379, 8.5622),
    "CPH" : (55.6180, 12.6560),
    "ORY" : (48.7233, 2.3794),
    "MXP" : (45.6301, 8.7255),
    "VIE" : (48.1103, 16.5697),
    "WAW" : (52.1657, 20.9671)
}

def get_weather(airport_code):    
    if airport_code not in Airports_coordinates:
        return None

    lat, lon = Airports_coordinates[airport_code]

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,weathercode,windspeed_10m",
        },
        timeout=5,
    )
    response.raise_for_status()  # raises an error if the request failed
    data = response.json()
    return data["current"]


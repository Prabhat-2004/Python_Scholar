
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Heavy drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Heavy rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail"
}


def get_data(url, params):
    full_url = url + "?" + urlencode(params)

    with urlopen(full_url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather(city):
    # Step 1: Find the city
    location_data = get_data(
        GEO_URL,
        {
            "name": city,
            "count": 5,
            "language": "en",
            "format": "json"
        }
    )

    places = location_data.get("results", [])

    if not places:
        print("City not found. Please try another city.")
        return

    # Use the first matching city
    place = places[0]

    latitude = place["latitude"]
    longitude = place["longitude"]

    # Step 2: Get current weather
    weather_data = get_data(
        WEATHER_URL,
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,weather_code,"
                "wind_speed_10m,precipitation"
            ),
            "timezone": "auto"
        }
    )

    current = weather_data["current"]

    code = current["weather_code"]
    condition = weather_codes.get(code, "Unknown condition")

    # Step 3: Display report
    print("\n" + "=" * 35)
    print("        WEATHER REPORT")
    print("=" * 35)

    print("City          :", place["name"])
    print("Country       :", place.get("country", "N/A"))
    print("Local time    :", current["time"])
    print("Condition     :", condition)
    print("Temperature   :", current["temperature_2m"], "°C")
    print("Feels like    :", current["apparent_temperature"], "°C")
    print("Humidity      :", current["relative_humidity_2m"], "%")
    print("Wind speed    :", current["wind_speed_10m"], "km/h")
    print("Precipitation :", current["precipitation"], "mm")

    print("=" * 35)


while True:
    city = input("\nEnter city name (or q to quit): ").strip()

    if city.lower() in ("q", "quit", "exit"):
        print("Thank you!")
        break

    if not city:
        print("Please enter a city name.")
        continue

    try:
        get_weather(city)

    except HTTPError as error:
        print("API error:", error.code)

    except URLError:
        print("Internet connection problem. Please try again.")

    except (KeyError, ValueError, TimeoutError) as error:
        print("Could not get weather data:", error)

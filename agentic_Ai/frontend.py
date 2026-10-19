
from flask import Flask, request, render_template_string
from urllib.request import urlopen
from urllib.parse import urlencode
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = ""
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            url = "https://geocoding-api.open-meteo.com/v1/search?"
            params = urlencode({"name": city, "count": 1})
            
            with urlopen(url + params, timeout=15) as response:
                places = json.loads(response.read()).get("results", [])

            if not places:
                error = "City not found!"
            else:
                place = places[0]

                url = "https://api.open-meteo.com/v1/forecast?"
                params = urlencode({
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                    "timezone": "auto"
                })

                with urlopen(url + params, timeout=15) as response:
                    current = json.loads(response.read())["current"]

                codes = {
                    0: "Clear Sky", 1: "Mainly Clear",
                    2: "Partly Cloudy", 3: "Overcast",
                    45: "Fog", 48: "Fog",
                    51: "Light Drizzle", 53: "Drizzle",
                    55: "Heavy Drizzle", 61: "Light Rain",
                    63: "Moderate Rain", 65: "Heavy Rain",
                    71: "Light Snow", 73: "Snow",
                    80: "Rain Showers", 81: "Rain Showers",
                    82: "Heavy Rain Showers", 95: "Thunderstorm"
                }

                weather = {
                    "city": place["name"] + ", " + place.get("country", ""),
                    "temp": current["temperature_2m"],
                    "feels": current["apparent_temperature"],
                    "humidity": current["relative_humidity_2m"],
                    "wind": current["wind_speed_10m"],
                    "condition": codes.get(current["weather_code"], "Unknown"),
                    "time": current["time"]
                }

        except Exception:
            error = "Unable to get weather. Check your internet connection."

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather App</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { box-sizing: border-box; }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #60a5fa, #a78bfa);
                min-height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .card {
                background: white;
                padding: 28px;
                border-radius: 20px;
                width: 100%;
                max-width: 400px;
                text-align: center;
                box-shadow: 0 10px 30px #0002;
            }
            h1 { color: #2563eb; }
            input, button {
                width: 100%;
                padding: 13px;
                margin: 7px 0;
                border-radius: 9px;
                font-size: 16px;
            }
            input { border: 1px solid #ccc; }
            button {
                background: #2563eb;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover { background: #1d4ed8; }
            .report {
                margin-top: 20px;
                padding: 15px;
                background: #eff6ff;
                border-radius: 12px;
            }
            .temp {
                color: #2563eb;
                font-size: 45px;
                font-weight: bold;
            }
            .detail {
                padding: 9px;
                margin: 6px 0;
                background: white;
                border-radius: 7px;
            }
            .error { color: red; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌤️ Weather App</h1>
            <p>Enter a city to check its weather</p>

            <form method="POST">
                <input name="city" placeholder="Enter city name"
                       value="{{ city }}" required>
                <button type="submit">Get Weather</button>
            </form>

            {% if weather %}
            <div class="report">
                <h2>{{ weather.city }}</h2>
                <div class="temp">{{ weather.temp }}°C</div>
                <h3>{{ weather.condition }}</h3>
                <div class="detail">🌡️ Feels like: {{ weather.feels }}°C</div>
                <div class="detail">💧 Humidity: {{ weather.humidity }}%</div>
                <div class="detail">💨 Wind: {{ weather.wind }} km/h</div>
                <div class="detail">🕒 Local time: {{ weather.time }}</div>
            </div>
            {% endif %}

            {% if error %}
            <p class="error">{{ error }}</p>
            {% endif %}
        </div>
    </body>
    </html>
    """, city=city, weather=weather, error=error)


if __name__ == "__main__":
    app.run(debug=True)


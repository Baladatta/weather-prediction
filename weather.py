
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import requests
import os

# 🔑 Replace with your actual API key from OpenWeather
API_KEY = "dc014b4e0e4ac5a5e4e1c5e05c1e7754"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__, static_folder="static")

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "wind_speed": data["wind"]["speed"]
        }
    else:
        try:
            error_data = response.json()
            error_message = error_data.get('message', 'Unknown error')
        except Exception:
            error_message = response.text
        return {"error": f"Error fetching data: {error_message}"}

@app.route("/")
def home():
    # Redirect to the HTML page in static folder
    return redirect(url_for('static', filename='/index.html'))

@app.route("/weather")
def weather_api():
    city = request.args.get("city", "")
    if not city:
        return jsonify({"error": "City name is required."})
    result = fetch_weather(city)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

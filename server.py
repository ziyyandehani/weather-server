import os
from flask import Flask, jsonify
import requests
import schedule, time, threading

server = Flask(__name__)

latest_weather = {}

def fetch_weather():
    global latest_weather
    api_key = os.environ.get("OWM_API_KEY")
    city = "Malang"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    r = requests.get(url)
    latest_weather = r.json()
    print("Weather updated:", latest_weather)

# Jalanin scheduler di background
def run_scheduler():
    schedule.every(5).minutes.do(fetch_weather)
    while True:
        schedule.run_pending()
        time.sleep(1)

@server.route("/")
def home():
    return jsonify({
        "status": "server jalan",
        "lastWeather": latest_weather
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=port)

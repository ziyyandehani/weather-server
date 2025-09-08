from flask import Flask, jsonify
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

latest_weather = None

def fetch_weather():
    global latest_weather
    city = "Malang"  # ganti sesuai lokasi
    api_key = os.getenv("OWM_API_KEY")  # pastikan di Railway → Variables
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        latest_weather = data
        print("Data cuaca diperbarui:", data.get("main"))
    except Exception as e:
        print("Gagal ambil data cuaca:", e)

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_weather, "interval", minutes=5)
scheduler.start()

@app.route("/")
def home():
    return jsonify({
        "status": "server jalan",
        "lastWeather": latest_weather
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

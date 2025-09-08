from flask import Flask, jsonify
import requests
import schedule
import time
import threading
import os

app = Flask(__name__)
latest_weather = None

API_KEY = os.getenv("OWM_API_KEY")  # set di Railway Variable
CITY = "Malang"                     # ganti lokasi sesuai kebutuhan

def fetch_weather():
    global latest_weather
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    try:
        r = requests.get(url)
        latest_weather = r.json()
        print("Data cuaca diperbarui:", latest_weather["main"])
    except Exception as e:
        print("Gagal ambil data cuaca:", e)

def scheduler():
    schedule.every(5).minutes.do(fetch_weather)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/")
def home():
    return jsonify({
        "status": "server jalan",
        "lastWeather": latest_weather
    })

if __name__ == "__main__":
    fetch_weather()  # ambil sekali di awal
    t = threading.Thread(target=scheduler, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

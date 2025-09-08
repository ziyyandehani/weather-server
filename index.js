import express from "express";
import fetch from "node-fetch";
import cron from "node-cron";

const app = express();
const PORT = process.env.PORT || 5000;

// Simpan data cuaca terakhir
let latestWeather = null;

// Fungsi fetch dari OpenWeatherMap
async function fetchWeather() {
  try {
    const city = "Malang"; // ganti sesuai lokasi
    const apiKey = process.env.OWM_API_KEY; // masukkan di Railway sebagai variable
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    const response = await fetch(url);
    const data = await response.json();

    latestWeather = data;
    console.log("Data cuaca diperbarui:", new Date().toISOString(), data);
    
  } catch (err) {
    console.error("Gagal ambil data cuaca:", err.message);
  }
}

// Scheduler: jalan tiap 5 menit
cron.schedule("*/5 * * * *", fetchWeather);

// Endpoint opsional untuk cek manual
app.get("/", (req, res) => {
  res.json({
    status: "server jalan",
    lastWeather: latestWeather,
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  fetchWeather(); // ambil sekali di awal
});

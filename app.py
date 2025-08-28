from flask import Flask, request

app = Flask(__name__)

@app.route("/data", methods=["POST"])
def get_data():
    data = request.json
    print("Data diterima:", data)
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

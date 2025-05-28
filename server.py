from flask import Flask, request, jsonify
import random

app = Flask(__name__)
estado_led = False

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/api/led", methods=["POST"])
def controlar_led():
    global estado_led
    estado_led = request.json.get("estado", False)
    print("Estado recibido:", estado_led)
    return {"ok": True}

@app.route("/api/estado", methods=["GET"])
def obtener_estado():
    return jsonify({"estado": estado_led})

@app.route("/api/sensores", methods=["GET"])
def datos_sensores():
    temp = round(random.uniform(20, 40), 2)
    hum = round(random.uniform(30, 70), 2)
    return jsonify({"temperatura": temp, "humedad": hum})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

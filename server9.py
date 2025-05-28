from flask import Flask, request, jsonify

app = Flask(__name__)
estado_led = False
ultimos_datos = {"temperatura": 0.0, "humedad": 0.0}

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

@app.route("/api/sensores", methods=["POST", "GET"])
def manejar_sensores():
    global ultimos_datos
    if request.method == "POST":
        datos = request.get_json()
        ultimos_datos["temperatura"] = datos.get("temperatura", 0.0)
        ultimos_datos["humedad"] = datos.get("humedad", 0.0)
        print("Datos recibidos:", ultimos_datos)
        return {"ok": True}
    else:
        return jsonify(ultimos_datos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

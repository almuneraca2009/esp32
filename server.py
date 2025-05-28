from flask import Flask, request, jsonify
app = Flask(__name__)

# Variable global para guardar el estado
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

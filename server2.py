from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/api/led", methods=["POST"])
def controlar_led():
    estado = request.json.get("estado")
    print("Estado recibido:", estado)
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request, jsonify, send_file
import sqlite3
from datetime import datetime
import pandas as pd
import pytz

app = Flask(__name__)
DB_FILE = "datos.db"
BOGOTA_TZ = pytz.timezone("America/Bogota")

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperatura REAL,
                humedad REAL,
                timestamp TEXT
            )
        """)
        conn.commit()

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/api/sensores", methods=["POST", "GET"])
def manejar_sensores():
    if request.method == "POST":
        data = request.get_json()
        temperatura = data.get("temperatura")
        humedad = data.get("humedad")
        timestamp = datetime.now(BOGOTA_TZ).isoformat()
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO sensores (temperatura, humedad, timestamp) VALUES (?, ?, ?)", (temperatura, humedad, timestamp))
        return {"ok": True}
    else:
        with sqlite3.connect(DB_FILE) as conn:
            row = conn.execute("SELECT temperatura, humedad, timestamp FROM sensores ORDER BY id DESC LIMIT 1").fetchone()
        return jsonify({"temperatura": row[0], "humedad": row[1], "timestamp": row[2]}) if row else jsonify({})

@app.route("/api/historico")
def historico():
    from_ts = request.args.get("from")
    to_ts = request.args.get("to")
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT temperatura, humedad, timestamp FROM sensores WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp", (from_ts, to_ts)).fetchall()
    return jsonify([{"temperatura": r[0], "humedad": r[1], "timestamp": r[2]} for r in rows])

@app.route("/api/exportar_excel")
def exportar_excel():
    from_ts = request.args.get("from")
    to_ts = request.args.get("to")
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM sensores WHERE timestamp BETWEEN ? AND ?", conn, params=(from_ts, to_ts))
    nombre = f"datos_{from_ts.replace(':','-')}_a_{to_ts.replace(':','-')}.xlsx"
    df.to_excel(nombre, index=False)
    return send_file(nombre, as_attachment=True)

estado_led = False

@app.route("/api/led", methods=["POST"])
def controlar_led():
    global estado_led
    estado_led = request.json.get("estado", False)
    return {"ok": True}

@app.route("/api/estado", methods=["GET"])
def obtener_estado():
    return jsonify({"estado": estado_led})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)

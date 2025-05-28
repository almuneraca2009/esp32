from flask import Flask, request, jsonify, send_file
import sqlite3
from datetime import datetime
import pandas as pd

app = Flask(__name__)
DB_FILE = "datos.db"

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

@app.before_first_request
def setup():
    init_db()

@app.route("/")
def index():
    return open("index.html").read()

@app.route("/api/sensores", methods=["POST", "GET"])
def manejar_sensores():
    if request.method == "POST":
        d = request.get_json()
        ts = datetime.utcnow().isoformat()
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO sensores (temperatura, humedad, timestamp) VALUES (?, ?, ?)",
                         (d.get("temperatura"), d.get("humedad"), ts))
        return {"ok": True}
    else:
        with sqlite3.connect(DB_FILE) as conn:
            r = conn.execute("SELECT temperatura, humedad, timestamp FROM sensores ORDER BY id DESC LIMIT 1").fetchone()
        return jsonify({"temperatura": r[0], "humedad": r[1], "timestamp": r[2]}) if r else jsonify({})

@app.route("/api/historico")
def historico():
    f1, f2 = request.args.get("from"), request.args.get("to")
    with sqlite3.connect(DB_FILE) as conn:
        r = conn.execute("SELECT temperatura, humedad, timestamp FROM sensores WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp", (f1, f2)).fetchall()
    return jsonify([{"temperatura": x[0], "humedad": x[1], "timestamp": x[2]} for x in r])

@app.route("/api/exportar_excel")
def exportar_excel():
    f1, f2 = request.args.get("from"), request.args.get("to")
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT * FROM sensores WHERE timestamp BETWEEN ? AND ?", conn, params=(f1, f2))
    nombre = f"datos_{f1.replace(':','-')}_a_{f2.replace(':','-')}.xlsx"
    df.to_excel(nombre, index=False)
    return send_file(nombre, as_attachment=True)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)

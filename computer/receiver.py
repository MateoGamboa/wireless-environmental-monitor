import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

DATABASE = "../database/environment.db"


def initialize_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            pressure REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/sensor", methods=["POST"])
def receive_sensor_data():
    data = request.get_json()

    temperature = data["temperature"]
    humidity = data["humidity"]
    pressure = data["pressure"]

    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        INSERT INTO sensor_readings (temperature, humidity, pressure)
        VALUES (?, ?, ?)
    """, (temperature, humidity, pressure))

    connection.commit()
    connection.close()

    print("Stored sensor data:")
    print(data)

    return jsonify({"status": "received"}), 200


@app.route("/api/latest")
def latest_reading():
    connection = sqlite3.connect(DATABASE)

    reading = connection.execute("""
        SELECT timestamp, temperature, humidity, pressure
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    connection.close()

    if reading is None:
        return jsonify({"error": "No readings available"}), 404

    return jsonify({
        "timestamp": reading[0],
        "temperature": reading[1],
        "humidity": reading[2],
        "pressure": reading[3]
    })

@app.route("/api/history")
def history():
    connection = sqlite3.connect(DATABASE)

    readings = connection.execute("""
        SELECT timestamp, temperature, humidity, pressure
        FROM sensor_readings
        ORDER BY id DESC
        LIMIT 50
    """).fetchall()

    connection.close()

    return jsonify([
        {
            "timestamp": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "pressure": row[3]
        }
        for row in readings
    ])


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
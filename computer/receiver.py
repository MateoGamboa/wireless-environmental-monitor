import sqlite3
from flask import Flask, request, jsonify

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


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
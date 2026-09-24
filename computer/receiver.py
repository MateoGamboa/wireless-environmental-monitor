from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/sensor", methods=["POST"])
def receive_sensor_data():
    data = request.get_json()

    print("Received sensor data:")
    print(data)

    return jsonify({"status": "received"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
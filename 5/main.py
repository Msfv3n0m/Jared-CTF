import jsonpickle
from flask import Flask, request
import datetime
import os

app = Flask(__name__)

DATA_FILE = "data_log.txt"


@app.route("/", methods=["POST"])
def root():
    raw = request.get_data(as_text=True)

    try:
        data = jsonpickle.decode(raw)
    except Exception as e:
        return f"Error decoding data: {e}", 400

    timestamp = datetime.datetime.utcnow().isoformat()
    entry = f"[{timestamp}] Received: {repr(data)}\n"

    with open(DATA_FILE, "a") as f:
        f.write(entry)

    response = {}
    if isinstance(data, dict) and "name" in data:
        response["message"] = f"Hello, {data['name']}!"
    else:
        response["message"] = "Data received and logged."

    response["received_at"] = timestamp

    return response, 200


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DATA_FILE) or ".", exist_ok=True)
    with open('README', 'r') as f:
        print(f"\033[32mGOAL: {f.read()}\033[0m")
    app.run(host='0.0.0.0')

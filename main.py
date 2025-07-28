import hashlib
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json.get("params", {})

    # Inject current timestamp if not provided
    timestamp = data.get("timestamp")
    if not timestamp:
        timestamp = str(int(time.time()))
        data["timestamp"] = timestamp

    # Strip any null or empty fields
    params_to_sign = {k: v for k, v in data.items() if v not in [None, ""]}

    # Sort params alphabetically
    sorted_items = sorted(params_to_sign.items())
    string_to_sign = "&".join(f"{k}={v}" for k, v in sorted_items)

    # Append API secret and hash using SHA-1
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    if not api_secret:
        return jsonify({"error": "CLOUDINARY_API_SECRET not set"}), 500

    to_hash = string_to_sign + api_secret
    signature = hashlib.sha1(to_hash.encode("utf-8")).hexdigest()

    return jsonify({
        "signature": signature,
        "string_to_sign": string_to_sign,
        "timestamp": timestamp
    })

if __name__ == "__main__":
    app.run(debug=True)

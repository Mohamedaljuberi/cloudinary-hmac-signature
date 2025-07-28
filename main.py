from flask import Flask, request, jsonify
import hashlib
import hmac
import time
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    # Example input JSON:
    # {
    #   "params": {
    #     "public_id": "your_id",
    #     "upload_preset": "preset",
    #     "folder": "your_folder",
    #     "unique_filename": "false"
    #   }
    # }

    data = request.json
    params = data.get("params", {})
    
    # Inject current Unix timestamp if not already provided
    if "timestamp" not in params:
        params["timestamp"] = str(int(time.time()))

    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not api_secret:
        return jsonify({"error": "Missing CLOUDINARY_API_SECRET"}), 500

    # Cloudinary says: sign everything EXCEPT file, cloud_name, resource_type, api_key
    # But include timestamp and any relevant optional fields like folder, public_id, upload_preset, unique_filename
    allowed_keys = [
        "eager", "folder", "invalidate", "overwrite", "public_id",
        "timestamp", "transformation", "upload_preset", "unique_filename"
    ]
    
    filtered = {k: v for k, v in params.items() if k in allowed_keys and v is not None}

    # Alphabetical order
    sorted_items = sorted(filtered.items())
    string_to_sign = "&".join(f"{k}={v}" for k, v in sorted_items)

    signature = hmac.new(
        api_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({
        "signature": signature,
        "string_to_sign": string_to_sign,
        "timestamp": params["timestamp"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

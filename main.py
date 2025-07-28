from flask import Flask, request, jsonify
import hashlib
import time
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})
    
    # Add timestamp if missing
    if "timestamp" not in params:
        params["timestamp"] = str(int(time.time()))

    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not api_secret:
        return jsonify({"error": "Missing CLOUDINARY_API_SECRET"}), 500

    allowed_keys = [
        "eager", "folder", "invalidate", "overwrite", "public_id",
        "timestamp", "transformation", "upload_preset", "unique_filename"
    ]

    filtered = {k: v for k, v in params.items() if k in allowed_keys and v is not None}
    sorted_items = sorted(filtered.items())
    string_to_sign = "&".join(f"{k}={v}" for k, v in sorted_items)

    # 🔥 FIXED: plain SHA1 hash, NOT HMAC
    signature_raw = string_to_sign + api_secret
    signature = hashlib.sha1(signature_raw.encode("utf-8")).hexdigest()

    return jsonify({
        "signature": signature,
        "string_to_sign": string_to_sign,
        "timestamp": params["timestamp"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

# ✅ Only include Cloudinary signable upload parameters
SIGNABLE_KEYS = [
    "callback", "eager", "folder", "invalidate", "overwrite", "public_id", "timestamp", "transformation", "upload_preset"
]

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})

    api_secret = os.environ.get("CLOUDINARY_API_SECRET")  # Set this securely in your environment
    if not api_secret:
        return jsonify({"error": "Missing CLOUDINARY_API_SECRET"}), 500

    # ✅ Filter only allowed parameters and remove None values
    filtered_params = {
        k: v for k, v in params.items()
        if k in SIGNABLE_KEYS and v is not None
    }

    # ✅ Sort parameters alphabetically by key
    sorted_items = sorted(filtered_params.items())
    string_to_sign = "&".join(f"{k}={v}" for k, v in sorted_items)

    # ✅ Generate HMAC-SHA1 signature using Cloudinary secret
    signature = hmac.new(
        api_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({
        "signature": signature,
        "string_to_sign": string_to_sign
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

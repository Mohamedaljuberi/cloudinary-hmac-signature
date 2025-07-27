from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})

    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not api_secret:
        return jsonify({"error": "CLOUDINARY_API_SECRET not set"}), 500

    # ✅ Include only the required parameters
    keys_to_sign = ["overwrite", "public_id", "timestamp", "upload_preset"]
    filtered_params = {k: v for k, v in params.items() if k in keys_to_sign and v is not None}

    # ✅ Sort alphabetically
    sorted_params = sorted(filtered_params.items())
    param_string = "&".join(f"{k}={v}" for k, v in sorted_params)

    print("STRING TO SIGN:", param_string)  # 🔍 Debug log

    # ✅ Generate signature
    signature = hmac.new(
        api_secret.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({"signature": signature})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

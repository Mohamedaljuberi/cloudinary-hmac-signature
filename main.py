from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})

    api_secret = os.environ.get('_ylC7lLKLqO4eN6rQK2APIZ-3XM')
    if not api_secret:
        return jsonify({"error": "CLOUDINARY_API_SECRET not set"}), 500

    # Only include allowed params (no 'file', 'api_key', etc.)
    allowed_keys = ["folder", "overwrite", "public_id", "timestamp", "upload_preset"]
    filtered_params = {k: v for k, v in params.items() if k in allowed_keys and v is not None}

    # ✅ Sort the filtered parameters alphabetically
    sorted_params = sorted(filtered_params.items())

    # Create the string to sign
    param_string = "&".join(f"{k}={v}" for k, v in sorted_params)

    print("STRING TO SIGN:", param_string)

    # Generate the SHA-1 HMAC signature
    signature = hmac.new(
        api_secret.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({"signature": signature, "string_to_sign": param_string})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

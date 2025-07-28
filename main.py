from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})

    # Make sure your secret is in your environment like:
    # export CLOUDINARY_API_SECRET=your_real_secret
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not api_secret:
        return jsonify({"error": "CLOUDINARY_API_SECRET not set"}), 500

    # Whitelist allowed keys
    allowed_keys = ["folder", "overwrite", "public_id", "timestamp", "upload_preset"]

    # Clean param values: strip whitespace and cast to string
    filtered_params = {
        k: str(v).strip() for k, v in params.items()
        if k in allowed_keys and v is not None
    }

    # Alphabetically sort params
    sorted_params = sorted(filtered_params.items())

    # Join into string to sign
    param_string = "&".join(f"{k}={v}" for k, v in sorted_params)

    # Generate SHA-1 HMAC signature
    signature = hmac.new(
        api_secret.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({
        "signature": signature,
        "string_to_sign": param_string
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

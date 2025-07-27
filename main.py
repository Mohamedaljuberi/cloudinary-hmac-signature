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

    # Build the param string in the original order, skipping empty values
    param_string = "&".join(f"{k}={v}" for k, v in params.items() if v)

    signature = hmac.new(
        api_secret.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({"signature": signature})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

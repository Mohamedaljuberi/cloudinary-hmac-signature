from flask import Flask, request, jsonify
import hashlib
import hmac
import os

app = Flask(__name__)

API_SECRET = "bf5MYFfKoqY51s-I3K_Fw9qC0OU"

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})

    # Required order for Cloudinary signature
    ordered_keys = ["overwrite", "public_id", "timestamp", "upload_preset"]
    ordered_params = [(k, params[k]) for k in ordered_keys if k in params and params[k]]

    param_string = "&".join(f"{k}={v}" for k, v in ordered_params)

    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({"signature": signature})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

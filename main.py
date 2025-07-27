from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

# Hardcoded API secret
API_SECRET = "bf5MYFfKoqY51s-I3K_Fw9qC0OU"

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})

    # Sort and filter out empty values
    sorted_params = sorted((k, v) for k, v in params.items() if v)
    param_string = "&".join(f"{k}={v}" for k, v in sorted_params)

    # Generate HMAC-SHA1 signature
    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({"signature": signature})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

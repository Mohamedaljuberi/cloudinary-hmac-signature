from flask import Flask, request, jsonify
import hashlib, hmac, os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_signature():
    data = request.json
    params = data.get("params", {})
    api_secret = os.environ.get("CLOUDINARY_API_SECRET")
    if not api_secret:
        return jsonify({"error": "Missing CLOUDINARY_API_SECRET"}), 500

    sorted_params = sorted((k, v) for k, v in params.items() if v)
    param_string = "&".join(f"{k}={v}" for k, v in sorted_params)
    signature = hmac.new(api_secret.encode(), param_string.encode(), hashlib.sha1).hexdigest()
    return jsonify({"signature": signature})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

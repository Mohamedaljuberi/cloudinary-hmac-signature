from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def sign():
    data = request.get_json()
    public_id = data.get("public_id")
    timestamp = data.get("timestamp")
    secret = os.getenv("CLOUDINARY_SECRET")

    if not public_id or not timestamp or not secret:
        return jsonify({"error": "Missing public_id, timestamp, or secret"}), 400

    string_to_sign = f"invalidate=true&overwrite=true&public_id={public_id}&timestamp={timestamp}"
    signature = hmac.new(
        key=secret.encode('utf-8'),
        msg=string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha1
    ).hexdigest()

    return jsonify({"signature": signature})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)
API_SECRET = "your_actual_api_secret_here"

@app.route("/", methods=["POST"])
def generate_signature():
    params = request.json.get("params", {})

    keys_to_sign = ["overwrite", "public_id", "timestamp", "upload_preset"]
    filtered_params = {k: v for k, v in params.items() if k in keys_to_sign and v is not None}
    sorted_params = sorted(filtered_params.items())
    param_string = "&".join(f"{k}={v}" for k, v in sorted_params)

    print("STRING TO SIGN:", param_string)

    signature = hmac.new(
        API_SECRET.encode("utf-8"),
        param_string.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return jsonify({
        "signature": signature,
        "string_to_sign": param_string
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

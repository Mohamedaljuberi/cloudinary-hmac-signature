# Cloudinary HMAC Signature Generator

This is a minimal Flask API that generates HMAC SHA-1 signatures for Cloudinary parameter validation.

## 🧠 What It Does

Accepts a JSON body with `params`, signs them using your Cloudinary API secret, and returns the signature.  
Useful for securing client-side upload widgets or authenticated API calls.

---

## 🧪 Example Request

```json
POST /
Content-Type: application/json

{
  "params": {
    "timestamp": "1690000000",
    "public_id": "example"
  }
}

import hmac
import hashlib

# REPLACE with your actual Cloudinary API secret
api_secret = "wTR7dDMs1ygFiG9mRgxor0QmrPA"

# String to sign (MUST match the fields you're sending to Cloudinary exactly)
string_to_sign = (
    "folder=what_is_this&"
    "public_id=king-henrys-cherry-slices-7oz-holly-market-oakland&"
    "timestamp=1753671747&"
    "upload_preset=auto_whatever"
)

# Create HMAC SHA-1 signature
signature = hmac.new(
    api_secret.encode('utf-8'),
    string_to_sign.encode('utf-8'),
    hashlib.sha1
).hexdigest()

print("✅ Signature:", signature)
print("🔐 String to Sign:", string_to_sign)

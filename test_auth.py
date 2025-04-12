import os
import json
import requests
import hmac
import hashlib
import time
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
# API_KEY = os.getenv("COINDCX_API_KEY")
# API_SECRET = os.getenv("COINDCX_API_SECRET")
import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
key = os.getenv("COINDCX_API_KEY")
secret = os.getenv("COINDCX_API_SECRET")

# python3
secret_bytes = bytes(secret, encoding='utf-8')


from api_service import CoinDCXApiService

# api_key = "your_api_key_here"
# api_secret = "your_api_secret_here"

client = CoinDCXApiService(key,secret)

try:
    data = client.make_authenticated_request("/exchange/v1/users/info")
    print("✅ Authenticated data:")
    print(data)
except Exception as e:
    print("❌ Failed:", str(e))

# # python2
# # secret_bytes = bytes(secret)

# # Generating a timestamp
# timeStamp = int(round(time.time() * 1000))

# body = {
#   "timestamp": timeStamp
# }

# json_body = json.dumps(body, separators = (',', ':'))

# signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

# url = "https://api.coindcx.com/exchange/v1/users/info"

# headers = {
#     'Content-Type': 'application/json',
#     'X-AUTH-APIKEY': key,
#     'X-AUTH-SIGNATURE': signature
# }

# response = requests.post(url, data = json_body, headers = headers)
# data = response.json();
# print(data);
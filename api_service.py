import json
import time
import hmac
import hashlib
import requests
from typing import Dict, Optional
from dotenv import load_dotenv
import os

class CoinDCXApiService:
    """
    Service for handling API communication with CoinDCX.
    """
    
    BASE_URL = "https://api.coindcx.com"

    # def __init__(self, api_key: str, api_secret: str):
    #     self.api_key = api_key
    #     self.api_secret = api_secret
    #     self.base_url = self.BASE_URL
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        load_dotenv()  # Load environment variables from .env file
        self.api_key = api_key or os.getenv("COINDCX_API_KEY")
        self.api_secret = api_secret or os.getenv("COINDCX_API_SECRET")
        self.base_url = "https://api.coindcx.com"

    def make_authenticated_request(self, endpoint: str, body: dict = None) -> Dict:
        """
        Make an authenticated POST request to the CoinDCX API.
        """
        timestamp = int(round(time.time() * 1000))
        body = body or {}
        payload = {
            "timestamp": timestamp,
            **body
        }

        json_body = json.dumps(payload, separators=(',', ':'))

        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            msg=json_body.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.api_key,
            'X-AUTH-SIGNATURE': signature
        }

        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=headers, data=json_body)

        if not response.ok:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")

        return response.json()
    
    def _sign_payload(self, payload):
        """
        Sign the payload with HMAC SHA256 using your API secret.
        """
        # Serialize payload without spaces for consistency
        payload_str = json.dumps(payload, separators=(',', ':'))
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            msg=payload_str.encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        return signature
    def get_balance(self):
        """
        Example method to fetch the user's account balance.
        You may need to adjust the endpoint and payload according to
        CoinDCX API documentation.
        """
        url = self.base_url + "/exchange/v1/users/balances"  # Adjust endpoint if needed.
        payload = {
            "timestamp": int(round(time.time() * 1000))
        }
        signature = self._sign_payload(payload)
        headers = {
            "X-AUTH-APIKEY": self.api_key,
            "X-AUTH-SIGNATURE": signature,
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    
    def get_ticker_data(self, symbol):
        
            """
        Fetch ticker data for a given symbol from CoinDCX.
        Adjust endpoint and filtering logic as per the CoinDCX API documentation.
        """
            url = f"{self.base_url}/exchange/ticker"
            response = requests.get(url)
            data = response.json()
        # Assuming data is a list of dictionaries and each has a 'market' field:
            return [item for item in data if item.get("market") == symbol]

    def make_public_request(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}{endpoint}"

        if method.upper() == "GET":
            response = requests.get(url, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, json=params if params else {})
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status {response.status_code}: {response.text}")

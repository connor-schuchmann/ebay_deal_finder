import base64
import os

import requests
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_ENV = os.getenv("EBAY_ENV")

TOKEN_URLS = {
    "SANDBOX": "https://api.sandbox.ebay.com/identity/v1/oauth2/token",
    "PRODUCTION": "https://api.ebay.com/identity/v1/oauth2/token",
}

SEARCH_URLS = {
    "SANDBOX": "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search",
    "PRODUCTION": "https://api.ebay.com/buy/browse/v1/item_summary/search",
}

def get_access_token():
    token_url = TOKEN_URLS[EBAY_ENV] # env toggle         

    creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
    creds_bytes = creds.encode()                  # txt -> bytes (for base64)
    creds_encoded = base64.b64encode(creds_bytes) # encode bytes
    creds_decoded = creds_encoded.decode()        # -> string for HTTP reader

    headers = {
        "Content-Type": "application/x-www-form-urlencoded", # body is form data (not JSON)
        "Authorization": f"Basic {creds_decoded}",           # get token
    }

    data = {
        "grant_type": "client_credentials",              # request as dev, not specified user
        "scope": "https://api.ebay.com/oauth/api_scope", # permission to read public data 
    }

    response = requests.post(token_url, headers=headers, data=data) # send request
    response.raise_for_status()                                     # guard for eBay error
    return response.json()["access_token"]                          # pull token -> JSON

def search_listings(token, query):
    search_url = SEARCH_URLS[EBAY_ENV] # env toggle

    headers = {
        "Content-Type": "application/json", # body is form JSON (not data)
        "Authorization": f"bearer {token}", # use token
    }

    params = {
        "q": query,  # keyword
        "limit": 50, # 0-200 per call
    }

    response = requests.get(search_url, headers=headers, params=params) # send request
    response.raise_for_status()                                         # guard for eBay error
    return response.json()                                              # pull info -> JSON


if __name__ == "__main__":
    # confirm env loaded
    print(f"Client ID: {CLIENT_ID}")
    print(f"Client Secret loaded: {bool(CLIENT_SECRET)}")
    print(f"Environment: {EBAY_ENV}")
    
    # confirm token
    token = get_access_token()
    print(f"Access token: {token[:15]}...")

    results = search_listings(token, "nike shirt")
    print(f"total matches: {results.get('total')}")
    print(f"Items returned: {len(results.get('itemSummaries', []))}")
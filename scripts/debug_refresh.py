import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_refresh():
    url = os.getenv("ZOHO_AUTH_URL")
    payload = {
        'refresh_token': os.getenv("ZOHO_REFRESH_TOKEN"),
        'client_id': os.getenv("ZOHO_CLIENT_ID"),
        'client_secret': os.getenv("ZOHO_CLIENT_SECRET"),
        'grant_type': 'refresh_token'
    }
    print(f"Testing Refresh on: {url}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, data=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_refresh()

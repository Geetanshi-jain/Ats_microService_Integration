import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

def get_token():
    payload = {
        'refresh_token': os.getenv("ZOHO_REFRESH_TOKEN"),
        'client_id': os.getenv("ZOHO_CLIENT_ID"),
        'client_secret': os.getenv("ZOHO_CLIENT_SECRET"),
        'grant_type': 'refresh_token'
    }
    response = requests.post(os.getenv("ZOHO_AUTH_URL"), data=payload)
    return response.json().get('access_token')

def list_modules():
    token = get_token()
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    base_url = os.getenv("ZOHO_BASE_URL")
    
    url = f"{base_url}/settings/modules"
    print(f"Fetching modules from: {url}")
    res = requests.get(url, headers=headers)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        modules = res.json().get('modules', [])
        for m in modules:
            print(f"- {m.get('api_name')} ({m.get('module_name')})")
            if 'Job' in m.get('api_name') or 'Cand' in m.get('api_name'):
                print(f"  Fields URL: {m.get('api_name')}/settings/fields")
    else:
        print(f"Error: {res.text}")

if __name__ == "__main__":
    list_modules()

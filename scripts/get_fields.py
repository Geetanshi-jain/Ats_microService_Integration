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

def get_fields(module, token):
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    base_url = os.getenv("ZOHO_BASE_URL")
    
    url = f"{base_url}/settings/fields?module={module}"
    print(f"Fetching fields for {module} from: {url}")
    res = requests.get(url, headers=headers)
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        fields = res.json().get('fields', [])
        for f in fields:
            if 'Job' in f.get('api_name') or 'Cand' in f.get('api_name') or f.get('data_type') == 'lookup':
                print(f"- {f.get('api_name')} ({f.get('field_label')}) - Type: {f.get('data_type')}")
    else:
        print(f"Error: {res.text}")

if __name__ == "__main__":
    token = get_token()
    if token:
        get_fields("Job_Openings", token)
        print("\n" + "="*50 + "\n")
        get_fields("Applications", token)
    else:
        print("Failed to get token")

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

def check_candidate_by_email(email):
    token = get_token()
    if not token:
        print("Failed to get token")
        return

    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    base_url = os.getenv("ZOHO_BASE_URL")
    
    # Search for candidate by email
    url = f"{base_url}/Candidates/search"
    params = {"criteria": f"(Email:equals:{email})"}
    
    print(f"Searching for Candidate Email: {email}")
    res = requests.get(url, headers=headers, params=params)
    
    if res.status_code == 200:
        data_list = res.json().get('data', [])
        if not data_list:
            print("No candidate found with this email.")
            return

        data = data_list[0]
        print("\n--- Zoho Candidate Details ---")
        print(f"ID: {data.get('id')}")
        print(f"Name: {data.get('First_Name')} {data.get('Last_Name')}")
        print(f"Email: {data.get('Email')}")
        print(f"Mobile: {data.get('Mobile')}")
        print(f"Status: {data.get('Candidate_Status')}")
        print("\nRaw Data Snapshot:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error fetching candidate: {res.status_code}")
        print(res.text)

if __name__ == "__main__":
    # Using the sample email provided by the user
    target_email = "test_1769776948@example.com"
    check_candidate_by_email(target_email)

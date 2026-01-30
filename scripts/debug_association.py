import requests
import os
from dotenv import load_dotenv

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

def test_association():
    token = get_token()
    headers = {'Authorization': f'Zoho-oauthtoken {token}'}
    base_url = os.getenv("ZOHO_BASE_URL")
    
    # Use real IDs from your previous run
    job_id = "210908000000354790"
    candidate_id = "210908000000358013" # Or use a fresh one
    
    print(f"Testing association for Job {job_id} and Candidate {candidate_id}")
    
    # Variation 1: Direct Associate_Job_Opening module
    url = f"{base_url}/Associate_Job_Opening"
    payload = {
        "data": [
            {
                "Job_Opening_ID": job_id,
                "Candidate_ID": candidate_id,
                "Status": "Applied"
            }
        ]
    }
    print(f"\nTrying Variation 1: POST {url}")
    res = requests.post(url, headers=headers, json=payload)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

    # Variation 3: Job_Openings/{id}/Candidates
    url = f"{base_url}/Job_Openings/{job_id}/Candidates"
    payload_sub = {
        "data": [
            {
                "id": candidate_id
            }
        ]
    }
    print(f"\nTrying Variation 3: POST {url}")
    res = requests.post(url, headers=headers, json=payload_sub)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

    # Variation 5: Applications module (Direct record creation)
    url = f"{base_url}/Applications"
    payload_app = {
        "data": [
            {
                "Candidate_ID": candidate_id,
                "Job_Opening_ID": job_id,
                "Status": "Applied"
            }
        ]
    }
    print(f"\nTrying Variation 5: POST {url}")
    res = requests.post(url, headers=headers, json=payload_app)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")

if __name__ == "__main__":
    test_association()

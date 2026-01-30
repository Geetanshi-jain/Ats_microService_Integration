import sys
import os

# Add current directory to path so we can import from folders
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import handler
import json

def test_full_flow():
    print("--- Testing Full Zoho Flow ---")
    
    # 1. Test GET /jobs
    print("Testing GET /jobs...")
    res_jobs = handler.get_jobs({}, {})
    jobs = json.loads(res_jobs['body'])
    print(f"Status: {res_jobs['statusCode']}, Jobs Found: {len(jobs)}")
    print(f"Jobs Body: {json.dumps(jobs, indent=2)}")
    
    if not jobs:
        print("No real jobs found in Zoho. Cannot test candidate creation efficiently.")
        return
        
    # Get the first real Job ID
    real_job_id = jobs[0].get('id')
    print(f"Using Real Job ID: {real_job_id} for further tests.")

    # 2. Test POST /candidates
    print(f"\nTesting POST /candidates for Job: {real_job_id}...")
    import time
    timestamp = int(time.time())
    body = {
        "name": f"Test User {timestamp}", 
        "email": f"test_{timestamp}@example.com", 
        "job_id": real_job_id
    }
    event = {"body": json.dumps(body)}
    res_cand = handler.create_candidate(event, {})
    print(f"Status: {res_cand['statusCode']}")
    print(f"Body: {res_cand['body']}")

    # 3. Test GET /applications
    print(f"\nTesting GET /applications for Job: {real_job_id}...")
    event_app = {"queryStringParameters": {"job_id": real_job_id}}
    res_app = handler.get_applications(event_app, {})
    print(f"Status: {res_app['statusCode']}")
    apps = json.loads(res_app['body'])
    print(f"Applications Found: {len(apps)}")
    if apps:
        print(f"Applications Body (First 3): {json.dumps(apps[:3], indent=2)}")

if __name__ == "__main__":
    test_full_flow()

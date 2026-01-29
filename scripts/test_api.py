import sys
import os

# Add current directory to path so we can import from folders
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import handler
import json

def test_jobs():
    print("Testing GET /jobs...")
    res = handler.get_jobs({}, {})
    print(f"Status: {res['statusCode']}")
    print(f"Body: {res['body']}")

def test_candidates():
    print("\nTesting POST /candidates...")
    body = {"name": "Test User", "email": "test@example.com", "job_id": "zoho-j1"}
    event = {"body": json.dumps(body)}
    res = handler.create_candidate(event, {})
    print(f"Status: {res['statusCode']}")
    print(f"Body: {res['body']}")

def test_applications():
    print("\nTesting GET /applications...")
    event = {"queryStringParameters": {"job_id": "zoho-j1"}}
    res = handler.get_applications(event, {})
    print(f"Status: {res['statusCode']}")
    print(f"Body: {res['body']}")

if __name__ == "__main__":
    test_jobs()
    test_candidates()
    test_applications()

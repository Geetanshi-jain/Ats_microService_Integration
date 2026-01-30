import json
from services.ats_service import ats_service

def response(status_code, body):
    return {
        "statusCode": status_code,
        "body": json.dumps(body)
    }

def get_jobs(event, context):
    try:
        jobs = ats_service.list_jobs()
        return response(200, jobs)
    except Exception as e:
        print(f"Error in get_jobs: {e}")
        return response(500, {"error": str(e)})

def create_candidate(event, context):
    try:
        if not event.get("body"):
             return response(400, {"error": "Missing request body"})
        
        body = json.loads(event["body"])
        
        # Basic validation
        required_fields = ["name", "email", "job_id"]
        missing = [f for f in required_fields if f not in body]
        if missing:
             return response(400, {"error": f"Missing required fields: {', '.join(missing)}"})

        result = ats_service.register_candidate(body)
        response_body = {
            "message": "Candidate applied successfully",
            "application_id": result.get("application_id")
        }
        return response(201, response_body)
    except json.JSONDecodeError:
        return response(400, {"error": "Invalid JSON in request body"})
    except Exception as e:
        print(f"Error in create_candidate: {e}")
        return response(500, {"error": str(e)})

def get_applications(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        job_id = query_params.get("job_id")
        
        if not job_id:
            return response(400, {"error": "Missing required query parameter: job_id"})
            
        applications = ats_service.list_applications(job_id)
        return response(200, applications)
    except Exception as e:
        print(f"Error in get_applications: {e}")
        return response(500, {"error": str(e)})

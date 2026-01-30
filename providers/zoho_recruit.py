import requests
import json
from .base import BaseATSProvider
from config.settings import settings
from utils.errors import ATSError
from utils.pagination import paginate_all

class ZohoRecruitProvider(BaseATSProvider):
    """Zoho Recruit ATS Integration"""

    def __init__(self):
        self.client_id = settings.ZOHO_CLIENT_ID
        self.client_secret = settings.ZOHO_CLIENT_SECRET
        self.refresh_token = settings.ZOHO_REFRESH_TOKEN
        self.base_url = settings.ZOHO_BASE_URL
        self.token_url = settings.ZOHO_AUTH_URL
        self._access_token = None

    def _get_access_token(self):
        """Fetch access token using refresh token."""
        if self._access_token:
            return self._access_token

        payload = {
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token"
        }
        
        try:
            # Use data=payload for POST token requests in Zoho
            response = requests.post(self.token_url, data=payload)
            response.raise_for_status()
            data = response.json()
            if "access_token" not in data:
                raise ATSError(f"Failed to get access token: {data.get('error', 'Unknown error')}", 401)
            
            self._access_token = data["access_token"]
            return self._access_token
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho Auth Error: {str(e)}", 401)

    def _get_headers(self):
        return {
            "Authorization": f"Zoho-oauthtoken {self._get_access_token()}",
            "Content-Type": "application/json"
        }

    def get_jobs(self):
        """Fetch all job openings from Zoho Recruit using pagination."""
        return paginate_all(self._fetch_jobs_page)

    def _fetch_jobs_page(self, page=1):
        """Fetch a single page of job openings."""
        url = f"{self.base_url}/Job_Openings"
        params = {"page": page}
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            
            if response.status_code == 204 or not response.text:
                return []
                
            response.raise_for_status()
            data = response.json()
            raw_jobs = data.get("data", [])
            return [self.normalize_job(j) for j in raw_jobs]
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho API Error: {str(e)}", 500)
        except json.JSONDecodeError:
            raise ATSError("Zoho API Error: Received invalid JSON response", 500)

    def create_candidate(self, candidate_data):
        """Create a candidate in Zoho Recruit, or return existing ID if duplicate."""
        url = f"{self.base_url}/Candidates"
        
        email = candidate_data.get("email")
        name_parts = candidate_data.get("name", "").split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else "N/A"

        payload = {
            "data": [
                {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "Mobile": candidate_data.get("phone", "")
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=self._get_headers(), data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            data = result.get("data", [{}])[0]
            
            # Handle success
            if data.get("status") == "success":
                candidate_id = data.get("details", {}).get("id")
                # Automatically attach to job if job_id is provided
                job_id = candidate_data.get("job_id")
                if job_id:
                    self.attach_candidate_to_job(candidate_id, job_id)
                    return {"application_id": f"{candidate_id}_{job_id}"}
                return {"candidate_id": candidate_id}
            
            # Handle duplicate error
            if data.get("status") == "error" and (data.get("code") == "DUPLICATE_DATA" or "Duplicate values" in data.get("message", "")):
                existing_id = self._search_candidate_by_email(email)
                job_id = candidate_data.get("job_id")
                if job_id:
                    self.attach_candidate_to_job(existing_id, job_id)
                    return {"application_id": f"{existing_id}_{job_id}"}
                return {"candidate_id": existing_id}
                
            if data.get("status") == "error":
                raise ATSError(f"Zoho Candidate Creation Error: {data.get('message')}", 400)
            
            return {"id": data.get("details", {}).get("id")}
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho API Error: {str(e)}", 500)

    def _search_candidate_by_email(self, email):
        """Search for a candidate ID by email address."""
        url = f"{self.base_url}/Candidates/search"
        params = {"criteria": f"(Email:equals:{email})"}
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            
            candidates = data.get("data", [])
            if candidates:
                return candidates[0].get("id")
                
            raise ATSError(f"Could not find existing candidate with email {email} despite duplicate error.", 404)
        except requests.exceptions.RequestException as e:
            raise ATSError(f"Zoho Search Error: {str(e)}", 500)

    def attach_candidate_to_job(self, candidate_id, job_id):
        """Associate a candidate with a job opening."""
        # Standard Zoho V2 Plural Association Endpoint
        url = f"{self.base_url}/Candidates/actions/associate"
        
        payload = {
          "data": [
            {
              "ids": [candidate_id],
              "jobids": [job_id],
              "status": "Associated"
            }
          ]
        }
        
        try:
            # V2.0 often uses PUT for the plural actions/associate endpoint
            response = requests.put(url, headers=self._get_headers(), data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            
            data = result.get("data", [{}])[0]
            if data.get("status") == "error":
                print(f"Warning: Zoho Association Error: {data.get('message')}")
                return False
            
            return True
        except requests.exceptions.RequestException as e:
            error_body = e.response.text if hasattr(e, 'response') and e.response else str(e)
            print(f"Warning: Zoho Association API Error: {error_body}")
            return False

    def get_applications(self, job_id):
        """Fetch all applications for a job using pagination."""
        return paginate_all(self._fetch_applications_page, job_id=job_id)

    def _fetch_applications_page(self, page=1, job_id=None):
        """Fetch a single page of applications for a job."""
        url = f"{self.base_url}/Applications/search"
        params = {
            "criteria": f"($Job_Opening_Id:equals:{job_id})",
            "page": page
        }
        
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            
            if response.status_code == 204:
                return []
                
            response.raise_for_status()
            data = response.json()
            raw_apps = data.get("data", [])
            
            return [self.normalize_application(a) for a in raw_apps]
        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to fetch applications for job {job_id} page {page}: {str(e)}")
            return []

    def normalize_job(self, raw_job):
        # Zoho status mapping to standard OPEN|CLOSED|DRAFT
        status_map = {
            "In-progress": "OPEN",
            "Waiting for approval": "DRAFT",
            "On-hold": "DRAFT",
            "Filled": "CLOSED",
            "Cancelled": "CLOSED",
            "Declined": "CLOSED"
        }
        
        raw_status = raw_job.get("Job_Opening_Status")
        normalized_status = status_map.get(raw_status, "OPEN") # Default to OPEN if unknown
        
        return {
            "id": str(raw_job.get("id")),
            "title": raw_job.get("Posting_Title"),
            "location": raw_job.get("City") or "Remote",
            "status": normalized_status,
            "external_url": f"https://recruit.zoho.in/recruit/ViewJob.na?digest={raw_job.get('id')}"
        }

    def normalize_application(self, raw_app):
        # Zoho status mapping to standard APPLIED|SCREENING|REJECTED|HIRED
        status_map = {
            "Associated": "APPLIED",
            "Applied": "APPLIED",
            "Screening": "SCREENING",
            "Interview": "SCREENING",
            "Offered": "SCREENING",
            "Rejected": "REJECTED",
            "Hired": "HIRED",
            "Hired-External": "HIRED"
        }
        
        raw_status = raw_app.get("Application_Status")
        normalized_status = status_map.get(raw_status, "APPLIED") # Default to APPLIED
        
        # The Applications module has candidate info directly or in fields like Full_Name, Email
        candidate_name = raw_app.get("Full_Name") or "Unknown"
        # If Full_Name is missing, try First/Last
        if candidate_name == "Unknown":
            first = raw_app.get("First_Name", "")
            last = raw_app.get("Last_Name", "")
            candidate_name = f"{first} {last}".strip() or "Unknown"

        return {
            "id": str(raw_app.get("id")),
            "candidate_name": candidate_name,
            "email": raw_app.get("Email", "N/A"),
            "status": normalized_status
        }

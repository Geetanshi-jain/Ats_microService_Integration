import requests
import json
from typing import List, Dict
from providers.base import BaseATSProvider
from config.settings import settings

class ZohoRecruitProvider(BaseATSProvider):
    def __init__(self):
        self.base_url = settings.ZOHO_BASE_URL
        self._access_token = None

    def _get_access_token(self):
        # Implementation for Zoho OAuth refresh token flow
        # For now, returning None until keys are configured
        if not settings.ZOHO_REFRESH_TOKEN:
            return None
            
        payload = {
            'refresh_token': settings.ZOHO_REFRESH_TOKEN,
            'client_id': settings.ZOHO_CLIENT_ID,
            'client_secret': settings.ZOHO_CLIENT_SECRET,
            'grant_type': 'refresh_token'
        }
        response = requests.post(settings.ZOHO_AUTH_URL, data=payload)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None

    def get_jobs(self) -> List[Dict]:
        # Mocking Zoho response if no API key
        if not settings.ZOHO_REFRESH_TOKEN:
            return [
                {"id": "zoho-j1", "title": "Zoho Developer", "location": "Chennai", "status": "OPEN", "external_url": "https://recruit.zoho.com/jobs/j1"}
            ]
        
        token = self._get_access_token()
        headers = {'Authorization': f'Zoho-oauthtoken {token}'}
        response = requests.get(f"{self.base_url}/Job_Openings", headers=headers)
        # Zoho specific parsing would go here
        return response.json().get('data', [])

    def create_candidate(self, data: Dict) -> Dict:
        # Mocking Zoho candidate creation
        if not settings.ZOHO_REFRESH_TOKEN:
            return {
                "candidate": {"id": "zoho-c1", "name": data.get("name")},
                "application": {"id": "zoho-a1", "status": "APPLIED"}
            }
            
        # Real Zoho API call to /Candidates and /Associate_Job_Opening
        # would be implemented here.
        return {}

    def get_applications(self, job_id: str) -> List[Dict]:
        if not settings.ZOHO_REFRESH_TOKEN:
            return [
                {"id": "zoho-a1", "candidate_name": "Zoho User", "email": "zoho@example.com", "status": "SCREENING"}
            ]
        return []

from typing import List, Dict
from providers.zoho_recruit import ZohoRecruitProvider

class ATSService:
    def __init__(self):
        # In a real app, we might use a factory to pick provider
        self.provider = ZohoRecruitProvider()

    def list_jobs(self) -> List[Dict]:
        return self.provider.get_jobs()

    def register_candidate(self, candidate_data: Dict) -> Dict:
        return self.provider.create_candidate(candidate_data)

    def list_applications(self, job_id: str) -> List[Dict]:
        return self.provider.get_applications(job_id)

ats_service = ATSService()

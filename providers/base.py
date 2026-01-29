from abc import ABC, abstractmethod
from typing import List, Dict

class BaseATSProvider(ABC):
    @abstractmethod
    def get_jobs(self) -> List[Dict]:
        """Fetch open jobs from ATS"""
        pass

    @abstractmethod
    def create_candidate(self, data: Dict) -> Dict:
        """Create a candidate and link to a job"""
        pass

    @abstractmethod
    def get_applications(self, job_id: str) -> List[Dict]:
        """Fetch applications for a specific job"""
        pass

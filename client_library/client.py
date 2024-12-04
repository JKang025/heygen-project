import requests
from .exceptions import ServerError

class VideoTranslationClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout

    def get_status(self, job_id):
        response = requests.get(f"{self.base_url}/status", params={"job_id": job_id}, timeout=self.timeout)
        if response.status_code != 200:
            raise ServerError("Failed to fetch status.")
        return response.json()["result"]

    def poll_status(self, job_id, max_wait=300, interval=5):
        # Polling logic here
        pass

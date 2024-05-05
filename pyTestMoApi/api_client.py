import os

import requests
from .errors import ErrorHandling


class ApiClient:

    def __init__(self, token: str = None, instance: str = None):
        self.instance = instance if instance else os.environ["TESTMO_INSTANCE"]
        self.token = token if token else os.environ["TESTMO_TOKEN"]
        self.BASE_URL = f"https://{self.instance}.testmo.net/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    def api_get(self, endpoint: str, *args, **kwargs) -> requests.Response:
        res = requests.get(f"{self.BASE_URL}{endpoint}", headers=self.headers, timeout=15, *args, **kwargs)
        ErrorHandling(res.status_code).handler()
        return res

    def api_post(self, endpoint: str, *args, **kwargs) -> requests.Response:
        res = requests.post(f"{self.BASE_URL}{endpoint}", headers=self.headers, timeout=15, *args, **kwargs)
        ErrorHandling(res.status_code).handler()
        return res

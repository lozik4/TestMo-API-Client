import os

import requests

from ._errors import ErrorHandling


class ApiClient:

    def __init__(self, token: str = None, instance: str = None, api_version: str = "v1"):
        self.instance = instance or os.getenv("TESTMO_INSTANCE")
        self.token = token or os.getenv("TESTMO_TOKEN")
        if not self.instance:
            raise ValueError(
                "TESTMO_INSTANCE must be provided either as argument or environment variable",
            )
        if not self.token:
            raise ValueError(
                "TESTMO_TOKEN must be provided either as argument or environment variable",
            )

        self.BASE_URL = f"https://{self.instance}.testmo.net/api/{api_version}"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    def get(self, endpoint: str, *args, **kwargs) -> requests.Response:
        res = requests.get(f"{self.BASE_URL}{endpoint}", headers=self.headers, timeout=15, *args, **kwargs)
        ErrorHandling(res.status_code).handler()
        return res

    def post(self, endpoint: str, json: dict, *args, **kwargs) -> requests.Response:
        res = requests.post(
            f"{self.BASE_URL}{endpoint}",
            json=json,
            headers=self.headers,
            timeout=15,
            *args,
            **kwargs
        )
        ErrorHandling(res.status_code).handler()
        return res

    def patch(self, endpoint: str, json: dict, **kwargs) -> requests.Response:
        res = requests.patch(f"{self.BASE_URL}{endpoint}", json=json, headers=self.headers, timeout=15, **kwargs)
        ErrorHandling(res.status_code).handler()
        return res

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        res = requests.delete(f"{self.BASE_URL}{endpoint}", headers=self.headers, timeout=15, **kwargs)
        ErrorHandling(res.status_code).handler()
        return res

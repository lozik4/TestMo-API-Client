from .api_client import ApiClient
from .utils import expands_validator


class Roles:

    def __init__(self):
        self.client = ApiClient()
        self.valid_expansions = ["users"]

    def get_roles(self, page: int = 1, per_page: int = 100, expands: str = ""):
        url = f"/roles?page={page}&per_page={per_page}"
        url += expands_validator(expands, self.valid_expansions)
        return self.client.api_get(url).json()

    def get_role_by_id(self, role_id: int, expands: str = ""):
        url = f"/roles/{role_id}?"
        url += expands_validator(expands, self.valid_expansions)
        return self.client.api_get(url).json()

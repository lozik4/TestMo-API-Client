from .api_client import ApiClient
from .utils import expands_validator, pagination_validator


class Groups:
    def __init__(self):
        self.client = ApiClient()
        self.valid_expansions = ["users"]

    def get_groups(self, page: int = 1, per_page: int = 100):
        url = f"/groups?page={page}"
        url += pagination_validator(per_page)
        return self.client.api_get(url).json()

    def get_group_info(self, group_id: int, expands: str = ""):
        url = f"/groups/{group_id}?"
        url += expands_validator(expands, self.valid_expansions)
        return self.client.api_get(url).json()

from .api_client import ApiClient
from .utils import expands_validator, pagination_validator


class Runs:

    def __init__(self):
        self.client = ApiClient()
        self.valid_expansions = ["configs", "issues", "milestones", "states", "statuses", "users"]

    def get_project_runs(self, project_id: int, page: int = 1, per_page: int = 100):
        url = f"/projects/{project_id}/runs?page={page}"
        url += pagination_validator(per_page)
        return self.client.api_get(url).json()

    def get_run_info(self, run_id: int, expands: str = ""):
        url = f"/runs/{run_id}?"
        url += expands_validator(expands, self.valid_expansions)
        return self.client.api_get(url).json()

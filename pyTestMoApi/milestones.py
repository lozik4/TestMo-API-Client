from .api_client import ApiClient
from .utils import expands_validator, pagination_validator


class Milestones:

    def __init__(self):
        self.client = ApiClient()
        self.valid_expansions = ["issues", "milestone_stats", "milestone_types", "milestones", "statuses", "users"]

    def get_project_milestones(self, project_id: int, page: int = 1, per_page: int = 100):
        url = f"/projects/{project_id}/milestones?page={page}"
        url += pagination_validator(per_page)
        return self.client.api_get(url).json()

    def get_milestone_info(self, milestone_id: int, expands: str = ""):
        url = f"/milestones/{milestone_id}?"
        url += expands_validator(expands, self.valid_expansions)
        return self.client.api_get(url).json()

from .api_client import ApiClient
from .utils import expands_validator, pagination_validator


class AutomationRuns:
    def __init__(self):
        self.client = ApiClient()
        self.valid_expansions = ["automation_sources", "configs", "milestones", "statuses", "users"]

    def get_automation_runs(self, project_id: int, page: int = 1, per_page: int = 100):
        url = f"/projects/{project_id}/automation/runs?page={page}"
        url += pagination_validator(per_page)
        return self.client.api_get(url).json()

    def get_automation_run_info(self, run_id: int, expands=""):
        url = f"/automation/runs/{run_id}?"
        url += expands_validator(expands, self.valid_expansions)
        return self.client.api_get(url).json()

    # TODO: Write POST methods

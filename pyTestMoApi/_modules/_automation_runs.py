from typing import Literal, Sequence

from .._utils import ApiClient, Pagination, build_expands

Expands = Literal["automation_sources", "configs", "milestones", "statuses", "users"]
ALLOWED_EXPANDS = ["automation_sources", "configs", "milestones", "statuses", "users"]


class AutomationRuns:
    def __init__(self, api_client: ApiClient):
        self.__client = api_client

    def get_automation_runs(self, project_id: int, page: int = 1, per_page: int = 100) -> dict:
        """Return automation runs for a given project.

        References:
            https://support.testmo.com/hc/en-us/articles/38162558701133-Automation-runs#1-get--projects--project-id--automation-runs-
        """
        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/projects/{project_id}/automation/runs",
        )
        return self.__client.get(url).json()

    def get_automation_run_info(self, run_id: int, expands: Sequence[Expands] | Expands = "") -> dict:
        """Return a single automation run by id.

        References:
            https://support.testmo.com/hc/en-us/articles/38162558701133-Automation-runs#2-get--automation-runs--run-id--
        """
        url = f"/automation/runs/{run_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self.__client.get(url).json()

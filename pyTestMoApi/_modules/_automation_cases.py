from typing import Literal, Sequence

from .._utils import BoundApi, Order, Pagination, build_expands, build_filters

Expands = Literal["automation_sources", "statuses"]
ALLOWED_EXPANDS = ["automation_sources", "statuses"]


class AutomationCases(BoundApi):
    def get_project_automation_cases(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 100,
        expands: Sequence[Expands] | Expands = "",
        *,
        order: Order = "asc",
        sort: Literal[
            "automation_sources:created_at",
            "automation_cases:name",
            "automation_cases:elapsed_average",
            "automation_cases:failure_count",
            "automation_cases:flaky_percent",
        ] = "automation_sources:created_at",
        source_id: str = "",
        status: str = "",
        name: str = "",
        folder: str = "",
    ) -> dict:
        """Get automation cases by project id.

        References:
            https://support.testmo.com/hc/en-us/articles/44292211893517-Automation-Cases

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of automation cases to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: automation_sources, statuses)
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: asc)
        :param sort: Sort field for the list of automation cases (supported: automation_sources:created_at,
                        automation_cases:name, automation_cases:elapsed_average, automation_cases:failure_count,
                        automation_cases:flaky_percent; default: automation_sources:created_at)
        :param source_id: Comma-separated list of automation sources to filter by.
        :param status: Comma-separated list of statuses to filter by. Use: 1 for neutral, 2 for success,
                        3 for failure, 4 for running.
        :param name: Limit result to automation cases matching this name.
        :param folder: Limit result to automation cases matching this folder.
        :return: Returns all automation cases for a project.

        Example:
            Get latest 100 automation cases for project with ID 5
            GET /api/v1/projects/5/automation/cases

            Get second result page (pagination)
            GET /api/v1/projects/5/automation/cases?page=2

            Get automation cases filtered by source
            GET /api/v1/projects/5/automation/cases?source_id=1

            Get failing automation cases sorted by failure count
            GET /api/v1/projects/5/automation/cases?status=3&sort=automation_cases:failure_count&order=desc

            Get automation cases and include source details
            GET /api/v1/projects/5/automation/cases?expands=automation_sources
        """

        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/projects/{project_id}/automation/cases",
        ) + build_expands(expands, ALLOWED_EXPANDS)
        params = {
            "order": order,
            "sort": sort,
            "source_id": source_id,
            "status": status,
            "name": name,
            "folder": folder,
        }

        filters = build_filters(params)
        return self._api.get(url + filters).json()

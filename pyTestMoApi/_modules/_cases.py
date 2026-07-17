from typing import Literal, Sequence

from .._utils import BoundApi, DateIso, Order, Pagination, build_date, build_expands, build_filters

Expands = Literal["automation_links", "comments", "folders", "history", "users", "tags", "templates"]
ALLOWED_EXPANDS = ["automation_links", "comments", "folders", "history", "users", "tags", "templates"]


class Cases(BoundApi):
    def get_project_cases(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 100,
        expands: Sequence[Expands] | Expands = "",
        *,
        order: Order = "desc",
        sort: Literal["repository_cases:created_at", "repository_cases:name"] = "repository_cases:created_at",
        created_by: str = "",
        folder_id: int | None = None,
        template_id: int | None = None,
        state_id: str = "",
        status_id: str = "",
        created_after: DateIso = "",
        created_before: DateIso = "",
        has_automation: bool | None = None,
        has_automation_status: bool | None = None,
    ) -> dict:
        """Get project cases

        References:
            https://support.testmo.com/hc/en-us/articles/40051160964749-Cases#1--get--projects--project-id--cases-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of cases to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: "automation_links", "comments",
                                                                "folders", "history", "users", "tags", "templates"
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc)
        :param sort: Sort field for the list of cases (supported: repository_cases:created_at, repository_cases:name;
                                                        default: repository_cases:created_at)
        :param created_by: Comma-separated list of user IDs to filter by.
        :param folder_id: Limit results to a single specified folder ID.
        :param template_id: Limit results to a single specified template ID.
        :param created_after: Limit result to cases created after (in ISO8601 format and UTC time zone).
        :param created_before: Limit result to cases created before (in ISO8601 format and UTC time zone).
        :param has_automation: Limit result to cases with automation (true, 1) or without automation (false, 0).
        :param has_automation_status: Limit result to cases with automation status (true, 1)
        or without automation status (false, 0).
        :param state_id: Comma-separated list of workflow states to filter by.
        :param status_id: Comma-separated list of statuses to filter by.
        :return: Returns a list of cases from the specified project.

        Examples:
            Paginate through results (page 2, 100 per page)
            GET /projects/1/cases?page=2&per_page=100

            Filter by folder and template
            GET /projects/1/cases?folder_id=10&template_id=3

            Sort by name ascending
            GET /projects/1/cases?sort=name&order=asc

            Get test cases created in a date range
            GET /projects/1/cases?created_after=2025-06-01T00:00:00Z&created_before=2025-06-15T23:59:59Z

            Get test cases and automation links
            GET /projects/1/cases?expand=automation_links

            Get test case and history
            GET /projects/1/cases?expand=history
        """
        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/projects/{project_id}/cases",
        ) + build_expands(expands, ALLOWED_EXPANDS)

        params = {
            "order": order,
            "sort": sort,
            "created_by": created_by,
            "folder_id": folder_id,
            "template_id": template_id,
            "created_after": build_date(created_after),
            "created_before": build_date(created_before),
            "has_automation": has_automation,
            "has_automation_status": has_automation_status,
            "state_id": state_id,
            "status_id": status_id,
        }
        filters = build_filters(params)
        return self._api.get(url + filters).json()

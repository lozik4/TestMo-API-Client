from typing import Literal, Sequence

from .._utils import BoundApi, Pagination, build_expands, Order, DateIso, build_date, build_filters

Expands = Literal["automation_sources", "configs", "milestones", "statuses", "users"]
ALLOWED_EXPANDS = ["automation_sources", "configs", "milestones", "statuses", "users"]


class AutomationRuns(BoundApi):
    def get_project_automation_runs(
            self,
            project_id: int,
            page: int = 1,
            per_page: int = 100,
            expands: Sequence[Expands] | Expands = "",
            *,
            order: Order = "desc",
            sort: Literal["automation_runs:created_at"] = "automation_runs:created_at",
            config_id: str = "",
            created_after: DateIso = "",
            created_before: DateIso = "",
            created_by: str = "",
            milestone_id: str = "",
            source_id: str = "",
            status: str = "",
            tags: str = ""
    ) -> dict:
        """ Get automation runs by project id.

        References:
            https://support.testmo.com/hc/en-us/articles/37971158770957-Automation-Runs#1-get--projects--project-id--automation-runs-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of automation runs to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: automation_sources, configs, milestones,
                                                                                statuses, users)
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc)
        :param sort: Sort field for the list of automation runs (supported: automation_runs:created_at;
                                                                default: automation_runs:created_at)
        :param config_id: Comma-separated list of configurations to filter by.
        :param created_after: Limit result to automation runs created after (in ISO8601 format and UTC time zone).
        :param created_before: Limit result to automation runs created before (in ISO8601 format and UTC time zone).
        :param created_by: Comma-separated list of users to filter by.
        :param milestone_id: Comma-separated list of milestones to filter by.
        :param source_id: Comma-separated list of automation sources to filter by.
        :param status: Comma-separated list of statuses to filter by. Use: 2 for success, 3 for failure, 4 for running.
        :param tags: Comma-separated list of tags to filter by.
        :return: Returns all automation runs for a project.

        Example:
            Get latest 100 automation runs for project with ID 5
            GET /api/v1/projects/5/automation/runs

            Get second result page (pagination)
            GET /api/v1/projects/5/automation/runs?page=2

            Get latest 100 automation runs
            GET /api/v1/projects/5/automation/runs

            Get latest 100 failed automation runs
            GET /api/v1/projects/5/automation/runs?state=3

            Get latest automation runs created after a certain date & time
            GET /api/v1/projects/5/automation/runs?created_after=2023-02-15T00:00:00.000Z

            Get automation runs and include expands
            GET /api/v1/projects/5/automation/runs?expands=automation_sources,configs,users
        """

        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/projects/{project_id}/automation/runs",
        ) + build_expands(expands, ALLOWED_EXPANDS)
        params = {
            "order": order,
            "sort": sort,
            "config_id": config_id,
            "created_after": build_date(created_after),
            "created_before": build_date(created_before),
            "created_by": created_by,
            "milestone_id": milestone_id,
            "source_id": source_id,
            "status": status,
            "tags": tags
        }

        filters = build_filters(params)
        return self._api.get(url + filters).json()

    def get_automation_run_by_id(self, automation_run_id: int, expands: Sequence[Expands] | Expands = "") -> dict:
        """Return a single automation run by id.

        References:
            https://support.testmo.com/hc/en-us/articles/38162558701133-Automation-runs#2-get--automation-runs--run-id--

        :param automation_run_id: Automation run id
        :param expands: Comma-separated list of expands to return (supported: automation_sources, configs, milestones,
                                                                            statuses, users)
        :return: Returns a single automation run by id.

        Example:
            Get the automation run with ID 5
            GET /api/v1/automation/runs/5

            Get a automation run and include expands
            GET /api/v1/automation/runs/1?expands=automation_sources,configs,users

        """
        url = f"/automation/runs/{automation_run_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

    # TODO POST methods

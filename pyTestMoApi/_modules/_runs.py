from typing import Literal, Sequence

from .._utils import BoolFilter, BoundApi, DateIso, Order, Pagination, build_date, build_expands, build_filters

Expands = Literal["configs", "issues", "milestones", "states", "statuses", "users"]
ALLOWED_EXPANDS = ["configs", "issues", "milestones", "states", "statuses", "users"]


class Runs(BoundApi):

    def get_project_runs(
            self,
            project_id: int,
            page: int = 1,
            per_page: int = 100,
            expands: Sequence[Expands] | Expands = "",
            *,
            order: Order = "desc",
            sort: Literal["runs:created_at", "runs:closed_at"] = "runs:created_at",
            closed_after: DateIso = "",
            closed_before: DateIso = "",
            config_id: str = "",
            created_after: DateIso = "",
            created_before: DateIso = "",
            created_by: str = "",
            is_closed: BoolFilter = None,
            milestone_id: str = "",
            state_id: str = "",
            tags: str = "",
    ):
        """This method uses pagination so you might need to request additional pages to retrieve all runs

        References:
            https://support.testmo.com/hc/en-us/articles/38159162797197-Runs#1-get--projects--project-id--runs-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of runs to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: configs, issues,
                                                                    milestones, states, statuses, users)
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc)
        :param sort: Sort field for the list of runs (supported: runs:created_at,
                                                        runs:closed_at; default: runs:created_at)
        :param closed_after: Limit result to runs closed after (in ISO8601 format and UTC time zone).
        :param closed_before: Limit result to runs closed before (in ISO8601 format and UTC time zone).
        :param config_id: Comma-separated list of configurations to filter by.
        :param created_after: Limit result to runs created after (in ISO8601 format and UTC time zone).
        :param created_before: Limit result to runs created before (in ISO8601 format and UTC time zone).
        :param created_by: Comma-separated list of users to filter by.
        :param is_closed: Limit result to active or closed runs only.
        :param milestone_id: Comma-separated list of milestones to filter by.
        :param state_id: Comma-separated list of workflow states to filter by.
        :param tags: Comma-separated list of tags to filter by.
        :return: Returns all runs for a project.

        Example:
            Get latest 100 runs for project with ID 5
            GET /api/v1/projects/5/runs

            Get second result page (pagination)
            GET /api/v1/projects/5/runs?page=2

            Get latest 100 active runs
            GET /api/v1/projects/5/runs?is_closed=0

            Get latest 100 closed runs, ordered by close date
            GET /api/v1/projects/5/runs?is_closed=1&sort=runs:closed_at

            Get latest runs created after a certain date & time
            GET /api/v1/projects/5/runs?created_after=2023-02-15T00:00:00.000Z

            Get runs and include expands
            GET /api/v1/projects/5/runs?expands=configs,issues,users
        """
        url = Pagination(
            page=page,
            per_page=per_page,
        ).set_paginator(f"/projects/{project_id}/runs") + build_expands(expands, ALLOWED_EXPANDS)
        params = {
            "order": order,
            "sort": sort,
            "closed_after": build_date(closed_after),
            "closed_before": build_date(closed_before),
            "config_id": config_id,
            "created_after": build_date(created_after),
            "created_before": build_date(created_before),
            "created_by": created_by,
            "is_closed": is_closed,
            "milestone_id": milestone_id,
            "state_id": state_id,
            "tags": tags,
        }
        filters = build_filters(params)
        print(url + filters)
        return self._api.get(url + filters).json()

    def get_runs_by_id(self, run_id: int, expands: Sequence[Expands] | Expands = ""):
        """Info about a specific run

        References:
            https://support.testmo.com/hc/en-us/articles/38159162797197-Runs#2-get--runs--run-id--

        :param run_id: ID of the run to return.
        :param expands: Comma-separated list of expands to return. (supported: configs, issues,
                                                                    milestones, states, statuses, users)
        :return: Returns a single run.

        Example:
            Get the run with ID 5
            GET /api/v1/runs/5

            Get a run and include expands
            GET /api/v1/runs/1?expands=configs,issues,users
        """
        url = f"/runs/{run_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

from typing import Literal, Sequence

from .._utils import BoolFilter, BoundApi, DateIso, Order, Pagination, build_date, build_expands, build_filters

Expands = Literal["issues", "users"]
ALLOWED_EXPANDS = ["issues", "users"]


class Results(BoundApi):

    def get_run_result(
            self,
            run_id: int,
            page: int = 1,
            per_page: int = 100,
            expands: Sequence[Expands] | Expands = "",
            *,
            sort: Literal["run_results:created_at"] = "run_results:created_at",
            order: Order = "desc",
            created_after: DateIso = "",
            created_before: DateIso = "",
            created_by: str = "",
            assignee_id: int | None = None,
            status_id: int | None = None,
            get_latest_result: BoolFilter = None,
    ):
        """
        Get a run result.

        References:
            https://support.testmo.com/hc/en-us/articles/38165496269325-Results#1-get--runs--run-id--results-

        :param run_id: ID of the run.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of results to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Expands to return (supported: ["issues", "users"])
        :param sort: Sort field for the list of results
                            (supported: run_results:created_at; default: run_results:created_at)
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc)
        :param created_after: Limit result set to results created after (in ISO8601 format and UTC time zone).
        :param created_before: Limit result set to results created before (in ISO8601 format and UTC time zone).
        :param created_by: Comma-separated list of users to filter by.
        :param assignee_id: Comma-separated list of assignees to filter by.
                                    Use assignee_id=0 for unassigned test case results.
        :param status_id: Comma-separated list of statuses to filter by. The system supports up to 25 total statuses.
                    Use the ID keys & name values as defined in your instance,
                    typically: 1 for Untested, 2 for Passed, 3 for Failed, 4 for Retest, 5 for Blocked, 6 for Skipped.
                    Unless modified by your administrator, custom statuses will have IDs 7-25.
        :param get_latest_result: Indicates whether to fetch only the latest result (true, 1) or all results (false, 0).
        :return: Returns all test results for a run.

        Examples:
            Get results for run with ID 1
            /api/v1/runs/1/results

            Get results and limit to 1 page with 25 results including expands
            /api/v1/runs/1/results?page=1&per_page=25&expands=issues,users
        """
        route = f"/runs/{run_id}/results"
        url = Pagination(per_page=per_page, page=page).set_paginator(route) + build_expands(expands, ALLOWED_EXPANDS)
        params = {
            "order": order,
            "sort": sort,
            "created_after": build_date(created_after),
            "created_before": build_date(created_before),
            "created_by": created_by,
            "assignee_id": assignee_id,
            "status_id": status_id,
            "get_latest_result": get_latest_result,
        }
        filters = build_filters(params)
        return self._api.get(url + filters).json()

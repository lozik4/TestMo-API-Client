from typing import Literal, Sequence

from .._utils import BoolFilter, BoundApi, DateIso, Order, Pagination, build_date, build_expands, build_filters

Expands = Literal["issues", "milestone_stats", "milestone_types", "milestones", "statuses", "users"]
ALLOWED_EXPANDS = ["issues", "milestone_stats", "milestone_types", "milestones", "statuses", "users"]


class Milestones(BoundApi):
    def get_project_milestones(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 100,
        expands: Sequence[Expands] | Expands = "",
        *,
        order: Order = "desc",
        sort: Literal["milestones:created_at", "milestones:completed_at"] = "milestones:created_at",
        automation_tags: str = "",
        completed_after: DateIso = "",
        completed_before: DateIso = "",
        created_after: DateIso = "",
        created_before: DateIso = "",
        created_by: str = "",
        is_completed: BoolFilter = None,
        parent_id: str = "",
        root_id: str = "",
        type_id: str = "",
    ):
        """
        Returns all milestones for a project.
        This method uses pagination so you might need to request additional pages to retrieve all milestones.

        References:
            https://support.testmo.com/hc/en-us/articles/38157425816717-Milestones#1-get--projects--project-id--milestones-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of milestones to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: issues, milestone_stats,
                                                                    milestone_types, milestones, statuses, users)
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc)
        :param sort: Sort field for the list of milestones (supported: milestones:created_at,
                        milestones:completed_at; default: milestones:created_at)
        :param automation_tags: Comma-separated list of automation tags to filter by.
        :param completed_after: Limit result to milestones completed after (in ISO8601 format and UTC time zone).
        :param completed_before: Limit result to milestones completed before (in ISO8601 format and UTC time zone).
        :param created_after: Limit result to milestones created after (in ISO8601 format and UTC time zone).
        :param created_before: Limit result to milestones created before (in ISO8601 format and UTC time zone).
        :param created_by: Comma-separated list of users to filter by.
        :param is_completed: Limit result to active or completed milestones only. (1=True, 0=False,
                                                                                    None=don't use this filter)
        :param parent_id: Comma-separated list of parent milestones to filter by.
        :param root_id: Comma-separated list of root milestones to filter by.
        :param type_id: Comma-separated list of milestone types to filter by.
        :return: dict with list of milestones

        Example:
            Get latest 100 milestones for project with ID 5
            GET /api/v1/projects/5/milestones

            Get second result page (pagination)
            GET /api/v1/projects/5/milestones?page=2

            Get latest 100 active milestones
            GET /api/v1/projects/5/milestones?is_completed=0

            Get latest 100 completed milestones, ordered by completion date
            GET /api/v1/projects/5/milestones?is_completed=1&sort=milestones:completed_at

            Get latest milestones created after a certain date & time
            GET /api/v1/projects/5/milestones?created_after=2023-02-15T00:00:00.000Z

            Get milestones and include expands
            GET /api/v1/projects/5/milestones?expands=issues,milestone_types,users
        """
        route = f"/projects/{project_id}/milestones"
        url = Pagination(page=page, per_page=per_page).set_paginator(route) + build_expands(expands, ALLOWED_EXPANDS)
        params = {
            "order": order,
            "sort": sort,
            "automation_tags": automation_tags,
            "completed_after": build_date(completed_after),
            "completed_before": build_date(completed_before),
            "created_after": build_date(created_after),
            "created_before": build_date(created_before),
            "created_by": created_by,
            "is_completed": is_completed,
            "parent_id": parent_id,
            "root_id": root_id,
            "type_id": type_id,
        }
        filters = build_filters(params)
        return self._api.get(url + filters).json()

    def get_milestone_by_id(self, milestone_id: int, expands: Sequence[Expands] | Expands = ""):
        """
        Get milestone by id

        References:
            https://support.testmo.com/hc/en-us/articles/38157425816717-Milestones#2-get--milestones--milestone-id--

        :param milestone_id: ID of the milestone to return.
        :param expands: Comma-separated list of expands to return. (supported: "issues", "milestone_stats",
                                                                "milestone_types", "milestones", "statuses", "users")
        :return: Returns a single milestone.

        Example:
            Get the milestone with ID 5
            GET /api/v1/milestones/5

            Get a milestone and include expands
            GET /api/v1/milestones/1?expands=issues,milestone_types,users
        """
        url = f"/milestones/{milestone_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

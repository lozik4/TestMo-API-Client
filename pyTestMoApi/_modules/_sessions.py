from typing import Literal, Sequence

from .._utils import BoolFilter, BoundApi, DateIso, Order, Pagination, build_date, build_expands, build_filters

Expands = Literal["configs", "field_values", "issues", "milestones", "states", "statuses", "templates", "users"]
ALLOWED_EXPANDS = ["configs", "field_values", "issues", "milestones", "states", "statuses", "templates", "users"]


class Sessions(BoundApi):
    def get_project_sessions(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 100,
        expands: Sequence[Expands] | Expands = "",
        *,
        order: Order = "desc",
        sort: Literal["sessions:created_at", "sessions:closed_at"] = "sessions:created_at",
        assignee_id: str = "",
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
        template_id: str = "",
    ) -> dict:
        """Get sessions for a project.

        References:
            https://support.testmo.com/hc/en-us/articles/38159977518989-Sessions#1-get--projects--project-id--sessions-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of sessions to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: "configs", "field_values", "issues",
                                                            "milestones", "states", "statuses", "templates", "users")
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc)
        :param sort: Sort field for the list of sessions (supported: sessions:created_at, sessions:closed_at;
                                                            default: sessions:created_at)
        :param assignee_id: Comma-separated list of assignees to filter by.
        :param closed_after: Limit result to sessions closed after (in ISO8601 format and UTC time zone).
        :param closed_before: Limit result to sessions closed before (in ISO8601 format and UTC time zone).
        :param config_id: Comma-separated list of configurations to filter by.
        :param created_after: Limit result to sessions created after (in ISO8601 format and UTC time zone).
        :param created_before: Limit result to sessions created before (in ISO8601 format and UTC time zone).
        :param created_by: Comma-separated list of users to filter by.
        :param is_closed: Limit result to active or closed sessions only.
        :param milestone_id: Comma-separated list of milestones to filter by.
        :param state_id: Comma-separated list of workflow states to filter by.
        :param tags: Comma-separated list of tags to filter by.
        :param template_id: Comma-separated list of templates to filter by.
        :return: Returns all sessions for a project.

        Example:
            Get latest 100 sessions for project with ID 5
            GET /api/v1/projects/5/sessions

            Get second result page (pagination)
            GET /api/v1/projects/5/sessions?page=2

            Get latest 100 active sessions
            GET /api/v1/projects/5/sessions?is_closed=0

            Get latest 100 closed sessions, ordered by close date
            GET /api/v1/projects/5/sessions?is_closed=1&sort=sessions:closed_at

            Get latest sessions created after a certain date & time
            GET /api/v1/projects/5/sessions?created_after=2023-02-15T00:00:00.000Z

            Get sessions and include expands
            GET /api/v1/projects/5/sessions?expands=configs,issues,users
        """

        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/projects/{project_id}/sessions",
        ) + build_expands(expands, ALLOWED_EXPANDS)

        params = {
            "order": order,
            "sort": sort,
            "assignee_id": assignee_id,
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
            "template_id": template_id,
        }
        filters = build_filters(params)
        return self._api.get(url + filters).json()

    def get_session_by_id(self, session_id: int, expands: Sequence[Expands] | Expands = ""):
        """Get info about a session

        References:
            https://support.testmo.com/hc/en-us/articles/38159977518989-Sessions#2-get--sessions--session-id--

        :param session_id: ID of the session to return.
        :param expands: Comma-separated list of expands to return. (supported: "configs", "field_values", "issues",
                                                            "milestones", "states", "statuses", "templates", "users")
        :return: Returns a single session.

        Example:
            Get the session with ID 5
            GET /api/v1/sessions/5

            Get a session and include expands
            GET /api/v1/sessions/1?expands=configs,issues,users
        """
        url = f"/sessions/{session_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

from typing import Literal, Sequence

from .._utils import BoolFilter, BoundApi, Order, Pagination, build_expands, build_filters

Expands = Literal["users"]
ALLOWED_EXPANDS = ["users"]


class AutomationSource(BoundApi):
    def get_automation_sources(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 100,
        expands: Sequence[Expands] | Expands = "",
        *,
        order: Order = "desc",
        sort: Literal[
            "automation_sources:created_at",
            "automation_sources:ran_at",
            "automation_sources:retired_at",
        ] = "automation_sources:created_at",
        is_retired: BoolFilter = None,
    ):
        """Get all automation sources for a project.

        References:
            https://support.testmo.com/hc/en-us/articles/37974874224141-Automation-Sources#1-get--projects--project-id--automation-sources-

        :param project_id: ID of the project.
        :param page: Page number to return (default: 1)
        :param per_page: Max items per page (15, 25, 50, 100; default: 100)
        :param expands: Comma-separated expands to include additional data. (supported: users)
        :param order: Sort order (asc or desc; default: desc)
        :param sort: Field to sort by (automation_sources:created_at, ran_at, retired_at; default: created_at)
        :param is_retired: Filter active/retired automation sources
        :return: Returns all automation sources for a project.

        Example:
            Get latest 100 automation sources for project ID 5
            GET /api/v1/projects/5/automation/sources

            Get second result page (pagination)
            GET /api/v1/projects/5/automation/sources?page=2

            Get latest 100 active automation sources
            GET /api/v1/projects/5/automation/sources?is_retired=0

            Get latest 100 retired automation sources, ordered by retire date
            GET /api/v1/projects/5/automation/sources?is_retired=1&sort=automation_sources:retired_at

            Get automation sources and include user details
            GET /api/v1/projects/5/automation/sources?expands=users
        """
        route = f"/projects/{project_id}/automation/sources"
        url = Pagination(page=page, per_page=per_page).set_paginator(route) + build_expands(expands, ALLOWED_EXPANDS)

        params = {
            "order": order,
            "sort": sort,
            "is_retired": is_retired,
        }
        filters = build_filters(params)
        return self._api.get(url + filters).json()

    def get_automation_source_by_id(self, automation_source_id: int, expands: Sequence[Expands] | Expands = ""):
        """ " Get info about a specific automation source by its ID.

        References:
            https://support.testmo.com/hc/en-us/articles/37974874224141-Automation-Sources#2-get--automation-sources--automation-source-id--

            :param automation_source_id: ID of the automation source
            :param expands: Comma-separated expands to include additional data. (supported: users)
            :return: Returns a single automation source.

            Example:
                Get the automation source with ID 5
                GET /api/v1/automation/sources/5

                Get an automation source and include user details
                GET /api/v1/automation/sources/1?expands=users
        """

        url = f"/automation/sources/{automation_source_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

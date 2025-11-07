from typing import Literal

from .._utils import BoolFilter, BoundApi, Order, Pagination, build_expands

Expands = Literal["users"]
ALLOWED_EXPANDS = ["users"]


class Projects(BoundApi):

    def get_projects(self,
                     page: int = 1,
                     per_page: int = 100,
                     expands: Expands = "",
                     *,
                     order: Order = "desc",
                     is_completed: BoolFilter = None,
                     ):
        """
        Returns all projects (a user has access to).
        This method uses pagination so you might need to request additional pages to retrieve all projects.

        References:
            https://support.testmo.com/hc/en-us/articles/38158978447885-Projects#1-get--projects-

        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of projects to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: "users")
        :param order: Order of results (asc or desc; default: desc)
        :param is_completed: Limit result to active or completed projects only.
                                (1=True, 0=False, None=don't use this filter)
        :return: dict with list of projects

        Example:
            Get latest 100 projects
            GET /api/v1/projects

            Get second result page (pagination)
            GET /api/v1/projects?page=2

            Get latest 100 active projects
            GET /api/v1/projects?is_completed=0

            Get latest 100 completed projects, ordered by completion date
            GET /api/v1/projects?is_completed=1&sort=projects:completed_at

            Get projects and include user details
            GET /api/v1/projects?expands=users
        """

        url = Pagination(page=page, per_page=per_page).set_paginator("/projects") + build_expands(expands,
                                                                                                  ALLOWED_EXPANDS)

        return self._api.get(url, params={"order": order, "is_completed": is_completed}).json()

    def get_project_by_id(self, project_id: int, expands: Expands = ""):
        """
        Returns a single project (if the user has access to the project).
        References:
            https://support.testmo.com/hc/en-us/articles/38158978447885-Projects#2-get--projects--project-id--
        :param project_id: ID of the project to return.
        :param expands: Comma-separated list of expands to return. (supported: "users")
        :return: dict with project info

        Example:
            Get the project with ID 5
            GET /api/v1/projects/5

            Get a project and include user details
            GET /api/v1/projects/1?expands=users

        """
        url = f"/projects/{project_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

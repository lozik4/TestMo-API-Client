from typing import Literal

from .._utils import BoundApi, Order, Pagination, build_filters


class Folders(BoundApi):
    def get_project_folders(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = 100,
        *,
        order: Order = "desc",
        sort: Literal["display_order", "name"] = "display_order",
        parent_id: int | None = None,
        name: str = "",
    ) -> dict:
        """Get project folders

        References:
            https://support.testmo.com/hc/en-us/articles/40067196221837-Folders#1--get--projects--project-id--folders-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page).
        :param per_page: Maximum number of folders to return (supported: 15, 25, 50, 100; default: 100).
        :param order: Sort order (ascending or descending) (supported: asc, desc; default: desc).
        :param sort: Sort field for the list of folders (supported: display_order, name; default: display_order:desc).
        :param parent_id: Filter by parent folder ID.
        :param name: Filter by name (partial match, e.g., "login" supported).
        :return: Returns a list of folders from the specified project.

        Example:
            Get folders with pagination
            GET /projects/1/folders?limit=2&offset=2

            Filter by parent folder ID
            GET /projects/1/folders?parent_id=601

            Filter by name (partial match)
            GET /projects/1/folders?name=login

            Request with combined filters
            GET /projects/1/folders?name=login&parent_id=601&limit=1
        """
        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/projects/{project_id}/folders",
        )
        params = {
            "order": order,
            "sort": sort,
            "parent_id": parent_id,
            "name": name,
        }
        filters = build_filters(params)
        return self._api.get(url + filters).json()

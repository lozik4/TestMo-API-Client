from typing import Literal, Sequence

from .._utils import BoundApi, Pagination, build_expands

Expands = Literal["users"]
ALLOWED_EXPANDS = ["users"]


class Groups(BoundApi):
    def get_groups(self, page: int = 1, per_page: int = 100, expands: Sequence[Expands] | Expands = ""):
        """
        Returns all groups. Requires site admin access.
        This method uses pagination so you might need to request additional pages to retrieve all groups.

        References:
            https://support.testmo.com/hc/en-us/articles/38071122378637-Groups#1-get--groups-
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of groups to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: users)
        :return: dict with list of groups

        Example:
            Get first 100 groups
            GET /api/v1/groups

            Get second result page (pagination)
            GET /api/v1/groups?page=2

            Get groups and include user details
            GET /api/v1/groups?expands=users
        """
        url = Pagination(page=page, per_page=per_page).set_paginator("/groups") + build_expands(
            expands,
            ALLOWED_EXPANDS,
        )
        return self._api.get(url).json()

    def get_groups_by_id(self, group_id: int, expands: Sequence[Expands] | Expands = ""):
        """
        Returns a single group. Requires site admin access.

        References:
            https://support.testmo.com/hc/en-us/articles/38071122378637-Groups#2-get--groups--group-id--

        :param group_id: ID of the group to return.
        :param expands:  Comma-separated list of expands to return. (supported: users)
        :return: dict with group info

        Example:
            Get the group with ID 5
            GET /api/v1/groups/5

            Get a group and include user details
            GET /api/v1/groups/1?expands=users
        """
        url = f"/groups/{group_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

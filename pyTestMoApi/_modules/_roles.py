from typing import Literal, Sequence

from .._utils import BoundApi, Pagination, build_expands

Expands = Literal["users"]
ALLOWED_EXPANDS = ["users"]


class Roles(BoundApi):
    def get_roles(self, page: int = 1, per_page: int = 100, expands: Sequence[Expands] | Expands = ""):
        """Get Roles
        Reference:
            https://support.testmo.com/hc/en-us/articles/38159045680525-Roles#1--get--roles-

        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of roles to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: users)
        :return: Returns all roles. Requires site admin access.

        Example:
            Get first 100 roles
            GET /api/v1/roles

            Get second result page (pagination)
            GET /api/v1/roles?page=2

            Get roles and include user details
            GET /api/v1/roles?expands=users
        """

        url = Pagination(page=page, per_page=per_page).set_paginator("/roles") + build_expands(expands, ALLOWED_EXPANDS)
        return self._api.get(url).json()

    def get_role_by_id(self, role_id: int, expands: Sequence[Expands] | Expands = ""):
        """Get info about a role

        Reference:
            https://support.testmo.com/hc/en-us/articles/38159045680525-Roles#2--get--roles--role-id--

        :param role_id: ID of the role to return.
        :param expands: Comma-separated list of expands to return. (supported: users)
        :return: Returns a single role. Requires site admin access.

        Example:
            Get the role with ID 5
            GET /api/v1/roles/5

            Get a role and include user details
            GET /api/v1/roles/1?expands=users
        """
        url = f"/roles/{role_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self._api.get(url).json()

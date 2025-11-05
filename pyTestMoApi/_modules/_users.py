from typing import Literal, Sequence

from .._utils import ApiClient, Pagination, build_expands

Expands = Literal["groups", "roles", "users"]
ALLOWED_EXPANDS = ["groups", "roles", "users"]


class Users:

    def __init__(self, api_client: ApiClient):
        self.__client = api_client

    def get_current_user(self):
        """
        Returns the current user. A typical use case for this method is to test API access and authentication.

        References:
            https://support.testmo.com/hc/en-us/articles/38165363497741-Users#2-get--user-

        :return: dict with user info

        Example:
        GET /api/v1/user

        Response:
        200 OK
        {
            "id": 1,
            "name": "User 1",
            "timezone": null,
            "date_format": null,
            "time_format": null
        }
        """
        return self.__client.get("/user").json()

    def get_users(self, page: int = 1, per_page: int = 100, expands: Sequence[Expands] | Expands = "") -> dict:
        """
        Returns all users. Requires site admin access.
        This method uses pagination so you might need to request additional pages to retrieve all users.

        References:
            https://support.testmo.com/hc/en-us/articles/38165363497741-Users#3-get--users-

        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of users to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: groups, roles, users)
        :return: dict with list of users

        Example:
        Get first 100 users
        GET /api/v1/users

        Get second result page (pagination)
        GET /api/v1/users?page=2

        Get users and include group & role details
        GET /api/v1/users?expands=groups,roles
        """
        url = Pagination(page=page, per_page=per_page).set_paginator("/users") + build_expands(expands, ALLOWED_EXPANDS)
        return self.__client.get(url).json()

    def get_users_by_id(self, user_id: int, expands: Sequence[Expands] | Expands = ""):
        """
        Returns a single user. Requires site admin access.

        References:
            https://support.testmo.com/hc/en-us/articles/38165363497741-Users#4-get--users--user-id--

        :param user_id: ID of the user to return.
        :param expands: Comma-separated list of expands to return. (supported: groups, roles, users)
        :return: dict with user info

        Example:
        Get the user with ID 5
        GET /api/v1/users/5

        Get a user and include group & role details
        GET /api/v1/users/1?expands=groups,roles
        """
        url = f"/users/{user_id}" + build_expands(expands, ALLOWED_EXPANDS, ampersand=False)
        return self.__client.get(url).json()

    def get_users_by_project_id(self, project_id: int, page: int = 1, per_page: int = 100):
        """
        Returns all users for a project.
        This method uses pagination so you might need to request additional pages to retrieve all users.

        References:
            https://support.testmo.com/hc/en-us/articles/38165363497741-Users#1-get--projects--project-id--users-

        :param project_id: ID of the project.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of users to return (supported: 15, 25, 50, 100; default: 100)
        :return: dict with list of users

        Example:
        Get first 100 users for project with ID 5
        GET /api/v1/project/5/users

        Get second result page (pagination)
        GET /api/v1/project/5/users?page=2

        Response:
        200 OK
        {
            "page": 1,
            "prev_page": null,
            "next_page": 2,
            "last_page": 2,
            "per_page": 100,
            "total": 150,
            "result": [
                { "id": 1, "name": "User 1", },
                { "id": 2, "name": "User 2", },
                ..
            ]
        }
        """
        url = Pagination(page=page, per_page=per_page).set_paginator(f"/projects/{project_id}/users")
        print(url)
        return self.__client.get(url).json()

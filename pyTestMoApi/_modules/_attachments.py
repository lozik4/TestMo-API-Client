from typing import Literal, Sequence

from .._utils import BoundApi, Order, Pagination, build_expands, build_filters

Expands = Literal["users"]
ALLOWED_EXPANDS = ["users"]


class Attachments(BoundApi):

    def get_case_attachments(
            self,
            case_id: int,
            page: int = 1,
            per_page: int = 100,
            expands: Sequence[Expands] | Expands = "",
            *,
            order: Order = "desc",
            created_by: str = "",
    ) -> dict:
        """ Get case attachments

        References:
            https://support.testmo.com/hc/en-us/articles/40045804558093-Attachments#1--get--cases--case-id--attachments-

        :param case_id: ID of the case.
        :param page: Number of page to return (default: first page)
        :param per_page: Maximum number of attachments to return (supported: 15, 25, 50, 100; default: 100)
        :param expands: Comma-separated list of expands to return. (supported: users)
        :param order: Sort order ascending or descending by attachment ID (supported: asc, desc; default: desc)
        :param created_by: Comma-separated list of user IDs to filter by.
        :return: Returns attachment details for a test case, including the path for download.

        Example:
            Paginate through results (page 1, 20 per page)
            GET /cases/1/attachments?limit=20&offset=0
            Limit results to 5 attachments
            GET /cases/1/attachments?limit=5
            Filter by user who created the attachments
            GET /cases/1/attachments?created_by=1
            Combine pagination + filter
            GET /cases/1001/attachments?limit=10&offset=10&created_by=1
        """
        url = Pagination(page=page, per_page=per_page).set_paginator(
            f"/cases/{case_id}/attachments",
        ) + build_expands(expands, ALLOWED_EXPANDS)
        params = {
            "order": order,
            "created_by": created_by,
        }
        filters = build_filters(params)
        print(url + filters)
        return self._api.get(url + filters).json()

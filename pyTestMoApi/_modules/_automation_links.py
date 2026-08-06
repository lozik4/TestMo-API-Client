from typing import Sequence

from .._utils import BoundApi

MIN_BULK_LINKS = 1
MAX_BULK_LINKS = 500

AutomationLinkPair = tuple[int, int]


class AutomationLinks(BoundApi):
    def create_automation_link(self, project_id: int, case_id: int, automation_case_id: int) -> None:
        """Link a single automation case to a repository test case.

        Creating a link connects an automated test to a manual test case in the repository so
        that automation coverage and the latest automation status appear on the case. The call
        is idempotent: linking the same pair twice is a safe no-op.

        References:
            https://support.testmo.com/hc/en-us/articles/47317503859469-Automation-Links#1-post--projects--project-id--automation-links

        :param project_id: ID of the project.
        :param case_id: ID of the repository test case to link to.
        :param automation_case_id: ID of the automation case to link (as returned by
                                   GET /automation/runs/{run_id}/tests as ``automation_case_id``).
        :return: None. The endpoint responds with ``204 No Content`` on success.
        :raises requests.exceptions.HTTPError: If the API returns a non-success status code.

        Example:
            Link automation case 101 to repository case 42 in project 1
            POST /api/v1/projects/1/automation-links
            {"case_id": 42, "automation_case_id": 101}
        """
        payload = {"case_id": case_id, "automation_case_id": automation_case_id}
        self._api.post(f"/projects/{project_id}/automation-links", json=payload)

    def create_automation_links_bulk(self, project_id: int, links: Sequence[AutomationLinkPair]) -> None:
        """Link many automation case / repository case pairs in a single request.

        This is the recommended way to create links at scale (up to 500 pairs per request). The
        call is idempotent (already-linked pairs are ignored) but validation is all-or-nothing: if
        any ``case_id`` or ``automation_case_id`` is invalid, the whole request is rejected and no
        links are created.

        References:
            https://support.testmo.com/hc/en-us/articles/47317503859469-Automation-Links#2-post--projects--project-id--automation-links-bulk

        :param project_id: ID of the project.
        :param links: Sequence of ``(case_id, automation_case_id)`` pairs to link (1..500 pairs).
        :return: None. The endpoint responds with ``204 No Content`` on success.
        :raises ValueError: If the number of pairs is outside the supported 1..500 range.
        :raises requests.exceptions.HTTPError: If the API returns a non-success status code.

        Example:
            Link three pairs in project 1
            POST /api/v1/projects/1/automation-links/bulk
            {"links": [{"case_id": 42, "automation_case_id": 101},
                       {"case_id": 43, "automation_case_id": 102}]}
        """
        pairs = [
            {"case_id": case_id, "automation_case_id": automation_case_id} for case_id, automation_case_id in links
        ]
        count = len(pairs)
        if not MIN_BULK_LINKS <= count <= MAX_BULK_LINKS:
            raise ValueError(
                f"Number of links must be between {MIN_BULK_LINKS} and {MAX_BULK_LINKS} (got {count}).",
            )
        self._api.post(f"/projects/{project_id}/automation-links/bulk", json={"links": pairs})

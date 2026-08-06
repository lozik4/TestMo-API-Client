import pytest

from pyTestMoApi._modules import Cases
from pyTestMoApi._modules._cases import (
    MAX_CASE_NAMES_PER_PAGE,
    MIN_CASE_NAMES_PER_PAGE,
)


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


class FakeApiClient:
    def __init__(self):
        self.last_url = None

    def get(self, url):
        self.last_url = url
        return FakeResponse({"result": []})


def test_case_names_default_call_builds_paginated_url():
    fake_client = FakeApiClient()
    cases = Cases(fake_client)

    cases.get_project_case_names(1)

    assert fake_client.last_url == "/projects/1/cases/names?page=1&per_page=100"


def test_case_names_custom_pagination():
    fake_client = FakeApiClient()
    cases = Cases(fake_client)

    cases.get_project_case_names(7, page=2, per_page=250)

    assert fake_client.last_url == "/projects/7/cases/names?page=2&per_page=250"


def test_case_names_per_page_boundaries_are_accepted():
    for per_page in (MIN_CASE_NAMES_PER_PAGE, MAX_CASE_NAMES_PER_PAGE):
        fake_client = FakeApiClient()
        cases = Cases(fake_client)

        cases.get_project_case_names(1, per_page=per_page)

        assert f"per_page={per_page}" in fake_client.last_url


def test_case_names_per_page_below_range_raises():
    fake_client = FakeApiClient()
    cases = Cases(fake_client)

    with pytest.raises(ValueError, match="per_page must be between"):
        cases.get_project_case_names(1, per_page=MIN_CASE_NAMES_PER_PAGE - 1)
    assert fake_client.last_url is None


def test_case_names_per_page_above_range_raises():
    fake_client = FakeApiClient()
    cases = Cases(fake_client)

    with pytest.raises(ValueError, match="per_page must be between"):
        cases.get_project_case_names(1, per_page=MAX_CASE_NAMES_PER_PAGE + 1)
    assert fake_client.last_url is None

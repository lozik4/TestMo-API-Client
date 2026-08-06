import pytest

from pyTestMoApi._modules import AutomationRuns
from pyTestMoApi._modules._automation_runs import (
    MAX_RUN_TESTS_PER_PAGE,
    MIN_RUN_TESTS_PER_PAGE,
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


def test_run_tests_default_call_builds_paginated_url_without_filters():
    fake_client = FakeApiClient()
    automation_runs = AutomationRuns(fake_client)

    automation_runs.get_automation_run_tests(1)

    url = fake_client.last_url
    assert url.startswith("/automation/runs/1/tests?page=1&per_page=100")
    assert "order=desc" in url
    assert "sort=automation_run_tests%3Aid" in url
    assert "thread_id" not in url
    assert "status_id" not in url


def test_run_tests_with_filters_builds_expected_query():
    fake_client = FakeApiClient()
    automation_runs = AutomationRuns(fake_client)

    automation_runs.get_automation_run_tests(
        1,
        page=2,
        per_page=500,
        order="asc",
        sort="automation_run_tests:elapsed",
        thread_id=5,
        status_id="3",
    )

    url = fake_client.last_url
    assert url.startswith("/automation/runs/1/tests?page=2&per_page=500")
    assert "order=asc" in url
    assert "sort=automation_run_tests%3Aelapsed" in url
    assert "thread_id=5" in url
    assert "status_id=3" in url


def test_run_tests_per_page_boundaries_are_accepted():
    for per_page in (MIN_RUN_TESTS_PER_PAGE, MAX_RUN_TESTS_PER_PAGE):
        fake_client = FakeApiClient()
        automation_runs = AutomationRuns(fake_client)

        automation_runs.get_automation_run_tests(1, per_page=per_page)

        assert f"per_page={per_page}" in fake_client.last_url


def test_run_tests_per_page_below_range_raises():
    fake_client = FakeApiClient()
    automation_runs = AutomationRuns(fake_client)

    with pytest.raises(ValueError, match="per_page must be between"):
        automation_runs.get_automation_run_tests(1, per_page=50)
    assert fake_client.last_url is None


def test_run_tests_per_page_above_range_raises():
    fake_client = FakeApiClient()
    automation_runs = AutomationRuns(fake_client)

    with pytest.raises(ValueError, match="per_page must be between"):
        automation_runs.get_automation_run_tests(1, per_page=MAX_RUN_TESTS_PER_PAGE + 1)
    assert fake_client.last_url is None

import pytest

from pyTestMoApi._modules import AutomationCases


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


def test_default_call_builds_paginated_url_without_filters():
    fake_client = FakeApiClient()
    automation_cases = AutomationCases(fake_client)

    automation_cases.get_project_automation_cases(5)

    assert fake_client.last_url.startswith("/projects/5/automation/cases?page=1&per_page=100")
    assert "order=asc" in fake_client.last_url
    assert "sort=automation_sources%3Acreated_at" in fake_client.last_url
    assert "source_id" not in fake_client.last_url
    assert "status" not in fake_client.last_url
    assert "name" not in fake_client.last_url
    assert "folder" not in fake_client.last_url
    assert "expands" not in fake_client.last_url


def test_call_with_filters_and_expands_builds_expected_query():
    fake_client = FakeApiClient()
    automation_cases = AutomationCases(fake_client)

    automation_cases.get_project_automation_cases(
        5,
        page=2,
        per_page=50,
        expands="automation_sources",
        order="desc",
        sort="automation_cases:failure_count",
        source_id="1,2",
        status="3",
        name="Login",
        folder="Auth",
    )

    url = fake_client.last_url
    assert url.startswith("/projects/5/automation/cases?page=2&per_page=50&expands=automation_sources")
    assert "order=desc" in url
    assert "sort=automation_cases%3Afailure_count" in url
    assert "source_id=1%2C2" in url
    assert "status=3" in url
    assert "name=Login" in url
    assert "folder=Auth" in url


def test_invalid_expand_raises_value_error():
    fake_client = FakeApiClient()
    automation_cases = AutomationCases(fake_client)

    with pytest.raises(ValueError, match="expands must be"):
        automation_cases.get_project_automation_cases(5, expands="not_a_real_expand")


def test_invalid_per_page_raises_value_error():
    fake_client = FakeApiClient()
    automation_cases = AutomationCases(fake_client)

    with pytest.raises(ValueError, match="per_page must be one of"):
        automation_cases.get_project_automation_cases(5, per_page=10)

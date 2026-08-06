import pytest

from pyTestMoApi._modules._automation_links import (
    MAX_BULK_LINKS,
    MIN_BULK_LINKS,
    AutomationLinks,
)


class FakeApiClient:
    """Minimal stand-in for ApiClient that records post() calls instead of doing HTTP."""

    def __init__(self):
        self.calls = []

    def post(self, endpoint, json):
        self.calls.append((endpoint, json))


def make_module():
    api = FakeApiClient()
    return AutomationLinks(api), api


def test_single_link_endpoint_and_payload():
    module, api = make_module()
    module.create_automation_link(1, 42, 101)
    assert api.calls == [("/projects/1/automation-links", {"case_id": 42, "automation_case_id": 101})]


def test_bulk_single_pair():
    module, api = make_module()
    module.create_automation_links_bulk(1, [(42, 101)])
    assert api.calls == [
        ("/projects/1/automation-links/bulk", {"links": [{"case_id": 42, "automation_case_id": 101}]}),
    ]


def test_bulk_preserves_order():
    module, api = make_module()
    module.create_automation_links_bulk(7, [(42, 101), (43, 102), (100, 103)])
    endpoint, body = api.calls[0]
    assert endpoint == "/projects/7/automation-links/bulk"
    assert body == {
        "links": [
            {"case_id": 42, "automation_case_id": 101},
            {"case_id": 43, "automation_case_id": 102},
            {"case_id": 100, "automation_case_id": 103},
        ],
    }


def test_bulk_at_max_limit():
    module, api = make_module()
    module.create_automation_links_bulk(1, [(i, i + 1000) for i in range(MAX_BULK_LINKS)])
    assert len(api.calls[0][1]["links"]) == MAX_BULK_LINKS


def test_bulk_empty_raises_and_does_not_post():
    module, api = make_module()
    with pytest.raises(ValueError):
        module.create_automation_links_bulk(1, [])
    assert api.calls == []


def test_bulk_over_limit_raises_and_does_not_post():
    module, api = make_module()
    with pytest.raises(ValueError):
        module.create_automation_links_bulk(1, [(i, i + 1000) for i in range(MAX_BULK_LINKS + 1)])
    assert api.calls == []


def test_bulk_limits_constants():
    assert MIN_BULK_LINKS == 1
    assert MAX_BULK_LINKS == 500

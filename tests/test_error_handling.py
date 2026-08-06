import pytest

from requests import Response
from requests.exceptions import HTTPError

from pyTestMoApi._utils import ErrorHandling


def make_response(status_code: int, body: str, content_type: str = "application/json") -> Response:
    res = Response()
    res.status_code = status_code
    res._content = body.encode()
    res.headers["Content-Type"] = content_type
    return res


def test_error_response_is_falsy_but_details_still_extracted():
    # A requests.Response is falsy for error status codes (bool(res) == res.ok),
    # so the handler must not skip the body for exactly these responses.
    res = make_response(422, '{"message": "The automation case does not exist or was deleted."}')
    assert bool(res) is False

    with pytest.raises(HTTPError, match="The automation case does not exist or was deleted."):
        ErrorHandling(res.status_code, res).handler()


def test_plain_text_body_is_included_as_fallback():
    res = make_response(500, "Internal boom", content_type="text/plain")

    with pytest.raises(HTTPError, match="Internal boom"):
        ErrorHandling(res.status_code, res).handler()


def test_no_response_does_not_break_handler():
    with pytest.raises(HTTPError):
        ErrorHandling(404).handler()


def test_success_status_does_not_raise():
    res = make_response(204, "")
    # Should simply return without raising.
    assert ErrorHandling(res.status_code, res).handler() is None

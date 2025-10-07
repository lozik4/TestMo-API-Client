"""
Pagination utilities for Testmo API according to
https://docs.testmo.com/api/introduction/pagination-expands

This module provides a lightweight helper to parse RFC 5988 Link headers
returned by Testmo and to iterate through paginated resources.

We keep this non-invasive: existing client methods continue to return
response.json() data. Consumers who need advanced pagination can use
Pagination.from_response(res) and iterate using ApiClient.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse, parse_qsl, urlunparse, urlencode


def _parse_link_header(link_header: str) -> Dict[str, str]:
    """Parse an RFC 5988 Link header into a mapping of rel -> url.

    Example header:
    <https://example.testmo.net/api/v1/users?page=2&per_page=100>; rel="next",
    <https://example.testmo.net/api/v1/users?page=10&per_page=100>; rel="last"
    """
    links: Dict[str, str] = {}
    if not link_header:
        return links
    parts = [p.strip() for p in link_header.split(",") if p.strip()]
    for part in parts:
        if part.startswith("<") and ">" in part:
            url_part, rest = part.split(">", 1)
            url = url_part[1:]
            rest = rest.strip("; ")
            # extract rel="..."
            for seg in rest.split(";"):
                seg = seg.strip()
                if seg.startswith("rel="):
                    rel_val = seg.split("=", 1)[1].strip().strip('"')
                    links[rel_val] = url
    return links


def _with_query(url: str, updates: Dict[str, str]) -> str:
    """Return URL with updated query parameters."""
    parsed = urlparse(url)
    q = dict(parse_qsl(parsed.query, keep_blank_values=True))
    q.update({k: str(v) for k, v in updates.items()})
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(q), parsed.fragment))


@dataclass
class Pagination:
    """Holds pagination links extracted from a response.

    Attributes:
        first: URL of the first page if provided.
        prev: URL of the previous page if provided.
        next: URL of the next page if provided.
        last: URL of the last page if provided.
        per_page: The per_page value if it could be detected from the URL.
    """
    first: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None
    last: Optional[str] = None
    per_page: Optional[int] = None

    @classmethod
    def from_response(cls, response) -> "Pagination":
        """Create Pagination from a requests.Response object."""
        link_header = response.headers.get("Link", "")
        links = _parse_link_header(link_header)
        # Detect per_page from any link
        per_page = None
        for url in links.values():
            parsed = urlparse(url)
            q = dict(parse_qsl(parsed.query, keep_blank_values=True))
            if "per_page" in q:
                try:
                    per_page = int(q["per_page"])  # type: ignore[assignment]
                except ValueError:
                    pass
                break
        return cls(
            first=links.get("first"),
            prev=links.get("prev"),
            next=links.get("next"),
            last=links.get("last"),
            per_page=per_page,
        )

    def has_next(self) -> bool:
        return self.next is not None

    def set_per_page(self, url: str) -> str:
        """Ensure URL has the same per_page as this Pagination if set."""
        if self.per_page is None:
            return url
        return _with_query(url, {"per_page": str(self.per_page)})

    def iter_all(self, client, start_url: str) -> Iterable[dict]:
        """Iterate all items across pages.

        - client: instance of ApiClient (must have api_get returning a Response)
        - start_url: path (endpoint) relative to BASE_URL. E.g. "/users?page=1&per_page=100"

        Yields JSON arrays (list of items) or handles envelope with "items" key
        if Testmo returns objects with items.
        """
        # Normalize: ensure start_url includes page
        url = start_url
        if "page=" not in url:
            url = url + ("&" if "?" in url else "?") + "page=1"
        while True:
            res = client.api_get(url)
            data = res.json()
            # Testmo list endpoints typically return arrays; also support {items: [...]} shape
            items = data.get("items") if isinstance(data, dict) else data
            if items:
                yield items
            pg = Pagination.from_response(res)
            if not pg.next:
                break
            url = pg.next.replace(client.BASE_URL, "") if pg.next.startswith(client.BASE_URL) else pg.next


__all__ = ["Pagination", "_parse_link_header"]

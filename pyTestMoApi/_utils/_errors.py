from typing import Optional, Any

from requests import Response
from requests.exceptions import HTTPError


class ErrorHandling:
    """Simple HTTP error handler.

    Assumptions:
    - `self.status_messages` contains all well-known HTTP error codes returned by the server.
    - We must also gracefully handle any undeclared/unexpected errors.
    """

    def __init__(self, status_code: int, response: Optional[Response] = None):
        self.status_code = status_code
        self.response = response
        self.status_messages = {
            401: "Unauthorized: Invalid or missing Testmo API token",
            403: "Forbidden: Missing or insufficient permissions",
            404: "Not Found: Unknown or deleted objects in API requests",
            405: "Method Not Allowed: Using GET instead of POST or vice versa",
            422: "Invalid data: Invalid parameters or data in API requests",
            429: "Too Many Requests: Rate limit reached (please see below). Check Retry-After",
        }

    def _extract_extra_details(self) -> str:
        """Try to extract extra diagnostic info from the response (if provided)."""
        if not self.response:
            return ""

        # Retry-After hint for rate limiting
        retry_after = self.response.headers.get("Retry-After")

        details: list[str] = []

        # Prefer JSON payload if available
        try:
            data: Any = self.response.json()  # type: ignore[no-untyped-call]
            if isinstance(data, dict):
                for key in ("message", "error", "detail", "description"):
                    if key in data and data[key]:
                        details.append(str(data[key]))
                        break
                # If there is an 'errors' list/object, include a compact form
                if not details and "errors" in data and data["errors"]:
                    details.append(str(data["errors"]))
        except Exception:
            # Fallback to plain text body
            text = None
            try:
                text = self.response.text
            except Exception:
                text = None
            if text:
                details.append(text[:500])  # avoid excessively long messages

        if retry_after:
            details.append(f"Retry-After: {retry_after}")

        return (" | ".join(details)).strip()

    def handler(self):
        # No error for successful responses
        if self.status_code < 300:
            return

        # Known/declared errors
        if self.status_code in self.status_messages:
            base_msg = self.status_messages[self.status_code]
            extra = self._extract_extra_details()
            suffix = f" | {extra}" if extra else ""
            raise HTTPError(
                f"\n {self.status_code} {base_msg}{suffix} \n"
                f"More information: https://docs.testmo.com/api/introduction/error-handling"
            )

        # Undeclared/unexpected errors
        extra = self._extract_extra_details()
        suffix = f": {extra}" if extra else ""
        raise HTTPError(
            f"\n Unknown error: {self.status_code}{suffix} \n"
            f"More information: https://docs.testmo.com/api/introduction/error-handling"
        )

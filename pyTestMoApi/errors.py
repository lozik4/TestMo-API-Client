from requests.exceptions import HTTPError


class ErrorHandling:

    def __init__(self, status_code: int):
        self.status_code = status_code
        self.status_messages = {
            401: "Unauthorized: Invalid or missing Testmo API token",
            403: "Forbidden: Missing or insufficient permissions",
            404: "Not Found: Unknown or deleted objects in API requests",
            405: "Method Not Allowed: Using GET instead of POST or vice versa",
            422: "Invalid data: Invalid parameters or data in API requests",
            429: "Too Many Requests: Rate limit reached (please see below). Check Retry-After"
        }

    def handler(self):
        if self.status_code in self.status_messages:
            raise HTTPError(f"{self.status_code} {self.status_messages[self.status_code]}")
        if self.status_code >= 300:
            raise HTTPError(f"Unknown error: {self.status_code}")

# TestMo-API
TestMo API wrapper

[TestMo REST API Link](https://docs.testmo.com/api)


## Using the ErrorHandling class

The project includes a simple HTTP error handler that raises requests.exceptions.HTTPError for non-success HTTP responses and enriches the message with details from the server response (if available).

Basic usage with requests:

```python
import requests
from pyTestMoApi._utils._errors import ErrorHandling

# Example GET request
res = requests.get("https://example.testmo.net/api/v1/projects", headers={"Authorization": "Bearer <TOKEN>"}, timeout=15)

# Will do nothing if status_code < 300; otherwise raises HTTPError with details
ErrorHandling(res.status_code, response=res).handler()

# If we reach here, the request succeeded
print(res.json())
```

Catching errors:

```python
import requests
from requests.exceptions import HTTPError
from pyTestMoApi._utils._errors import ErrorHandling

try:
    res = requests.get("https://example.testmo.net/api/v1/projects", headers={"Authorization": "Bearer <TOKEN>"}, timeout=15)
    ErrorHandling(res.status_code, response=res).handler()
except HTTPError as e:
    # e will include status code, a friendly message for known errors (401/403/404/405/422/429),
    # any message/detail sent by the server, and a link to Testmo docs.
    print(f"Request failed: {e}")
```

Notes:
- For known status codes (401, 403, 404, 405, 422, 429), the handler prints a friendly message and includes details such as JSON message/detail or Retry-After headers when rate-limited.
- For any other >= 300 status code, the handler raises an HTTPError with an "Unknown error" message and includes any details it can parse from the response.
- If you don’t pass the response object, the error will still be raised for non-success codes, just without extra parsed details.

### Using together with ApiClient

The included ApiClient wraps GET/POST requests to the Testmo API. After each request it calls the error handler. Example:

```python
from pyTestMoApi.api_client import ApiClient

client = ApiClient(token="<TOKEN>", instance="example")  # or set TESTMO_TOKEN and TESTMO_INSTANCE env vars

# GET projects
res = client.api_get("/projects")
print(res.json())

# POST example
payload = {"name": "My Project"}
res = client.api_post("/projects", json=payload)
print(res.json())
```

```uv
uv sync           # to create/update the environment
uv sync --all-extras --group dev  # to create/update the environment with extras
uv build          # to build the package
uv pip install .  # to install the local package
```
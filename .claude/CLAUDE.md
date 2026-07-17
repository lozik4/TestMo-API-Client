# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python wrapper library for the [TestMo REST API](https://docs.testmo.com/api). PyPI package name: `TestMoApiClient`, imported as `pyTestMoApi`. Requires Python >= 3.13.

This is a **public SDK published to PyPI** — it's consumed as a dependency by third parties, not just used internally. Treat the public surface (`TestMoClient` and the `_modules/` API classes) with the care of a library, not an app: avoid casual breaking changes to method signatures.

## Development Commands

```bash
uv sync --group dev          # Install dependencies + dev tools (pytest==9.1.1, ruff==0.15.22, pinned exact versions)
uv run pytest                # Run all tests
uv run pytest tests/test_build_date.py  # Run a single test file
uv run pytest -k "test_name" # Run a specific test by name
uv run ruff check .          # Lint
uv run ruff format .         # Format
uv build                     # Build the package
```

There is no CI configured (no `.github/workflows`) — linting, tests, and build are run manually.

## Architecture

**Entry point:** `TestMoClient` in `pyTestMoApi/__init__.py` — instantiated with a token and instance name (or via `TESTMO_TOKEN` / `TESTMO_INSTANCE` env vars). Exposes API modules as properties (e.g., `client.users`, `client.cases`, `client.projects`).

**`_utils/` — shared infrastructure:**
- `ApiClient` (`_api.py`): HTTP client wrapping `requests` with GET/POST/PATCH/DELETE. Constructs base URL as `https://{instance}.testmo.net/api/v1`. Every request passes through `ErrorHandling`.
- `ErrorHandling` (`_errors.py`): inspects the response status code and always raises `requests.exceptions.HTTPError` (no custom exception classes) — with a friendly message for known codes (401/403/404/405/422/429), or "Unknown error" otherwise. Extracts extra detail from JSON body fields (`message`/`error`/`detail`/`description`/`errors`) or raw text, plus `Retry-After` if present.
- `BoundApi` (`_bound_api.py`): Base class for all API modules; holds a reference to `ApiClient` via `self._api`.
- `Pagination` (`_paginations.py`): Dataclass for pagination with RFC 5988 Link header parsing. `per_page` must be one of: 15, 25, 50, 100.
- `build_filters` / `build_date` (`_utils.py`): Query string helpers. `build_date` normalizes date inputs to ISO 8601 UTC with `Z` suffix.
- `_custom_typing.py`: Shared type aliases (`DateIso`, `Order`, `BoolFilter`).

**`_modules/` — one file per API resource:** Each module class extends `BoundApi` and implements methods that map to TestMo API endpoints. Methods build URLs with pagination/expands/filters and return parsed JSON.

## Adding new API endpoints

Every new endpoint requires all three of the following (see the `/new-endpoint` skill for the full checklist):
1. A method on the relevant `_modules/` class.
2. A Google-style docstring that links to the corresponding page in the [official TestMo API docs](https://docs.testmo.com/api).
3. A unit test in `tests/`.

## Linting/Formatting (Ruff)

Configured in `pyproject.toml`. Key settings:
- Line length: 120, indent: 4 spaces, target: py313
- `preview = true` is enabled for both the linter and formatter — ruff preview-mode rules are in effect
- Lint rules: E, F, C90, I, COM, ISC, PT, Q, ARG, PLC, PLE, A — with `F403, F405, E266, PT013, A001` ignored
- `pydocstyle` convention: **Google style** — docstrings must follow this format
- Max complexity (mccabe): 18, max statements: 80, max function args: 10, max positional args: 3
- `tests/`, `__init__.py`, and `docker/` are excluded from linting

## Testing

- Plain `pytest`, no HTTP mocking libraries (no `responses`/`httpx`/`VCR`/`pytest-mock`) — tests exercise pure utility functions directly (see `tests/test_build_date.py`).
- Test files must match pytest's default `test_*.py` discovery pattern.

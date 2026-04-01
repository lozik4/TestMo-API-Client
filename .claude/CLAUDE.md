# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python wrapper library for the [TestMo REST API](https://docs.testmo.com/api). Package name: `pyTestMoApi`. Requires Python >= 3.13.

## Development Commands

```bash
uv sync --group dev          # Install dependencies + dev tools (pytest, ruff)
uv run pytest                # Run all tests
uv run pytest tests/test_build_date.py  # Run a single test file
uv run pytest -k "test_name" # Run a specific test by name
uv run ruff check .          # Lint
uv run ruff format .         # Format
uv build                     # Build the package
```

## Architecture

**Entry point:** `TestMoClient` in `pyTestMoApi/__init__.py` — instantiated with a token and instance name (or via `TESTMO_TOKEN` / `TESTMO_INSTANCE` env vars). Exposes API modules as properties (e.g., `client.users`, `client.cases`, `client.projects`).

**`_utils/` — shared infrastructure:**
- `ApiClient` (`_api.py`): HTTP client wrapping `requests` with GET/POST/PATCH/DELETE. Constructs base URL as `https://{instance}.testmo.net/api/v1`. Every request passes through `ErrorHandling`.
- `BoundApi` (`_bound_api.py`): Base class for all API modules; holds a reference to `ApiClient` via `self._api`.
- `Pagination` (`_paginations.py`): Dataclass for pagination with RFC 5988 Link header parsing. `per_page` must be one of: 15, 25, 50, 100.
- `build_filters` / `build_date` (`_utils.py`): Query string helpers. `build_date` normalizes date inputs to ISO 8601 UTC with `Z` suffix.
- `_custom_typing.py`: Shared type aliases (`DateIso`, `Order`, `BoolFilter`).

**`_modules/` — one file per API resource:** Each module class extends `BoundApi` and implements methods that map to TestMo API endpoints. Methods build URLs with pagination/expands/filters and return parsed JSON.

## Linting/Formatting (Ruff)

Configured in `pyproject.toml`. Key settings:
- Line length: 120, indent: 4 spaces, target: py313
- Lint rules: E, F, C90, I, COM, ISC, PT, Q, ARG, PLC, PLE, A
- `tests/`, `__init__.py`, and `docker/` are excluded from linting
- Max function args: 10, max positional args: 3
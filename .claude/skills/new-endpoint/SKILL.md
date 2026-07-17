---
name: new-endpoint
description: Checklist for adding a new TestMo API endpoint to pyTestMoApi — use whenever implementing a method that calls a new or existing TestMo REST API endpoint.
---

This is a public SDK published to PyPI (`TestMoApiClient`). Every new endpoint must ship with all three of the following — do not consider the task done until each is present.

## 1. Implement the method

- Add the method to the relevant class in `pyTestMoApi/_modules/` (one file per resource, e.g. `_cases.py`, `_runs.py`, `_projects.py`). If no existing file matches the resource, create a new one following the same pattern (extend `BoundApi`, use `self._api` for HTTP calls).
- Reuse existing helpers instead of hand-rolling query strings: `build_filters` / `build_date` from `_utils/_utils.py`, `Pagination` from `_utils/_paginations.py` (`per_page` must be one of 15, 25, 50, 100), and shared type aliases from `_utils/_custom_typing.py` (`DateIso`, `Order`, `BoolFilter`).
- Respect the ruff constraints already enforced on this file: max 10 function args, max 3 positional args, max complexity 18.
- Do not add custom exception handling — `ApiClient` already routes every response through `ErrorHandling`, which raises `requests.exceptions.HTTPError` on failure.

## 2. Write a Google-style docstring with an official doc reference

- Docstrings must follow the Google convention (ruff's `pydocstyle` is configured for it).
- Include a link to the corresponding page in the [official TestMo API docs](https://docs.testmo.com/api) — find the exact endpoint page and cite it, don't just link the docs root.
- Document parameters, return value, and any raised exceptions relevant to the caller.

## 3. Add a unit test

- Add a test in `tests/`, named `test_*.py` so pytest's default discovery picks it up (note: `tests_users.py` in this repo is a naming mistake — don't copy that pattern).
- Follow the existing style (see `tests/test_build_date.py`): no HTTP mocking libraries — test pure logic (URL/query construction, filter building, pagination handling) directly rather than mocking `requests`.
- Run `uv run pytest` before considering the endpoint complete.

## Before finishing

- `uv run ruff check .` and `uv run ruff format .` — must pass clean.
- `uv run pytest` — must pass.

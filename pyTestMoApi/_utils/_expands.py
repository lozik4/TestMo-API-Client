"""
Expands utilities for Testmo API according to
https://docs.testmo.com/api/introduction/pagination-expands

Provides helpers to validate and build the expands query string for resources.
This complements the simple expands_validator already present in utils.py.
"""

from __future__ import annotations

from typing import Iterable, Sequence


def build_expands(expands: Sequence[str] | str, allowed: Iterable[str], *, ampersand: bool = True) -> str:
    """Validate and build the expands query string.

    - expands: sequence of expansions or comma-separated string.
    - allowed: iterable with allowed expansion names for the resource.
    - ampersand: if True, use '&expands=' instead of '?expands='.

    Returns a string starting with '&expands=' or an empty string if no expands.
    Raises ValueError if any expansion is not allowed.
    """
    allowed_set = set(allowed)
    if isinstance(expands, str):
        expands = [e for e in expands.split(",") if e]
    invalid = [e for e in expands if e not in allowed_set]
    if invalid:
        allowed_list = ", ".join(f"'{i}'" for i in allowed)
        raise ValueError(f"expands must be: {allowed_list}")
    if not expands:
        return ""

    return "&expands=" + ",".join(expands) if ampersand else "?expands=" + ",".join(expands)


__all__ = ["build_expands"]

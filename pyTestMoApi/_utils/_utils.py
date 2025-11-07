from datetime import date as _date
from datetime import datetime as _dt
from datetime import time as _time
from datetime import timezone as _tz
from urllib.parse import urlencode


def build_filters(filters: dict[str, str | int]) -> str:
    """Build query string for filters, skipping empty and None values.

    - filters: mapping of query parameter names to values (str or int).
    - Removes keys with value None or empty/blank strings.
    - Integers are kept (including 0). Other types are converted to str.

    Returns a string starting with '&' or an empty string if no filters remain.
    """
    if not filters:
        return ""

    cleaned: dict[str, str] = {}
    for key, value in filters.items():
        if value is None:
            continue
        if isinstance(value, str):
            if value.strip() == "":
                continue
            cleaned[key] = value
        else:
            cleaned[key] = str(value)

    if not cleaned:
        return ""

    return "&" + urlencode(cleaned)


def build_date(value) -> str:
    """Normalize a date/time input to ISO 8601 in UTC.

    Accepts:
    - datetime: aware is converted to UTC; naive is interpreted as local time and converted to UTC.
    - date: treated as start of day 00:00:00 UTC.
    - str: ISO 8601 date or datetime (with optional timezone). Supports trailing 'Z'.
    - None or blank string: returns empty string.

    Returns an ISO 8601 string in UTC with 'Z' suffix, without microseconds.
    Raises ValueError for unsupported/invalid formats.
    """
    # None or empty/blank string -> empty output (similar to build_filters behavior)
    if value is None:
        return ""
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return ""
        # If it's a plain date (YYYY-MM-DD), treat as start of day UTC (do NOT interpret as local time)
        if len(s) == 10 and s[4] == "-" and s[7] == "-":
            try:
                d = _date.fromisoformat(s)
            except ValueError as e:
                raise ValueError(
                    "Invalid date string. Use ISO 8601, e.g. '2025-11-06', "
                    "'2025-11-06T14:30:00Z', or '2025-11-06T14:30:00+02:00'.",
                ) from e
            dt = _dt.combine(d, _time(0, 0, 0), tzinfo=_tz.utc)
        else:
            # Normalize 'Z' to "+00:00" for fromisoformat compatibility
            s_norm = s[:-1] + "+00:00" if s.endswith("Z") else s
            # Try parse as datetime first
            try:
                dt = _dt.fromisoformat(s_norm)
                if dt.tzinfo is None:
                    # Interpret naive as local time, then convert to UTC
                    dt = dt.astimezone(_tz.utc)
                else:
                    dt = dt.astimezone(_tz.utc)
            except ValueError as e:
                raise ValueError(
                    "Invalid date string. Use ISO 8601, e.g. '2025-11-06', "
                    "'2025-11-06T14:30:00Z', or '2025-11-06T14:30:00+02:00'.",
                ) from e
    elif isinstance(value, _dt):
        dt = value.astimezone(_tz.utc) if value.tzinfo is not None else value.astimezone(_tz.utc)
    elif isinstance(value, _date):
        # Only date (not datetime) -> start of day in UTC
        dt = _dt.combine(value, _time(0, 0, 0), tzinfo=_tz.utc)
    else:
        raise TypeError("build_date accepts datetime, date, str, or None")

    # Drop microseconds and format with 'Z'
    dt = dt.replace(microsecond=0)
    iso = dt.isoformat()
    if iso.endswith("+00:00"):
        iso = iso[:-6] + "Z"
    return iso


__all__ = ["build_filters", "build_date"]

from datetime import date, datetime, timedelta, timezone

import pytest

from pyTestMoApi._utils import build_date


def parse_iso_utc(s: str) -> datetime:
    assert s.endswith("Z"), f"Output must end with 'Z': {s}"
    # Convert trailing Z to +00:00 for fromisoformat
    return datetime.fromisoformat(s[:-1] + "+00:00")


def test_none_and_blank_return_empty_string():
    assert build_date(None) == ""
    assert build_date("") == ""
    assert build_date("   ") == ""


def test_date_object_to_start_of_day_utc():
    d = date(2025, 11, 6)
    out = build_date(d)
    assert out == "2025-11-06T00:00:00Z"


def test_datetime_aware_utc_kept_and_microseconds_dropped():
    dt = datetime(2025, 11, 6, 15, 30, 45, 123456, tzinfo=timezone.utc)
    out = build_date(dt)
    assert out == "2025-11-06T15:30:45Z"


def test_datetime_aware_offset_converted_to_utc():
    # 15:30:00 at +02:00 should be 13:30:00Z
    tz_plus2 = timezone(timedelta(hours=2))
    dt = datetime(2025, 11, 6, 15, 30, 0, tzinfo=tz_plus2)
    out = build_date(dt)
    assert out == "2025-11-06T13:30:00Z"


def test_naive_datetime_is_treated_as_local_then_converted_to_utc():
    # Build a naive local time and compute expected using the system local tz
    naive = datetime(2025, 11, 6, 8, 0, 0)
    local_tz = datetime.now().astimezone().tzinfo
    # Interpret naive as local time
    local_dt = naive.replace(tzinfo=local_tz)
    expected_utc = local_dt.astimezone(timezone.utc).replace(microsecond=0)
    out = build_date(naive)
    got = parse_iso_utc(out)
    assert got == expected_utc


def test_string_date_only():
    out = build_date("2025-11-06")
    assert out == "2025-11-06T00:00:00Z"


def test_string_datetime_with_z():
    out = build_date("2025-11-06T15:30:00Z")
    assert out == "2025-11-06T15:30:00Z"


def test_string_datetime_with_offset():
    out = build_date("2025-11-06T15:30:00+02:00")
    assert out == "2025-11-06T13:30:00Z"


def test_invalid_string_raises_value_error():
    with pytest.raises(ValueError):
        build_date("06-11-2025")  # non-ISO format
    with pytest.raises(ValueError):
        build_date("2025/11/06")


def test_invalid_type_raises_type_error():
    with pytest.raises(TypeError):
        build_date(123.456)  # unsupported type

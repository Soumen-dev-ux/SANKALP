from app.services.data_ingestion_service import parse_datetime


def test_parse_datetime():
    value = parse_datetime("2026-01-15T00:00:00")

    assert value is not None
    assert value.year == 2026
    assert value.month == 1
    assert value.day == 15


def test_parse_none_datetime():
    assert parse_datetime(None) is None
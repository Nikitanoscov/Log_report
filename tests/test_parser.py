import pytest
from parser import RequestLogParser

@pytest.mark.parametrize("line, expected", [
    (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
        {"level": "INFO", "handler": "/api/v1/reviews/"}
    ),
    (
        "2025-03-28 12:44:46,000 INFO django.request: POST /api/v1/orders/ 201 Created [192.168.1.60]",
        {"level": "INFO", "handler": "/api/v1/orders/"}
    ),
    (
        "2025-03-28 12:07:59,000 ERROR django.request: Internal Server Error: /api/v1/support/ [192.168.1.45]",
        {"level": "ERROR", "handler": "/api/v1/support/"}
    ),
    (
        "2025-03-28 12:01:42,000 WARNING django.request: GET /api/v1/debug/ 400 Bad Request [192.168.1.70]",
        {"level": "WARNING", "handler": "/api/v1/debug/"}
    )
])
def test_request_log_parser_valid(line: str, expected: dict):
    assert RequestLogParser.parse_line(line) == expected


@pytest.mark.parametrize("line", [
    "2025-03-28 12:25:45,000 DEBUG django.db.backends: (0.41) SELECT * FROM 'products'",
    "2025-03-28 12:44:46,000 django.request: GET /api/v1/reviews/",
    "2025-03-28 12:44:46,000 INFO django.request: GET 204 OK [192.168.1.59]",
    "",
    "Hello, world!"
])
def test_request_log_parser_invalid(line: str):
    assert RequestLogParser.parse_line(line) is None
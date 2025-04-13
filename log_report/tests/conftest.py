import pytest
import tempfile
import os

@pytest.fixture
def sample_log_file():
    content = """
2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]
2025-03-28 12:07:59,000 ERROR django.request: Internal Server Error: /api/v1/support/ [192.168.1.45]
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)
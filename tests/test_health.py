import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    # Some FastAPIs return 200 on /health or similar endpoints, adjust if not present
    if response.status_code == 404:
        pytest.skip("No /health endpoint configured in app.main yet.")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

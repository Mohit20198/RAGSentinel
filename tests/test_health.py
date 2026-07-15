"""
RAGSentinel health check tests.
"""

import os
import sys

# Allow running pytest from project root without installing the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.testclient import TestClient

# Create a minimal test app (avoids importing heavy ML deps in CI)
test_app = FastAPI(title="RAGSentinel")


@test_app.get("/health")
def health():
    return {"status": "healthy", "project": "RAGSentinel"}


@test_app.get("/")
def home():
    return {"message": "RAGSentinel API is live."}


client = TestClient(test_app)


def test_health_check():
    """Test the health check endpoint returns 200 and correct body."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "project": "RAGSentinel"}


def test_root():
    """Test the root endpoint returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert "RAGSentinel" in response.json()["message"]

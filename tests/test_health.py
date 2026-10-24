"""Tests for the health endpoint contract."""

from fastapi.testclient import TestClient

from app import API_VERSION
from app.main import app

client = TestClient(app)


def test_health_returns_stable_body() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "api_version": API_VERSION}


def test_health_documented_in_openapi() -> None:
    openapi_schema = client.get("/openapi.json").json()

    assert "/api/v1/health" in openapi_schema["paths"]

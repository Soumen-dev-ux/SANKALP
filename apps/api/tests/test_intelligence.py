import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies.auth import get_current_user
from app.models.user import User

client = TestClient(app)


def test_intelligence_anonymous_access_rejected():
    protected_urls = [
        "/api/v1/intelligence/regions/1",
        "/api/v1/intelligence/regions/compare",
        "/api/v1/intelligence/regions/1/trends",
        "/api/v1/intelligence/regions/1/infrastructure",
        "/api/v1/intelligence/regions/1/projects",
        "/api/v1/intelligence/regions/1/hotspots",
        "/api/v1/intelligence/regions/1/need-vs-development",
        "/api/v1/intelligence/export",
    ]
    for url in protected_urls:
        res = client.get(url)
        assert res.status_code == 401, f"Expected 401 for anonymous access to {url}, got {res.status_code}"


def test_intelligence_authenticated_analyst_access():
    def mock_analyst():
        return User(id=1, email="analyst@example.com", role="analyst", is_active=True)

    app.dependency_overrides[get_current_user] = mock_analyst
    try:
        res = client.get("/api/v1/intelligence/regions/1")
        assert res.status_code in [200, 404]

        res_compare = client.get("/api/v1/intelligence/regions/compare")
        assert res_compare.status_code == 200

        res_trends = client.get("/api/v1/intelligence/regions/1/trends")
        assert res_trends.status_code in [200, 404]

        res_export = client.get("/api/v1/intelligence/export?format=json")
        assert res_export.status_code == 200
        assert "application/json" in res_export.headers.get("content-type", "")

        res_csv = client.get("/api/v1/intelligence/export?format=csv")
        assert res_csv.status_code == 200
        assert "text/csv" in res_csv.headers.get("content-type", "")
    finally:
        app.dependency_overrides.clear()

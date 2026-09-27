import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies.auth import get_current_user
from app.models.user import User

client = TestClient(app)


def test_anonymous_access_to_protected_endpoints_rejected():
    protected_urls = [
        "/api/v1/demand/regions/1",
        "/api/v1/infrastructure-gap/regions/1",
        "/api/v1/development-insights/regions/1",
        "/api/v1/clusters/regions/1",
        "/api/v1/reviews/pending",
        "/api/v1/admin/access-check",
    ]

    for url in protected_urls:
        response = client.get(url)
        assert response.status_code == 401, f"Expected 401 for anonymous access to {url}, got {response.status_code}"


def test_rbac_role_authorizations():
    # Analyst trying to access admin-only endpoint -> 403
    def mock_analyst():
        return User(id=1, email="analyst@example.com", role="analyst", is_active=True)

    app.dependency_overrides[get_current_user] = mock_analyst
    try:
        res = client.get("/api/v1/admin/access-check")
        assert res.status_code == 403
    finally:
        app.dependency_overrides.clear()

    # Reviewer trying to access admin-only endpoint -> 403
    def mock_reviewer():
        return User(id=2, email="reviewer@example.com", role="reviewer", is_active=True)

    app.dependency_overrides[get_current_user] = mock_reviewer
    try:
        res = client.get("/api/v1/admin/access-check")
        assert res.status_code == 403
    finally:
        app.dependency_overrides.clear()

    # Admin accessing admin endpoint -> 200
    def mock_admin():
        return User(id=3, email="admin@example.com", role="admin", is_active=True)

    app.dependency_overrides[get_current_user] = mock_admin
    try:
        res = client.get("/api/v1/admin/access-check")
        assert res.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_public_citizen_endpoints_remain_public():
    public_urls = [
        "/",
        "/api/v1/health/",
        "/api/v1/regions",
    ]

    for url in public_urls:
        response = client.get(url)
        assert response.status_code == 200, f"Expected 200 for public url {url}, got {response.status_code}"

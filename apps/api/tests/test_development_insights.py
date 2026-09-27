from app.main import app
from app.api.dependencies.auth import get_current_user
from app.models.user import User


def mock_get_current_user():
    return User(
        id=1,
        email="analyst@example.com",
        role="analyst",
        is_active=True,
    )


def test_development_insights_region_not_found(client):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    try:
        response = client.get(
            "/api/v1/development-insights/regions/999999"
        )
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()


def test_development_insights_region(client):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    try:
        response = client.get(
            "/api/v1/development-insights/regions/1"
        )
        assert response.status_code == 200

        data = response.json()

        assert data["region_id"] == 1
        assert data["region_name"]
        assert "insights" in data
        assert isinstance(data["insights"], list)
    finally:
        app.dependency_overrides.clear()
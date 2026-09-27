from app.main import app
from app.api.dependencies.auth import get_current_user
from app.models.user import User


def mock_get_current_user():
    return User(id=1, email="admin@example.com", role="admin", is_active=True)


def test_infrastructure_capacity_validation(client):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    try:
        response = client.post(
            "/api/v1/infrastructure",
            json={
                "region_id": 1,
                "category": "Healthcare",
                "infrastructure_type": "Primary Health Centre",
                "capacity": -10,
            },
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()

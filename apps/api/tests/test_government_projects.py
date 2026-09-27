from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies.auth import get_current_user
from app.models.user import User


client = TestClient(app)


def mock_get_current_user():
    return User(id=1, email="admin@example.com", role="admin", is_active=True)


def test_invalid_project_status():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    try:
        response = client.post(
            "/api/v1/government-projects",
            json={
                "region_id": 1,
                "name": "Demo Project",
                "category": "Healthcare",
                "status": "Unknown",
            },
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_negative_budget_rejected():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    try:
        response = client.post(
            "/api/v1/government-projects",
            json={
                "region_id": 1,
                "name": "Demo Project",
                "category": "Healthcare",
                "status": "Planned",
                "budget": -100,
            },
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_invalid_project_coordinates():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    try:
        response = client.post(
            "/api/v1/government-projects",
            json={
                "region_id": 1,
                "name": "Demo Project",
                "category": "Healthcare",
                "status": "Planned",
                "latitude": 100,
            },
        )
        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()
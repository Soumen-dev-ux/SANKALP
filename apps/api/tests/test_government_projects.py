from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_project_status():

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


def test_negative_budget_rejected():

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


def test_invalid_project_coordinates():

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
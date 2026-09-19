from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_regions():
    response = client.get("/api/v1/regions")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_region_not_found():
    response = client.get(
        "/api/v1/regions/999999"
    )

    assert response.status_code == 404


def test_region_summary_not_found():
    response = client.get(
        "/api/v1/regions/999999/summary"
    )

    assert response.status_code == 404
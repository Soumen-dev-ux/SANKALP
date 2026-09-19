from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_request_requires_text():
    response = client.post(
        "/api/v1/requests",
        json={}
    )

    assert response.status_code == 422


def test_request_text_validation():
    response = client.post(
        "/api/v1/requests",
        json={
            "raw_text": "Hi"
        }
    )

    assert response.status_code == 422

def test_invalid_latitude():

    response = client.post(
        "/api/v1/requests",
        json={
            "raw_text": "There is no drinking water here",
            "language": "en",
            "latitude": 100,
            "longitude": 88,
        },
    )

    assert response.status_code == 422


def test_invalid_longitude():

    response = client.post(
        "/api/v1/requests",
        json={
            "raw_text": "There is no drinking water here",
            "language": "en",
            "latitude": 22,
            "longitude": 200,
        },
    )

    assert response.status_code == 422

def test_request_not_found():

    response = client.get(
        "/api/v1/requests/999999"
    )

    assert response.status_code == 404
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_english_water_request():

    response = client.post(
        "/api/v1/requests/analyze",
        json={
            "text": "There is no drinking water in our area"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["language"] == "en"
    assert data["category"] == "Water & Sanitation"
    assert data["issue"] == "Drinking Water"


def test_analyze_bengali_request():

    response = client.post(
        "/api/v1/requests/analyze",
        json={
            "text": "আমাদের এলাকায় পানীয় জলের সমস্যা হচ্ছে"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["language"] == "bn"
    assert data["category"] == "Water & Sanitation"


def test_analyze_hindi_request():

    response = client.post(
        "/api/v1/requests/analyze",
        json={
            "text": "हमारे इलाके में पीने के पानी की समस्या है"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["language"] == "hi"
    assert data["category"] == "Water & Sanitation"


def test_analyze_requires_text():

    response = client.post(
        "/api/v1/requests/analyze",
        json={}
    )

    assert response.status_code == 422
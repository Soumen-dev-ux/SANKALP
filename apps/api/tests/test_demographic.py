from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_demographic_population_validation():
    response = client.post(
        "/api/v1/demographics",
        json={
            "region_id" : 1,
            "population" : -100
        }
    )
    assert response.status_code == 422
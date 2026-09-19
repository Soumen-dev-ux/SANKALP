def test_demand_region_not_found(client):
    response = client.get("/api/v1/demand/regions/999999")

    assert response.status_code == 404

def test_demand_region_without_requests(client):
    response = client.get(
        "/api/v1/demand/regions/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["region_id"] == 1
    assert "total_requests" in data
    assert "categories" in data
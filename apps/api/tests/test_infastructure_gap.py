def test_infrastructure_gap_region_not_found(client):
    response = client.get(
        "/api/v1/infrastructure-gap/regions/999999"
    )

    assert response.status_code == 404


def test_infrastructure_gap_region(client):
    response = client.get(
        "/api/v1/infrastructure-gap/regions/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["region_id"] == 1
    assert "total_requests" in data
    assert "categories" in data
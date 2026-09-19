def test_development_insights_region_not_found(client):
    response = client.get(
        "/api/v1/development-insights/regions/999999"
    )

    assert response.status_code == 404


def test_development_insights_region(client):
    response = client.get(
        "/api/v1/development-insights/regions/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["region_id"] == 1
    assert data["region_name"]
    assert "insights" in data
    assert isinstance(data["insights"], list)
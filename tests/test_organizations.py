import pytest
from datetime import datetime , timezone
# test_case 01 : create organization success
@pytest.mark.asyncio
async def test_create_organization_success(client):
    org_data = {
        "name": "Test Organization",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.post("/api/v1/orgs/create", json=org_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Organization created successfully"
    assert "org_id" in response_data
# test_case 02 : create organization failure (duplicate name)
@pytest.mark.asyncio
async def test_create_organization_duplicate_name(client, db_session):
    org_data = {
        "name": "Duplicate Org",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response1 = await client.post("/api/v1/orgs/create", json=org_data)
    assert response1.status_code == 200

    response2 = await client.post("/api/v1/orgs/create", json=org_data)
    assert response2.status_code == 400
    assert response2.json()["message"]
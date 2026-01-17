import pytest
import pytest_asyncio
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

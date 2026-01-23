import  pytest

# case 01 : get report success 
@pytest.mark.asyncio
async def test_get_report_success_admin(client, admin_auth_headers , test_project):
    response = await client.get(f"/api/v1/reports/project/{test_project.project_id}", headers=admin_auth_headers)
    if response.status_code == 200:
        print("Response content:", response)
    
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["stats"]  is not None
    assert data["overdue_tasks"] is not None
# case 02 : get report failure ( unauthorized user)
@pytest.mark.asyncio
async def test_get_report_unauthorized_user(client, member_auth_headers , test_project):
    response = await client.get(f"/api/v1/reports/project/{test_project.project_id}", headers=member_auth_headers)
    assert response.status_code == 403
    data = response.json()
    assert data["message"]
#case 03 : get  report  not found project id 
@pytest.mark.asyncio
async def test_get_report_project_not_found(client, admin_auth_headers):
    fake_project_id = 999999
    response = await client.get(f"/api/v1/reports/project/{fake_project_id}", headers=admin_auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["message"] == "Project not found"
import pytest
from datetime import datetime , timezone
# case 01 : create project success ( with admin user )
@pytest.mark.asyncio
async def test_create_project_success(client, test_org , admin_auth_headers):
    project_data = {
        "name": "Test Project",
        "description": "This is a test project",
        "org_id": test_org.org_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.post("/api/v1/projects/create", json=project_data , headers= admin_auth_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data
# case 02 : create project failure ( with member user )
@pytest.mark.asyncio
async def test_create_project_failure_member_role(client, test_org , member_auth_headers):
    project_data = {
        "name": "Test Project Fail",
        "description": "This is a test project that should fail",
        "org_id": test_org.org_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.post("/api/v1/projects/create", json=project_data , headers= member_auth_headers)
    assert response.status_code == 403
    response_data = response.json()
    assert response_data["message"] 
# case 03 : create success ( with manager user )
@pytest.mark.asyncio
async def test_create_project_success_manager_role(client, test_org , manager_auth_headers):
    project_data = {
        "name": "Test Project Manager",
        "description": "This is a test project created by manager",
        "org_id": test_org.org_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.post("/api/v1/projects/create", json=project_data , headers= manager_auth_headers)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Project created successfully"
    assert "project_id" in response_data
    

# case 04 : add member to project success ( with admin user )
@pytest.mark.asyncio
async def test_add_member_to_project_success_admin(client, test_org, test_user_member, admin_auth_headers, db_session):
    project_data = {
        "name": "Project for Adding Member",
        "description": "Project to test adding member",
        "org_id": test_org.org_id,
    }
    create_response = await client.post("/api/v1/projects/create", json=project_data , headers= admin_auth_headers)
    assert create_response.status_code == 200
    project_id = create_response.json()["project_id"]

    member_data = {
        "user_id": test_user_member.user_id,
        "role": "member",  
        "email": test_user_member.email,
    }
    add_member_response = await client.post(f"/api/v1/projects/{project_id}/add-member", json=member_data , headers= admin_auth_headers)
    assert add_member_response.status_code == 200
    response_data = add_member_response.json()
    assert response_data["user_id"] == test_user_member.user_id

# case 05 : add member to project failure ( with member user )
@pytest.mark.asyncio
async def test_add_member_to_project_failure_member_role(client, test_org, test_user_member, member_auth_headers, db_session):
    project_data = {
        "name": "Project for Adding Member Fail",
        "description": "Project to test adding member fail",
        "org_id": test_org.org_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    create_response = await client.post("/api/v1/projects/create", json=project_data , headers= member_auth_headers)
    assert create_response.status_code == 403  


# case 06 : create user member not in org to project failure
@pytest.mark.asyncio
async def test_add_member_to_project_failure_user_not_in_org(client, test_org, admin_auth_headers, db_session):
    project_data = {
        "name": "Project for Adding Invalid Member",
        "description": "Project to test adding invalid member",
        "org_id": test_org.org_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    create_response = await client.post("/api/v1/projects/create", json=project_data , headers= admin_auth_headers)
    assert create_response.status_code == 200
    project_id = create_response.json()["project_id"]

    invalid_member_data = {
        "user_id": 99999,  
        "role": "member",
        "email": "9999member@gmail.com"
    }
    add_member_response = await client.post(f"/api/v1/projects/{project_id}/add-member", json=invalid_member_data , headers= admin_auth_headers)
    assert add_member_response.status_code == 400
    response_data = add_member_response.json()
    assert response_data["message"] 
    
# case 07 : create project organization does not exist
@pytest.mark.asyncio
async def test_create_project_failure_org_not_exist(client, admin_auth_headers):
    project_data = {
        "name": "Test Project Invalid Org",
        "description": "This is a test project with invalid organization",
        "org_id": 99999,  
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    response = await client.post("/api/v1/projects/create", json=project_data , headers= admin_auth_headers)
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["message"]

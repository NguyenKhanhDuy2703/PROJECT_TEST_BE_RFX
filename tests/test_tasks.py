import pytest
from datetime import datetime , timezone , timedelta
from app.schemas.task_schema import PriorityEnum , TaskStatus
from app.core.security import decode_access_token
# case 01 : create task with project success ( with member user )
@pytest.mark.asyncio
async def test_create_task_success_admin(client , member_auth_headers, test_user_member , test_project_member):
    
    task_data = {
        "title": "Test Task member",
        "description": "This is a test task created by member",
        "project_id": test_project_member.project_id,
        "priority": "HIGH",
        "status": "TO_DO",
        "due_date": (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)).isoformat(),
        "assigned_to": test_user_member.user_id,
    }
    response = await client.post("/api/v1/tasks/create", json=task_data , headers= member_auth_headers)
    response_data = response.json()
    assert "task_id" in response_data
# case 02 : update task status success
@pytest.mark.asyncio
async def test_update_task_success(client, member_auth_headers, test_user_member, test_project_member):
    task_data = {
        "title": "Task to Update",
        "description": "Will be updated soon",
        "project_id": test_project_member.project_id,
        "priority": "LOW", 
        "status": "TO_DO",
        "due_date": (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)).isoformat(),
        "assigned_to": test_user_member.user_id,
    }
    create_res = await client.post("/api/v1/tasks/create", json=task_data, headers=member_auth_headers)
    
    if create_res.status_code != 201:
        print(f"DEBUG SETUP FAIL: {create_res.json()}")
        
    assert create_res.status_code == 201
    task_id = create_res.json()["task_id"]

    update_data = {
        "status": "IN_PROGRESS", 
        "title": "Task Updated Title"
    }
    
    response = await client.put(
        f"/api/v1/tasks/{task_id}/update", 
        json=update_data, 
        headers=member_auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "IN_PROGRESS"
    assert response_data["title"] == "Task Updated Title"


# case 03 : update task failure (task not found)
@pytest.mark.asyncio
async def test_update_task_not_found(client, member_auth_headers):
    fake_task_id = 999999
    update_data = {"status": "IN_PROGRESS"} 
    
    response = await client.put(
        f"/api/v1/tasks/{fake_task_id}/update", 
        json=update_data, 
        headers=member_auth_headers
    )

    if response.status_code not in [404, 400]:
        print(f"DEBUG NOT FOUND ERROR: {response.json()}")

    assert response.status_code in [404, 400]

# case 04 : list tasks success
@pytest.mark.asyncio
async def test_list_tasks_success(client, member_auth_headers, test_project_member, test_user_member):
    for i in range(2):
        task_data = {
            "title": f"Task {i}",
            "project_id": test_project_member.project_id,
            "priority": "LOW",
            "status": "TO_DO",
            "due_date": (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)).isoformat(),
            "assigned_to": test_user_member.user_id,
        }
        await client.post("/api/v1/tasks/create", json=task_data, headers=member_auth_headers)
    params = {
        "project_id": test_project_member.project_id,
        "page": 1,
        "limit": 10
    }
    response = await client.get("/api/v1/tasks/list", params=params, headers=member_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2 
    assert data[0]["project_id"] == test_project_member.project_id

# case 05 : list tasks with filter (priority & status)
@pytest.mark.asyncio
async def test_list_tasks_filter(client, member_auth_headers, test_project_member, test_user_member):
    task_high = {
        "title": "High Task",
        "project_id": test_project_member.project_id,
        "priority": "HIGH",
        "status": "TO_DO",
        "due_date": (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)).isoformat(),
        "assigned_to": test_user_member.user_id,
    }
    await client.post("/api/v1/tasks/create", json=task_high, headers=member_auth_headers)
    params = {
        "project_id": test_project_member.project_id,
        "priority": "HIGH",
        "status_task": "TO_DO" 
    }
    
    response = await client.get("/api/v1/tasks/list", params=params, headers=member_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["priority"] == "HIGH"
    assert data[0]["status"] == "TO_DO"
# case  06 : list tasks with filter (assigned_to)
@pytest.mark.asyncio
async def test_list_task_filter (client, member_auth_headers, test_project_member, test_user_member):
    task_data = {
        "title": "Assigned Task",
        "project_id": test_project_member.project_id,
        "priority": "MEDIUM",
        "status": "TO_DO",
        "due_date": (datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=1)).isoformat(),
        "assigned_to": test_user_member.user_id,
    }
    await client.post("/api/v1/tasks/create", json=task_data, headers=member_auth_headers)
    params = {
        "project_id": test_project_member.project_id,
        "assigned_to": test_user_member.user_id
    }
    response = await client.get("/api/v1/tasks/list", params=params, headers=member_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["assignee_id"] == test_user_member.user_id
# case 07 : list tasks failure (missing required project_id)
@pytest.mark.asyncio
async def test_list_tasks_missing_project_id(client, member_auth_headers):
    response = await client.get("/api/v1/tasks/list", headers=member_auth_headers)
    assert response.status_code == 422

import pytest

# case 01  : add comment to task success
@pytest.mark.asyncio
async def test_add_comment_success(client, member_auth_headers , test_task_in_project ):
    comment_data = {
        "task_id": test_task_in_project.task_id,
        "content": "This is a test comment from member."
    }
    response = await client.post("/api/v1/comments/create", json=comment_data, headers=member_auth_headers)
    assert response.status_code == 201
    response_data = response.json()
    assert "comment_id" in response_data
    assert response_data["content"] == "This is a test comment from member."
# case 02 : add comment failure ( task not found )
@pytest.mark.asyncio
async def test_add_comment_task_not_found(client, member_auth_headers):
    comment_data = {
        "task_id": 999999,  
        "content": "This comment should fail."
    }
    response = await client.post("/api/v1/comments/create", json=comment_data, headers=member_auth_headers)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["message"] == "Task does not exist"
# case 03 : add comment missing content
@pytest.mark.asyncio
async def test_add_comment_missing_content(client, member_auth_headers , test_task_in_project):
    comment_data = {
        "task_id": test_task_in_project.task_id,
    }
    response = await client.post("/api/v1/comments/create", json=comment_data, headers=member_auth_headers)
    assert response.status_code == 422 
@pytest.mark.asyncio
async def test_add_comment_missing_task_id(client, member_auth_headers):
    comment_data = {
        "content": "This comment should fail due to missing task_id."
    }
    response = await client.post("/api/v1/comments/create", json=comment_data, headers=member_auth_headers)
    assert response.status_code == 422  


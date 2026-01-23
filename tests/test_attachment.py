import pytest
from httpx import AsyncClient
# case 01: Attach file success 
@pytest.mark.asyncio
async def test_attach_file_success(client, member_auth_headers, test_task_in_project):
    file_content = b"fake_image_content"
    file_name = "test_image.png"
    form_data = {
        "task_id": str(test_task_in_project.task_id)
    }
    files = {
        "file": (file_name, file_content, "image/png")
    }
    
    response = await client.post("/api/v1/attachments/upload",headers=member_auth_headers,data=form_data, files=files )

    assert response.status_code == 201
    data = response.json()
    assert "attachment_id" in data
    assert data["file_name"] == file_name
    assert data["file_size"] == len(file_content)

# case 02: Attach file failure (Task not found) 
@pytest.mark.asyncio
async def test_attach_file_task_not_found(client, member_auth_headers ):
    fake_task_id = "999999"
    form_data = {"task_id": fake_task_id}
    files = {"file": ("test.png", b"content", "image/png")}
    
    response = await client.post("/api/v1/attachments/upload", headers=member_auth_headers, data=form_data, files=files)
    assert response.status_code == 403

# case 03 : Attach over size limit (>5MB) 
@pytest.mark.asyncio
async def test_attach_file_oversize(client, member_auth_headers, test_task_in_project):
    large_content = b"0" * (5 * 1024 * 1024 + 10) 
    form_data = {"task_id": str(test_task_in_project.task_id)}
    files = {
        "file": ("large_file.zip", large_content, "application/zip")
    }
    
    response = await client.post("/api/v1/attachments/upload", headers=member_auth_headers, data=form_data, files=files)
    assert response.status_code == 400

# case 04 : Attach over number of files (Max 3 files) 
@pytest.mark.asyncio
async def test_attach_file_max_limit(client, member_auth_headers, test_task_in_project):
    form_data = {"task_id": str(test_task_in_project.task_id)}
    for i in range(3):
        files = {"file": (f"file_{i}.png", b"valid_content", "image/png")}
        response = await client.post(
            "/api/v1/attachments/upload",
            headers=member_auth_headers,
            data=form_data,
            files=files
        )
        assert response.status_code == 201
    files_fail = {"file": ("file_4.png", b"valid_content", "image/png")}
    response = await client.post("/api/v1/attachments/upload", headers=member_auth_headers, data=form_data, files=files_fail)
    
    assert response.status_code == 400
  